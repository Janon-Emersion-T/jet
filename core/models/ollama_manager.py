import subprocess
import time


def _run(command: list[str], timeout: int = 20):
    try:
        started = time.time()

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        duration = round(time.time() - started, 3)

        return {
            "ok": result.returncode == 0,
            "command": " ".join(command),
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "duration_seconds": duration,
        }

    except FileNotFoundError:
        return {
            "ok": False,
            "error": "Ollama is not installed or not available in PATH.",
        }

    except subprocess.TimeoutExpired:
        return {
            "ok": False,
            "error": "Ollama command timed out.",
        }


def list_ollama_models():
    result = _run(["ollama", "list"])

    if not result.get("ok"):
        return result

    lines = result["stdout"].splitlines()
    models = []

    for line in lines[1:]:
        parts = line.split()
        if parts:
            models.append(parts[0])

    return {
        "ok": True,
        "models": models,
        "raw": result["stdout"],
    }


def pull_ollama_model(model_name: str):
    return _run(["ollama", "pull", model_name], timeout=600)


def test_ollama_model(model_name: str):
    started = time.time()

    result = _run(
        ["ollama", "run", model_name, "Reply with one short sentence: ready."],
        timeout=60,
    )

    result["model"] = model_name
    result["latency_seconds"] = round(time.time() - started, 3)

    return result