import json
import time
from pathlib import Path
from core.models.ollama_manager import test_ollama_model

PERFORMANCE_PATH = Path("storage/model_performance.json")


def load_model_performance():
    if not PERFORMANCE_PATH.exists():
        return {}

    with PERFORMANCE_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_model_performance(data: dict):
    PERFORMANCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    PERFORMANCE_PATH.write_text(json.dumps(data, indent=4), encoding="utf-8")
    return data


def benchmark_model(model_name: str):
    result = test_ollama_model(model_name)

    performance = load_model_performance()

    performance[model_name] = {
        "model": model_name,
        "ok": result.get("ok", False),
        "latency_seconds": result.get("latency_seconds"),
        "tested_at": int(time.time()),
        "stdout": result.get("stdout", ""),
        "stderr": result.get("stderr", ""),
        "error": result.get("error", ""),
    }

    save_model_performance(performance)
    return performance[model_name]
