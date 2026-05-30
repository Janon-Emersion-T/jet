import os
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


def terminate_process(process, name):
    if process and process.poll() is None:
        print(f"Stopping {name}...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print(f"Force killing {name}...")
            process.kill()


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
                "--host",
                "127.0.0.1",
                "--port",
                "8000",
            ],
            cwd=BASE_DIR,
        )

        time.sleep(3)

        print("Launching Electron frontend...")

        frontend_process = subprocess.Popen(
            ["npm", "run", "app"],
            cwd=FRONTEND_DIR,
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