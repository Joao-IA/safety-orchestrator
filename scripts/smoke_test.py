"""Verifica a infra do passo 1 SEM gastar API: usa um cliente fake que simula
os quatro estados do classificador. Rode:  python -m scripts.smoke_test"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cache import DiskCache
from src.cost import CostTracker
from src.models import CallResult, ClassifierState
from pathlib import Path
import tempfile


def fake_result(item_id, model_id, state: ClassifierState) -> CallResult:
    return CallResult(
        item_id=item_id, requested_model=model_id,
        served_model="opus-4-8" if state == ClassifierState.FALLBACK else model_id,
        classifier_state=state,
        text=None if state in (ClassifierState.FLAGGED, ClassifierState.ERROR) else "resposta simulada",
        flag_category="cyber" if state == ClassifierState.FLAGGED else None,
        request_id="req_fake123",
        prompt_tokens=120, completion_tokens=80,
    )


def main():
    tmp = Path(tempfile.mkdtemp())
    cache = DiskCache(tmp, enabled=True)
    cost = CostTracker()

    prompt = "prompt defensivo de exemplo"
    for state in ClassifierState:
        r = fake_result(f"item_{state.value}", "fable-5", state)
        cache.put(prompt, r)
        got = cache.get(r.item_id, "fable-5", prompt)
        assert got is not None and got.from_cache, "cache round-trip falhou"
        assert got.classifier_state == state
        cost.record("fable-5", r.prompt_tokens, r.completion_tokens, from_cache=False)
        print(f"  [{state.value:8}] cache OK  flag={got.flag_category}  served={got.served_model}")

    print("\nResumo de custo:", cost.summary())
    print("\nSMOKE TEST OK — infra do passo 1 íntegra (cache, custo, estados do classificador).")


if __name__ == "__main__":
    main()
