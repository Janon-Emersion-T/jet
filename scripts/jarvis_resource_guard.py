#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
STATUS_PATH = ROOT_DIR / "storage" / "local_ai" / "resource_guard_status.json"


def _run(command: list[str], timeout: int = 20) -> tuple[bool, str]:
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
        text = result.stdout.strip() or result.stderr.strip()
        return result.returncode == 0, text
    except Exception as exc:
        return False, str(exc)


def _meminfo() -> dict[str, float]:
    values: dict[str, float] = {}
    for raw in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        number = value.strip().split()[0]
        values[key] = round(float(number) / 1024 / 1024, 2)
    return values


def _gpu_info() -> dict:
    ok, text = _run(
        [
            "nvidia-smi",
            "--query-gpu=name,memory.total,memory.used,utilization.gpu",
            "--format=csv,noheader,nounits",
        ],
        timeout=10,
    )
    if not ok or not text:
        return {"detected": False}

    parts = [part.strip() for part in text.splitlines()[0].split(",")]
    total = round(float(parts[1]) / 1024, 2)
    used = round(float(parts[2]) / 1024, 2)
    return {
        "detected": True,
        "name": parts[0],
        "total_vram_gb": total,
        "used_vram_gb": used,
        "free_vram_gb": round(max(total - used, 0), 2),
        "gpu_util_percent": float(parts[3]),
    }


def _stop_ollama_models() -> list[str]:
    ok, text = _run(["ollama", "ps"], timeout=15)
    if not ok or not text:
        return []

    stopped: list[str] = []
    for line in text.splitlines()[1:]:
        parts = line.split()
        if not parts:
            continue
        model = parts[0]
        stop_ok, _ = _run(["ollama", "stop", model], timeout=15)
        if stop_ok:
            stopped.append(model)
    return stopped


def guard_once() -> dict:
    mem = _meminfo()
    gpu = _gpu_info()
    ram_available = mem.get("MemAvailable", 0.0)
    swap_used = round(max(mem.get("SwapTotal", 0.0) - mem.get("SwapFree", 0.0), 0.0), 2)
    gpu_free = gpu.get("free_vram_gb", 999.0)

    actions: list[str] = []
    stopped_models: list[str] = []

    if ram_available < 1.0 or swap_used > 3.0 or gpu_free < 0.5:
        stopped_models = _stop_ollama_models()
        if stopped_models:
            actions.append("stopped_ollama_models")

    payload = {
        "time": datetime.now(timezone.utc).isoformat(),
        "ram_available_gb": ram_available,
        "swap_used_gb": swap_used,
        "gpu": gpu,
        "actions": actions,
        "stopped_models": stopped_models,
    }
    STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATUS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()

    if args.once:
        print(json.dumps(guard_once(), indent=2))
        return 0

    print(json.dumps({"ok": False, "error": "Use --once when running from systemd."}, indent=2))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
