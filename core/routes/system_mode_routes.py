from core.system_modes import (
    show_system_mode,
    set_prompt_version,
    set_personality_profile,
    set_active_mode,
    set_strict_mode,
    set_developer_mode,
)


def handle_system_mode_routes(user_input: str, text: str, clean_text: str):
    if text in ["system mode", "show system mode", "jarvis mode"]:
        return show_system_mode()

    if text.startswith("set prompt version "):
        version = user_input.replace("set prompt version ", "", 1).strip()
        return set_prompt_version(version)

    if text.startswith("set personality "):
        profile = user_input.replace("set personality ", "", 1).strip()
        return set_personality_profile(profile)

    if text.startswith("set mode "):
        mode = user_input.replace("set mode ", "", 1).strip()
        return set_active_mode(mode)

    if text in ["enable strict mode", "strict mode on"]:
        return set_strict_mode(True)

    if text in ["disable strict mode", "strict mode off"]:
        return set_strict_mode(False)

    if text in ["enable developer mode", "developer mode on"]:
        return set_developer_mode(True)

    if text in ["disable developer mode", "developer mode off"]:
        return set_developer_mode(False)

    if text in ["business mode", "enable business mode"]:
        return set_active_mode("business")

    if text in ["tutor mode", "enable tutor mode"]:
        return set_active_mode("tutor")

    if text in ["research mode", "enable research mode"]:
        return set_active_mode("research")

    if text in ["seo mode", "enable seo mode"]:
        return set_active_mode("seo")

    if text in ["social media mode", "social mode", "enable social media mode"]:
        return set_active_mode("social")

    return None