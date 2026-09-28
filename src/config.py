"""Carregamento e validação da configuração do experimento."""
from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path
import yaml
from dotenv import load_dotenv

load_dotenv()  # carrega ANTHROPIC_API_KEY do .env


@dataclass(frozen=True)
class ModelSpec:
    id: str
    label: str


@dataclass(frozen=True)
class Config:
    name: str
    seed: int
    sample_size: int
    primary: ModelSpec
    fallback: ModelSpec
    max_tokens: int
    temperature: float
    max_retries: int
    backoff_base_seconds: float
    requests_per_minute: int
    cache_enabled: bool
    cache_dir: Path
    results_dir: Path
    raw_dir: Path
    api_key: str

    @staticmethod
    def load(path: str | Path = "configs/config.yaml") -> "Config":
        raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY não definido. Copie .env.example para .env e preencha."
            )
        m = raw["models"]
        r = raw["runtime"]
        p = raw["paths"]
        cfg = Config(
            name=raw["experiment"]["name"],
            seed=int(raw["experiment"]["seed"]),
            sample_size=int(raw["experiment"]["sample_size"]),
            primary=ModelSpec(**m["primary"]),
            fallback=ModelSpec(**m["fallback_disclosed"]),
            max_tokens=int(raw["generation"]["max_tokens"]),
            temperature=float(raw["generation"]["temperature"]),
            max_retries=int(r["max_retries"]),
            backoff_base_seconds=float(r["backoff_base_seconds"]),
            requests_per_minute=int(r["requests_per_minute"]),
            cache_enabled=bool(r["cache_enabled"]),
            cache_dir=Path(p["cache_dir"]),
            results_dir=Path(p["results_dir"]),
            raw_dir=Path(p["raw_dir"]),
            api_key=api_key,
        )
        for d in (cfg.cache_dir, cfg.results_dir, cfg.raw_dir):
            d.mkdir(parents=True, exist_ok=True)
        return cfg
