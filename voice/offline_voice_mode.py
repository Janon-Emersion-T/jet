from core.command_router import route_command
from core.memory import save_memory
from voice.offline_speech_to_text import listen_offline
from voice.text_to_speech import speak
from voice.command_correction import correct_voice_command
from voice.wake_word import has_wake_word
from voice.silence_detector import is_noise_or_silence
from voice.voice_config import VOICE_CONFIG
from voice.voice_state import VOICE_STATE
from core.system_modes import set_voice_mode

STOP_PHRASES = [
    "stop voice mode",
    "deactivate voice mode",
    "deactivate offline voice mode",
    "exit voice mode",
    "shutdown voice mode",
    "go back to text mode",
]


def start_offline_voice_mode():
    VOICE_STATE["mode"] = "listening"
    VOICE_STATE["interrupted"] = False
    speak("Voice mode activated.")

    try:
        while True:
            raw_input = listen_offline(seconds=VOICE_CONFIG["listen_seconds"]).strip()

            VOICE_STATE["last_heard"] = raw_input

            if raw_input == "__INTERRUPTED__":
                speak("Voice mode interrupted.")
                break

            if is_noise_or_silence(raw_input):
                continue

            user_input = correct_voice_command(raw_input)
            text = user_input.lower().strip()

            print(f"YOU: {user_input}")

            if text in STOP_PHRASES:
                speak("Voice mode deactivated.")
                break

            if has_wake_word(text):
                response = "Master Janon. What can I assist you with?"
                print(f"JARVIS: {response}")
                speak(response)
                continue

            if VOICE_CONFIG["wake_required"]:
                continue

            VOICE_STATE["last_command"] = user_input
            VOICE_STATE["mode"] = "processing"

            if VOICE_CONFIG.get("command_confirmation"):
                from voice.command_confirmation import confirm_voice_command

                if not confirm_voice_command(user_input):
                    speak("Command cancelled.")
                    continue

            response = route_command(user_input)

            print(f"JARVIS: {response}")
            VOICE_STATE["last_response"] = response
            VOICE_STATE["mode"] = "listening"
            
            speak(response[:700])

            save_memory(user_input, response)

    except KeyboardInterrupt:
        VOICE_STATE["mode"] = "idle"
        VOICE_STATE["interrupted"] = True
        print("\nVoice mode stopped safely.")
        try:
            speak("Voice mode stopped safely.")
        except Exception:
            pass
    finally:
        VOICE_STATE["mode"] = "idle"
        set_voice_mode(False)
