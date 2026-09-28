"""Cache em disco por (item, modelo, prompt). Garante idempotência: não re-roda
um item já processado e não gasta API à toa entre execuções."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from typing import Optional
from .models import CallResult, ClassifierState


class DiskCache:
    def __init__(self, cache_dir: Path, enabled: bool = True):
        self.dir = Path(cache_dir)
        self.enabled = enabled
        self.dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def key(item_id: str, model_id: str, prompt: str) -> str:
        h = hashlib.sha256(f"{item_id}|{model_id}|{prompt}".encode("utf-8")).hexdigest()
        return h[:32]

    def _path(self, k: str) -> Path:
        return self.dir / f"{k}.json"

    def get(self, item_id: str, model_id: str, prompt: str) -> Optional[CallResult]:
        if not self.enabled:
            return None
        p = self._path(self.key(item_id, model_id, prompt))
        if not p.exists():
            return None
        d = json.loads(p.read_text(encoding="utf-8"))
        d["classifier_state"] = ClassifierState(d["classifier_state"])
        res = CallResult(**d)
        res.from_cache = True
        return res

    def put(self, prompt: str, result: CallResult) -> None:
        if not self.enabled:
            return
        k = self.key(result.item_id, result.requested_model, prompt)
        self._path(k).write_text(
            json.dumps(result.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
