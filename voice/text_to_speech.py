import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 165)
engine.setProperty("volume", 1.0)


def speak(text: str):
    if not text:
        return

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
        print(f"TTS failed safely: {e}")