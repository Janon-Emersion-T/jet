from tools.desktop_control_tools import (
    desktop_control_status,
    keyboard_automation_request,
    mouse_automation_request,
    app_launcher_request,
    list_desktop_actions,
    confirm_desktop_action,
    desktop_control_help,
)


def handle_desktop_control_routes(user_input: str, text: str, clean_text: str):

    if text in ["desktop control help", "automation help"]:
        return desktop_control_help()

    # ========================================================
    # Phase 196
    # ========================================================

    if text in ["desktop control status", "desktop mode status"]:
        return desktop_control_status()

    # ========================================================
    # Phase 197
    # ========================================================

    if text.startswith("keyboard automation request "):
        details = user_input.replace("keyboard automation request ", "", 1).strip()
        return keyboard_automation_request(details)

    # ========================================================
    # Phase 198
    # ========================================================

    if text.startswith("mouse automation request "):
        details = user_input.replace("mouse automation request ", "", 1).strip()
        return mouse_automation_request(details)

    # ========================================================
    # Phase 199
    # ========================================================

    if text.startswith("app launcher request "):
        app_name = user_input.replace("app launcher request ", "", 1).strip()
        return app_launcher_request(app_name)

    # ========================================================
    # Phase 200
    # ========================================================

    if text.startswith("confirm desktop action "):
        action_id = user_input.replace("confirm desktop action ", "", 1).strip()
        return confirm_desktop_action(action_id)

    if text in ["list desktop actions", "desktop actions"]:
        return list_desktop_actions()

    return None
