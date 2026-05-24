from voice.voice_config import VOICE_CONFIG
from voice.piper_tts import speak_piper

import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 165)
engine.setProperty("volume", 1.0)


def speak_pyttsx3(text: str):
    try:
        engine.stop()
        engine.say(text)
        engine.runAndWait()

    except KeyboardInterrupt:
        try:
            engine.stop()
        except Exception:
            pass

    except Exception as e:
        print(f"pyttsx3 failed safely: {e}")


def speak(text: str):
    if not text:
        return

    if VOICE_CONFIG["voice_engine"] == "piper":
        speak_piper(text)
        return

    speak_pyttsx3(text)