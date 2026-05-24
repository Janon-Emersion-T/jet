from core.command_router import route_command
from core.memory import save_memory
from voice.offline_speech_to_text import listen_offline
from voice.text_to_speech import speak

STOP_PHRASES = [
    "stop voice mode",
    "deactivate voice mode",
    "deactivate offline voice mode",
    "exit voice mode",
    "shutdown voice mode",
    "go back to text mode",
]

WAKE_PHRASES = [
    "hey jarvis",
    "hey jabbies",
    "jarvis",
    "jabbies",
]


def _is_blank(text: str) -> bool:
    lowered = text.lower().strip()
    return (
        not lowered
        or "[blank_audio]" in lowered
        or "blank audio" in lowered
        or lowered == "__interrupted__"
    )


def _is_wake_phrase(text: str) -> bool:
    lowered = text.lower().strip()
    return any(phrase in lowered for phrase in WAKE_PHRASES)


def start_offline_voice_mode():
    speak("Voice mode activated.")

    try:
        while True:
            user_input = listen_offline(seconds=5).strip()

            if user_input == "__INTERRUPTED__":
                speak("Voice mode interrupted.")
                break

            if _is_blank(user_input):
                continue

            text = user_input.lower().strip()
            print(f"YOU: {user_input}")

            if text in STOP_PHRASES:
                speak("Voice mode deactivated.")
                break

            if _is_wake_phrase(text):
                response = "Master Janon. What can I assist you with?"
                print(f"JARVIS: {response}")
                speak(response)
                continue

            response = route_command(user_input)

            print(f"JARVIS: {response}")
            speak(response[:700])

            save_memory(user_input, response)

    except KeyboardInterrupt:
        print("\nVoice mode stopped safely.")
        speak("Voice mode stopped safely.")