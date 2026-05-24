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

def start_offline_voice_mode():
    speak("Voice mode activated.")

    while True:
        user_input = listen_offline(seconds=5).strip()

        if not user_input:
            continue

        text = user_input.lower().strip()

        if "[blank_audio]" in text or "blank audio" in text:
            continue

        print(f"YOU: {user_input}")

        if text in STOP_PHRASES:
            speak("Voice mode deactivated.")
            break

        response = route_command(user_input)

        print(f"JARVIS: {response}")
        speak(response[:700])

        save_memory(user_input, response)