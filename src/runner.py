"""Orquestra config + cache + client + custo em torno de uma chamada.
Esta é a 'engine' do passo 1. O passo 3 (ingestão do Juliet + montagem dos
prompts defensivos) vai consumir este runner."""
from __future__ import annotations
from typing import Optional
from .config import Config
from .cache import DiskCache
from .cost import CostTracker
from .client import SafeguardClient
from .models import CallResult


class Runner:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.cache = DiskCache(cfg.cache_dir, cfg.cache_enabled)
        self.cost = CostTracker()
        self.client = SafeguardClient(cfg)

    def run_one(self, item_id: str, model_id: str, prompt: str,
                system: Optional[str] = None) -> CallResult:
        cached = self.cache.get(item_id, model_id, prompt)
        if cached is not None:
            self.cost.record(model_id, cached.prompt_tokens,
                             cached.completion_tokens, from_cache=True)
            return cached
        res = self.client.call(item_id, model_id, prompt, system=system)
        self.cache.put(prompt, res)
        self.cost.record(model_id, res.prompt_tokens,
                         res.completion_tokens, from_cache=False)
        return res

    def run_both_models(self, item_id: str, prompt: str,
                        system: Optional[str] = None) -> dict[str, CallResult]:
        """Roda o MESMO prompt no primary (classificador ativo) e no fallback."""
        return {
            self.cfg.primary.label: self.run_one(item_id, self.cfg.primary.id, prompt, system),
            self.cfg.fallback.label: self.run_one(item_id, self.cfg.fallback.id, prompt, system),
        }
