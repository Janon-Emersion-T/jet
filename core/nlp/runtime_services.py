from dataclasses import dataclass
from datetime import datetime
import json
import os
from pathlib import Path
import platform
import time
from typing import Dict, Optional


CACHE_FILE = Path("storage/nlp/semantic_cache.json")
AVAILABLE_MODELS = [
    "BAAI/bge-small-en-v1.5",
    "sentence-transformers/all-MiniLM-L6-v2",
]


@dataclass
class RuntimeProfile:
    embedding_model: str
    device: str
    cache_hit: bool = False
    keyword_fallback: bool = False


def select_local_embedding_model() -> str:
    configured = os.getenv("JARVIS_EMBEDDING_MODEL", "").strip()
    return configured or AVAILABLE_MODELS[0]


def model_cache_status() -> Dict[str, object]:
    locations = [Path.home() / ".cache" / "huggingface", Path("storage/models")]
    return {
        "models": AVAILABLE_MODELS,
        "cache_locations": [str(path) for path in locations],
        "available_locations": [str(path) for path in locations if path.exists()],
    }


def profile_runtime() -> Dict[str, str]:
    device = "gpu" if os.getenv("CUDA_VISIBLE_DEVICES", "").strip() not in {"", "-1"} else "cpu"
    return {
        "device": device,
        "platform": platform.system().lower(),
        "embedding_model": select_local_embedding_model(),
    }


def warmup_transformer() -> Dict[str, object]:
    started = time.perf_counter()
    try:
        from core.nlp.phase000b_semantic_router import get_embedding_model

        loaded = get_embedding_model() is not None
    except Exception:
        loaded = False
    return {"loaded": loaded, "elapsed_ms": round((time.perf_counter() - started) * 1000, 2)}


def _load_cache() -> Dict:
    if not CACHE_FILE.exists():
        return {}
    try:
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def semantic_cache_get(key: str) -> Optional[Dict]:
    return _load_cache().get(key.strip().lower())


def semantic_cache_put(key: str, value: Dict) -> None:
    cache = _load_cache()
    cache[key.strip().lower()] = {
        "value": value,
        "updated_at": datetime.now().isoformat(timespec="seconds"),
    }
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(cache, indent=2), encoding="utf-8")


def keyword_fallback(text: str) -> Optional[str]:
    rules = {
        "git": "devops", "deploy": "devops", "database": "database",
        "sql": "database", "invoice": "accounting", "marketing": "marketing",
        "research": "research", "file": "project_analysis",
    }
    lowered = text.lower()
    return next((intent for keyword, intent in rules.items() if keyword in lowered), None)
