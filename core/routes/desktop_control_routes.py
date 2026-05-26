from tools.desktop_control_tools import (
    emergency_stop,
    clear_emergency_stop,
    request_keyboard_text,
    request_mouse_click,
    request_app_launch,
    allow_app,
    list_allowed_apps,
    list_actions,
    cancel_action,
    execute_action,
)


def handle_desktop_control_routes(user_input: str, text: str = None, clean_text: str = None):
    cmd = user_input.strip()

    if cmd == "desktop control help":
        return (
            "DESKTOP CONTROL COMMANDS\n"
            "- desktop emergency stop\n"
            "- desktop clear emergency stop\n"
            "- keyboard automation request <text>\n"
            "- mouse click request <x> <y>\n"
            "- allow desktop app <app_name>\n"
            "- list allowed desktop apps\n"
            "- launch app request <app_name>\n"
            "- list desktop actions\n"
            "- cancel desktop action <action_id>\n"
            "- confirm desktop action <action_id>\n\n"
            "Safety: All actions require confirmation, expire, and cannot be replayed."
        )

    if cmd == "desktop emergency stop":
        return emergency_stop()

    if cmd == "desktop clear emergency stop":
        return clear_emergency_stop()

    if cmd.startswith("keyboard automation request "):
        text = cmd.replace("keyboard automation request ", "", 1)
        return request_keyboard_text(text)

    if cmd.startswith("mouse click request "):
        parts = cmd.replace("mouse click request ", "", 1).split()
        if len(parts) != 2:
            return {"success": False, "error": "Usage: mouse click request <x> <y>"}
        return request_mouse_click(parts[0], parts[1])

    if cmd.startswith("allow desktop app "):
        app = cmd.replace("allow desktop app ", "", 1).strip()
        return allow_app(app)

    if cmd == "list allowed desktop apps":
        return list_allowed_apps()

    if cmd.startswith("launch app request "):
        app = cmd.replace("launch app request ", "", 1).strip()
        return request_app_launch(app)

    if cmd == "list desktop actions":
        return list_actions()

    if cmd.startswith("cancel desktop action "):
        action_id = cmd.replace("cancel desktop action ", "", 1).strip()
        return cancel_action(action_id)

    if cmd.startswith("confirm desktop action "):
        action_id = cmd.replace("confirm desktop action ", "", 1).strip()
        return execute_action(action_id)

    return None
