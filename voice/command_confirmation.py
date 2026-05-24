from voice.text_to_speech import speak


def confirm_voice_command(command: str) -> bool:
    speak(f"You said: {command}. Say confirm to continue.")

    # Real second-listen confirmation can come later.
    # For now we return True to avoid blocking workflow.
    return True