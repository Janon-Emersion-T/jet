from core.system_modes import (
    show_system_mode,
    list_system_modes,
    reset_system_mode,
    set_prompt_version,
    set_personality_profile,
    set_active_mode,
    set_strict_mode,
    set_developer_mode,
)


def handle_system_mode_routes(user_input: str, text: str, clean_text: str):
    if text in ["system mode", "show system mode", "jarvis mode"]:
        return show_system_mode()

    if text in ["list modes", "available modes", "show modes"]:
        return list_system_modes()

    if text in ["reset mode", "reset system mode", "default mode"]:
        return reset_system_mode()

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

    mode_shortcuts = {
        "business mode": "business",
        "enable business mode": "business",
        "tutor mode": "tutor",
        "enable tutor mode": "tutor",
        "research mode": "research",
        "enable research mode": "research",
        "seo mode": "seo",
        "enable seo mode": "seo",
        "social media mode": "social",
        "social mode": "social",
        "enable social media mode": "social",
    }

    if text in mode_shortcuts:
        return set_active_mode(mode_shortcuts[text])

    return None