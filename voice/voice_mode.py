from core.command_router import route_command
from core.memory import save_memory
from core.chat_sessions import append_message, build_recent_context, ensure_chat_session
from voice.speech_to_text import listen
from voice.text_to_speech import speak
from voice.voice_state import VOICE_STATE


def start_voice_mode():
    speak("JARVIS voice mode activated.")

    session = ensure_chat_session("Voice chat")
    VOICE_STATE["chat_session_id"] = session["id"]

    while True:
        user_input = listen()

        if not user_input:
            continue

        print(f"YOU: {user_input}")

        if user_input.lower() in ["exit", "quit", "shutdown", "stop voice mode"]:
            speak("Voice mode shutting down.")
            break

        chat_context = build_recent_context(VOICE_STATE["chat_session_id"], limit=8)
        response = route_command(user_input, chat_context=chat_context)

        append_message(VOICE_STATE["chat_session_id"], "user", user_input)
        append_message(VOICE_STATE["chat_session_id"], "jarvis", response)

        print(f"JARVIS: {response}")
        speak(response[:700])

        save_memory(user_input, response)