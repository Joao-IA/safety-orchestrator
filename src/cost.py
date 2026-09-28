"""Rastreamento simples de tokens e custo por execução."""
from __future__ import annotations
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class CostTracker:
    calls: int = 0
    api_calls: int = 0          # exclui cache hits
    prompt_tokens: int = 0
    completion_tokens: int = 0
    by_model: dict = field(default_factory=lambda: defaultdict(lambda: {"in": 0, "out": 0, "n": 0}))

    def record(self, model_id: str, prompt_tokens: int, completion_tokens: int, from_cache: bool):
        self.calls += 1
        if not from_cache:
            self.api_calls += 1
        self.prompt_tokens += prompt_tokens
        self.completion_tokens += completion_tokens
        m = self.by_model[model_id]
        m["in"] += prompt_tokens
        m["out"] += completion_tokens
        m["n"] += 1

    def summary(self) -> dict:
        return {
            "total_calls": self.calls,
            "api_calls": self.api_calls,
            "cache_hits": self.calls - self.api_calls,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "by_model": {k: dict(v) for k, v in self.by_model.items()},
        }
