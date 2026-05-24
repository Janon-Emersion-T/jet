import subprocess
from pathlib import Path

WHISPER_PATH = str(Path.home() / "whisper.cpp" / "build" / "bin" / "whisper-cli")
MODEL_PATH = str(Path.home() / "whisper.cpp" / "models" / "ggml-base.en.bin")
AUDIO_PATH = "storage/input.wav"


def record_audio(seconds: int = 5):
    print("Listening offline...")

    try:
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-f", "pulse",
                "-i", "default",
                "-t", str(seconds),
                "-ar", "16000",
                "-ac", "1",
                AUDIO_PATH,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except KeyboardInterrupt:
        return False
    except Exception as e:
        print(f"Audio recording failed: {e}")
        return False

    return True


def transcribe_audio() -> str:
    try:
        result = subprocess.run(
            [
                WHISPER_PATH,
                "-m", MODEL_PATH,
                "-f", AUDIO_PATH,
                "-nt",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
    except KeyboardInterrupt:
        return "__INTERRUPTED__"
    except Exception as e:
        return f"__ERROR__: {e}"

    lines = result.stdout.strip().splitlines()

    if not lines:
        return ""

    return lines[-1].strip()


def listen_offline(seconds: int = 5) -> str:
    recorded = record_audio(seconds)

    if not recorded:
        return "__INTERRUPTED__"

    return transcribe_audio()