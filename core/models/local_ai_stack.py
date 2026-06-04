from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent.parent.parent
CATALOG_PATH = BASE_DIR / "config" / "local_ai_models.json"
STATE_DIR = BASE_DIR / "storage" / "local_ai"
HF_CACHE_DIR = STATE_DIR / "hf-cache"


def _run(command: list[str], timeout: int = 60) -> dict[str, Any]:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return {
            "ok": result.returncode == 0,
            "code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
    except Exception as exc:
        return {"ok": False, "code": -1, "stdout": "", "stderr": str(exc)}


def load_catalog() -> dict[str, Any]:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def _parse_meminfo() -> dict[str, float]:
    values: dict[str, float] = {}
    try:
        for raw in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
            if ":" not in raw:
                continue
            key, value = raw.split(":", 1)
            parts = value.strip().split()
            if not parts:
                continue
            kb = float(parts[0])
            values[key] = round(kb / 1024 / 1024, 2)
    except Exception:
        pass
    return values


def detect_system_profile() -> dict[str, Any]:
    meminfo = _parse_meminfo()
    ram_total = round(meminfo.get("MemTotal", 0.0), 2)
    ram_available = round(meminfo.get("MemAvailable", 0.0), 2)
    swap_total = round(meminfo.get("SwapTotal", 0.0), 2)
    swap_free = round(meminfo.get("SwapFree", 0.0), 2)

    gpu = {
        "detected": False,
        "name": "",
        "total_vram_gb": 0.0,
        "used_vram_gb": 0.0,
        "free_vram_gb": 0.0,
    }
    nvidia = _run(
        [
            "nvidia-smi",
            "--query-gpu=name,memory.total,memory.used",
            "--format=csv,noheader,nounits",
        ],
        timeout=15,
    )
    if nvidia["ok"] and nvidia["stdout"]:
        first = nvidia["stdout"].splitlines()[0]
        parts = [part.strip() for part in first.split(",")]
        if len(parts) >= 3:
            total = round(float(parts[1]) / 1024, 2)
            used = round(float(parts[2]) / 1024, 2)
            gpu = {
                "detected": True,
                "name": parts[0],
                "total_vram_gb": total,
                "used_vram_gb": used,
                "free_vram_gb": round(max(total - used, 0), 2),
            }

    return {
        "ram_total_gb": ram_total,
        "ram_class_gb": int(round(ram_total)),
        "ram_available_gb": ram_available,
        "swap_total_gb": swap_total,
        "swap_used_gb": round(max(swap_total - swap_free, 0), 2),
        "gpu": gpu,
    }


def _ollama_installed_models() -> list[str]:
    result = _run(["ollama", "list"], timeout=30)
    if not result["ok"]:
        return []
    lines = result["stdout"].splitlines()[1:]
    return [line.split()[0] for line in lines if line.split()]


def _hf_cached(model_id: str) -> bool:
    slug = model_id.replace("/", "--")
    return (HF_CACHE_DIR / slug).exists()


def _service_active(service_name: str) -> bool:
    result = _run(["systemctl", "--user", "is-active", service_name], timeout=15)
    return result["ok"] and result["stdout"].strip() == "active"


def evaluate_catalog() -> dict[str, Any]:
    catalog = load_catalog()
    system = detect_system_profile()
    installed_ollama = set(_ollama_installed_models())
    gpu_vram = system["gpu"]["total_vram_gb"] if system["gpu"]["detected"] else 0.0

    items: list[dict[str, Any]] = []
    for model in catalog.get("models", []):
        backend = model.get("backend", "")
        runtime_model = model.get("runtime_model", "")
        if backend == "ollama":
            installed = runtime_model in installed_ollama
        elif backend == "diffusers":
            installed = _hf_cached(runtime_model)
        elif backend == "chromadb":
            installed = True
        else:
            installed = False

        min_ram = float(model.get("min_ram_gb", 0))
        ram_ok = system.get("ram_total_gb", 0.0) >= max(min_ram - 1.25, 0.0)
        vram_needed = float(model.get("recommended_vram_gb", 0))
        vram_ok = gpu_vram >= vram_needed if vram_needed > 0 else True

        verdict = "ready"
        if not ram_ok:
            verdict = "not-enough-ram"
        elif vram_needed > 0 and not vram_ok:
            verdict = "cpu-offload-required" if backend == "ollama" else "tight-fit"

        items.append(
            {
                **model,
                "installed": installed,
                "service_active": _service_active("jarvis-chromadb.service") if backend == "chromadb" else None,
                "compatibility": verdict,
            }
        )

    return {
        "catalog": items,
        "defaults": catalog.get("defaults", {}),
        "system": system,
    }


def _find_model(model_id: str) -> dict[str, Any]:
    for model in load_catalog().get("models", []):
        if model.get("id") == model_id:
            return model
    raise KeyError(f"Unknown local AI target: {model_id}")


def install_target(model_id: str) -> dict[str, Any]:
    model = _find_model(model_id)
    install_method = model.get("install_method")
    runtime_model = model.get("runtime_model", "")

    if install_method == "ollama_pull":
        result = _run(["ollama", "pull", runtime_model], timeout=7200)
        return {"ok": result["ok"], "target": model_id, "stdout": result["stdout"], "stderr": result["stderr"]}

    if install_method == "huggingface_snapshot":
        try:
            from huggingface_hub import snapshot_download
        except Exception as exc:
            return {"ok": False, "target": model_id, "stderr": f"huggingface_hub is required: {exc}"}

        target_dir = HF_CACHE_DIR / runtime_model.replace("/", "--")
        target_dir.parent.mkdir(parents=True, exist_ok=True)
        os.environ.setdefault("HF_HOME", str(HF_CACHE_DIR))
        snapshot_download(repo_id=runtime_model, local_dir=str(target_dir), local_dir_use_symlinks=False)
        return {"ok": True, "target": model_id, "path": str(target_dir)}

    if install_method == "python_package":
        return {"ok": True, "target": model_id, "stdout": "No separate model download is required."}

    return {"ok": False, "target": model_id, "stderr": f"Unsupported install method: {install_method}"}


def runtime_paths() -> dict[str, str]:
    return {
        "base_dir": str(BASE_DIR),
        "state_dir": str(STATE_DIR),
        "hf_cache_dir": str(HF_CACHE_DIR),
        "venv_python": str(BASE_DIR / ".venv" / "bin" / "python"),
    }


def write_user_unit(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def prepare_user_services() -> dict[str, Any]:
    paths = runtime_paths()
    unit_dir = Path.home() / ".config" / "systemd" / "user"
    chroma_dir = BASE_DIR / "storage" / "chroma"
    chroma_dir.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)

    python_bin = paths["venv_python"]
    if not Path(python_bin).exists():
        python_bin = shutil.which("python3") or "python3"

    chroma_bin = str(BASE_DIR / ".venv" / "bin" / "chroma")
    if not Path(chroma_bin).exists():
        chroma_bin = shutil.which("chroma") or chroma_bin

    chroma_service = f"""[Unit]
Description=JARVIS ChromaDB Local Service
After=default.target

[Service]
Type=simple
WorkingDirectory={BASE_DIR}
ExecStart={chroma_bin} run --host 127.0.0.1 --port 8001 --path {chroma_dir}
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
"""

    guard_service = f"""[Unit]
Description=JARVIS Local AI Resource Guard
After=default.target

[Service]
Type=oneshot
WorkingDirectory={BASE_DIR}
ExecStart={python_bin} {BASE_DIR / 'scripts' / 'jarvis_resource_guard.py'} --once
"""

    guard_timer = """[Unit]
Description=Run JARVIS Local AI Resource Guard every minute

[Timer]
OnBootSec=2min
OnUnitActiveSec=1min
Unit=jarvis-resource-guard.service

[Install]
WantedBy=timers.target
"""

    write_user_unit(unit_dir / "jarvis-chromadb.service", chroma_service)
    write_user_unit(unit_dir / "jarvis-resource-guard.service", guard_service)
    write_user_unit(unit_dir / "jarvis-resource-guard.timer", guard_timer)

    responses = {
        "daemon_reload": _run(["systemctl", "--user", "daemon-reload"], timeout=30),
        "enable_chromadb": _run(["systemctl", "--user", "enable", "--now", "jarvis-chromadb.service"], timeout=30),
        "enable_guard_timer": _run(["systemctl", "--user", "enable", "--now", "jarvis-resource-guard.timer"], timeout=30),
    }
    return {"ok": True, "units_dir": str(unit_dir), "actions": responses}
