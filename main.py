import os
import socket
import subprocess
import sys
import time
from pathlib import Path


os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"
COMFYUI_DIR = BASE_DIR / "engines" / "ComfyUI"
COMFYUI_VENV_PYTHON = COMFYUI_DIR / "venv" / "bin" / "python"
IMAGE_OUTPUT_DIR = BASE_DIR / "storage" / "generated_images" / "outputs"
FRONTEND_NODE_MODULES = FRONTEND_DIR / "node_modules"
FRONTEND_PACKAGE_LOCK = FRONTEND_DIR / "package-lock.json"


def reserve_local_port(host: str = "127.0.0.1") -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, 0))
        return sock.getsockname()[1]


def wait_for_port(host: str, port: int, timeout: float = 10.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            if sock.connect_ex((host, port)) == 0:
                return True
        time.sleep(0.2)
    return False


def terminate_process(process, name):
    if process and process.poll() is None:
        print(f"Stopping {name}...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print(f"Force killing {name}...")
            process.kill()


def ensure_frontend_dependencies():
    concurrently_bin = FRONTEND_NODE_MODULES / ".bin" / "concurrently"
    electron_bin = FRONTEND_NODE_MODULES / ".bin" / "electron"

    if concurrently_bin.exists() and electron_bin.exists():
        return

    if not FRONTEND_PACKAGE_LOCK.exists():
        raise RuntimeError(
            f"Cannot install frontend dependencies automatically: missing {FRONTEND_PACKAGE_LOCK}"
        )

    print("Frontend dependencies missing. Running npm ci...")
    subprocess.run(
        ["npm", "ci"],
        cwd=FRONTEND_DIR,
        check=True,
    )


def start_local_image_engine():
    """
    Starts the local image engine silently as part of JARVIS.

    This does NOT open another app.
    This does NOT expose the engine to the network.
    This runs only on 127.0.0.1.
    """

    if not COMFYUI_DIR.exists():
        print("Local image engine not installed. Skipping image engine startup.")
        print("Expected path:", COMFYUI_DIR)
        return None

    if not COMFYUI_VENV_PYTHON.exists():
        print("Local image engine venv not found. Skipping image engine startup.")
        print("Expected Python:", COMFYUI_VENV_PYTHON)
        return None

    IMAGE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Starting local image engine...")

    process = subprocess.Popen(
        [
            str(COMFYUI_VENV_PYTHON),
            "main.py",
            "--listen",
            "127.0.0.1",
            "--port",
            "8188",
            "--output-directory",
            str(IMAGE_OUTPUT_DIR),
        ],
        cwd=COMFYUI_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )

    time.sleep(5)

    if process.poll() is not None:
        print("Local image engine failed to start.")
        return None

    print("Local image engine running on 127.0.0.1:8188")
    return process


def main():
    api_process = None
    frontend_process = None
    image_engine_process = None
    api_host = "127.0.0.1"
    api_port = reserve_local_port(api_host)
    api_url = f"http://{api_host}:{api_port}"

    try:
        print("JARVIS STARTING...")

        image_engine_process = start_local_image_engine()

        print("Starting existing API server...")

        api_process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "api_server:app",
                "--host", api_host,
                "--port", str(api_port),
            ],
            cwd=BASE_DIR,
        )

        if api_process.poll() is not None:
            raise RuntimeError(
                "JARVIS API failed to start. Ensure the active Python environment has uvicorn installed."
            )

        if not wait_for_port(api_host, api_port, timeout=10):
            terminate_process(api_process, "JARVIS API")
            raise RuntimeError(
                f"JARVIS API did not become reachable on {api_url}. Check backend dependencies and startup logs."
            )

        print(f"JARVIS API running on {api_url}")

        print("Launching Electron frontend...")
        ensure_frontend_dependencies()

        frontend_env = os.environ.copy()
        frontend_env["JARVIS_API_URL"] = api_url
        frontend_env.pop("ELECTRON_RUN_AS_NODE", None)

        frontend_process = subprocess.Popen(
            ["npm", "run", "app"],
            cwd=FRONTEND_DIR,
            env=frontend_env,
        )

        frontend_process.wait()

    except KeyboardInterrupt:
        print("\nJARVIS shutting down safely...")

    finally:
        terminate_process(frontend_process, "Electron frontend")
        terminate_process(api_process, "JARVIS API")
        terminate_process(image_engine_process, "Local image engine")
        print("JARVIS shutdown complete.")


if __name__ == "__main__":
    main()
