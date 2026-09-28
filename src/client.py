"""Camada fina sobre a API. Responsabilidade única: fazer UMA chamada e
classificar o resultado em ClassifierState (normal / fallback / flagged / error).

PONTO CRÍTICO METODOLÓGICO
--------------------------
O disparo do classificador (FLAGGED) e o redirecionamento (FALLBACK) são o DADO
que o estudo mede — não são erros a suprimir nem a contornar. Por isso:
  * NÃO fazemos retry em FLAGGED. Um flag é uma observação.
  * NÃO reescrevemos o prompt para evitar o flag. Isso destruiria a variável dependente.
  * Só fazemos retry em falhas transitórias reais (rate-limit, overload, rede).
"""
from __future__ import annotations
import time
from typing import Optional
import anthropic

from .config import Config
from .models import CallResult, ClassifierState


# --------------------------------------------------------------------------- #
# Detecção do estado do classificador — AJUSTE ao contrato exato do seu endpoint.
# Centralizado aqui de propósito: é a única parte específica do ambiente.
# --------------------------------------------------------------------------- #

def _extract_flag_category(err: Exception) -> Optional[str]:
    """Tenta extrair a categoria do flag (ex.: 'cyber') do erro da API.

    No erro observado: `Details: [cyber]`, com um Request ID. Adapte os campos
    conforme a resposta real do seu endpoint (body, headers, message)."""
    msg = str(getattr(err, "message", "") or err)
    for cat in ("cyber", "bio", "chem", "nuclear", "csam", "cbrn"):
        if f"[{cat}]" in msg or f"'{cat}'" in msg:
            return cat
    body = getattr(err, "body", None)
    if isinstance(body, dict):
        # ex.: {"error": {"type": "safeguard_flagged", "details": "cyber"}}
        details = body.get("error", {}).get("details")
        if isinstance(details, str):
            return details.strip("[]")
    return None


def _is_safeguard_flag(err: Exception) -> bool:
    """True se o erro representa um bloqueio do classificador (e NÃO uma falha transitória)."""
    return _extract_flag_category(err) is not None


def _served_model(response) -> Optional[str]:
    """Modelo que de fato respondeu. Se != modelo pedido, houve fallback divulgado.
    Anthropic devolve `response.model`. Se seu endpoint expuser o fallback em outro
    campo/header, ajuste aqui."""
    return getattr(response, "model", None)


# --------------------------------------------------------------------------- #

class SafeguardClient:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self._client = anthropic.Anthropic(api_key=cfg.api_key)
        self._min_interval = 60.0 / max(cfg.requests_per_minute, 1)
        self._last_call = 0.0

    def _throttle(self):
        wait = self._min_interval - (time.time() - self._last_call)
        if wait > 0:
            time.sleep(wait)
        self._last_call = time.time()

    def call(self, item_id: str, model_id: str, prompt: str,
             system: Optional[str] = None) -> CallResult:
        """Uma chamada, com retry SOMENTE em falhas transitórias."""
        attempt = 0
        while True:
            attempt += 1
            self._throttle()
            t0 = time.time()
            try:
                resp = self._client.messages.create(
                    model=model_id,
                    max_tokens=self.cfg.max_tokens,
                    temperature=self.cfg.temperature,
                    system=system or anthropic.NOT_GIVEN,
                    messages=[{"role": "user", "content": prompt}],
                )
                latency = time.time() - t0
                served = _served_model(resp)
                state = (ClassifierState.FALLBACK
                         if served and served != model_id
                         else ClassifierState.NORMAL)
                text = "".join(
                    b.text for b in resp.content if getattr(b, "type", None) == "text"
                )
                usage = getattr(resp, "usage", None)
                return CallResult(
                    item_id=item_id,
                    requested_model=model_id,
                    served_model=served,
                    classifier_state=state,
                    text=text,
                    flag_category=None,
                    request_id=getattr(resp, "_request_id", None),
                    prompt_tokens=getattr(usage, "input_tokens", 0) if usage else 0,
                    completion_tokens=getattr(usage, "output_tokens", 0) if usage else 0,
                    latency_seconds=latency,
                )

            except anthropic.APIStatusError as err:
                # 1) É um flag do classificador? -> DADO, não erro. Não faz retry.
                if _is_safeguard_flag(err):
                    return CallResult(
                        item_id=item_id,
                        requested_model=model_id,
                        served_model=None,
                        classifier_state=ClassifierState.FLAGGED,
                        text=None,
                        flag_category=_extract_flag_category(err),
                        request_id=getattr(err, "request_id", None),
                        latency_seconds=time.time() - t0,
                    )
                # 2) Falha transitória? -> retry com backoff.
                transient = getattr(err, "status_code", None) in (429, 500, 502, 503, 529)
                if transient and attempt <= self.cfg.max_retries:
                    time.sleep(self.cfg.backoff_base_seconds * (2 ** (attempt - 1)))
                    continue
                # 3) Erro definitivo não-classificador.
                return CallResult(
                    item_id=item_id, requested_model=model_id, served_model=None,
                    classifier_state=ClassifierState.ERROR, text=None,
                    flag_category=None, request_id=getattr(err, "request_id", None),
                    latency_seconds=time.time() - t0,
                )
            except anthropic.APIConnectionError:
                if attempt <= self.cfg.max_retries:
                    time.sleep(self.cfg.backoff_base_seconds * (2 ** (attempt - 1)))
                    continue
                return CallResult(
                    item_id=item_id, requested_model=model_id, served_model=None,
                    classifier_state=ClassifierState.ERROR, text=None,
                    flag_category=None, request_id=None,
                    latency_seconds=time.time() - t0,
                )
