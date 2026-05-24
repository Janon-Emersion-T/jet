import subprocess
from pathlib import Path

PIPER_BIN = str(Path.home() / "AI" / "piper" / "piper" / "piper")
VOICE_MODEL = str(
    Path.home()
    / "AI"
    / "piper"
    / "models"
    / "en_US-lessac-medium.onnx"
)

OUTPUT_FILE = "storage/piper_output.wav"


def speak_piper(text: str):
    if not text:
        return

    try:
        command = (
            f'echo "{text}" | '
            f'{PIPER_BIN} '
            f'--model {VOICE_MODEL} '
            f'--output_file {OUTPUT_FILE}'
        )

        subprocess.run(command, shell=True, check=False)

        subprocess.run(
            ["aplay", OUTPUT_FILE],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )

    except KeyboardInterrupt:
        pass

    except Exception as e:
        print(f"Piper TTS failed: {e}")
