"""Estruturas de dados do experimento. O ClassifierState é o dado primário."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional
import time


class ClassifierState(str, Enum):
    """O que aconteceu com o classificador de segurança do modelo primary.

    Esta é a variável dependente central do estudo.
    """
    NORMAL = "normal"        # primary respondeu normalmente, sem intervenção
    FALLBACK = "fallback"    # classificador redirecionou para o modelo de fallback divulgado
    FLAGGED = "flagged"      # classificador bloqueou (ex.: erro com details=[cyber])
    ERROR = "error"          # falha não relacionada ao classificador (rede, rate-limit esgotado)


@dataclass
class CallResult:
    """Resultado bruto de UMA chamada a UM modelo para UM item. Serializável em JSON."""
    item_id: str
    requested_model: str          # id do modelo que pedimos
    served_model: Optional[str]   # id do modelo que de fato respondeu (revela fallback)
    classifier_state: ClassifierState
    text: Optional[str]           # resposta do modelo (None se FLAGGED/ERROR)
    flag_category: Optional[str]  # ex.: "cyber", extraído do details do erro
    request_id: Optional[str]     # id da requisição da API, para auditoria
    prompt_tokens: int = 0
    completion_tokens: int = 0
    latency_seconds: float = 0.0
    from_cache: bool = False
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["classifier_state"] = self.classifier_state.value
        return d
