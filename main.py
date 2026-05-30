import os
import subprocess
import sys
import time
from pathlib import Path

os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"


def terminate_process(process, name):
    if process and process.poll() is None:
        print(f"Stopping {name}...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print(f"Force killing {name}...")
            process.kill()


def main():
    api_process = None
    frontend_process = None

    try:
        print("JARVIS STARTING...")
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
        print("JARVIS shutdown complete.")


if __name__ == "__main__":
    main()