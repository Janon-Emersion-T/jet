from core.command_router import route_command
from core.memory import save_memory
from voice.speech_to_text import listen
from voice.text_to_speech import speak

def start_voice_mode():
    speak("JARVIS voice mode activated.")

    while True:
        user_input = listen()

        if not user_input:
            continue

        print(f"YOU: {user_input}")

        if user_input.lower() in ["exit", "quit", "shutdown", "stop voice mode"]:
            speak("Voice mode shutting down.")
            break

        response = route_command(user_input)

        print(f"JARVIS: {response}")
        speak(response[:700])

        save_memory(user_input, response)