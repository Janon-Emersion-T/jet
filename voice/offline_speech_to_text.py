import subprocess
from pathlib import Path

WHISPER_PATH = str(Path.home() / "whisper.cpp" / "build" / "bin" / "whisper-cli")
MODEL_PATH = str(Path.home() / "whisper.cpp" / "models" / "ggml-base.en.bin")
AUDIO_PATH = "storage/input.wav"

def record_audio(seconds: int = 5):
    print("Listening offline...")
    subprocess.run([
        "ffmpeg",
        "-y",
        "-f", "pulse",
        "-i", "default",
        "-t", str(seconds),
        "-ar", "16000",
        "-ac", "1",
        AUDIO_PATH
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def transcribe_audio() -> str:
    result = subprocess.run([
        WHISPER_PATH,
        "-m", MODEL_PATH,
        "-f", AUDIO_PATH,
        "-nt"
    ], capture_output=True, text=True)

    lines = result.stdout.strip().splitlines()

    if not lines:
        return ""

    return lines[-1].strip()

def listen_offline(seconds: int = 5) -> str:
    record_audio(seconds)
    return transcribe_audio()