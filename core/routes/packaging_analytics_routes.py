from tools.packaging_analytics_tools import (
    windows_installer_generator,
    linux_appimage_assistant,
    mac_packaging_advisor,
    auto_update_system_planner,
    telemetry_framework_advisor,
    crash_logging_framework,
    local_analytics_engine,
    user_behavior_tracker,
    session_replay_assistant,
    microsoft_clarity_assistant,
)


def handle_packaging_analytics_routes(user_input: str, text: str, clean_text: str):
    if text in ["windows installer generator", "windows installer"]:
        return windows_installer_generator()

    if text in ["linux appimage assistant", "appimage assistant", "linux appimage"]:
        return linux_appimage_assistant()

    if text in ["mac packaging advisor", "mac packaging", "macos packaging advisor"]:
        return mac_packaging_advisor()

    if text in ["auto update system planner", "auto-update system planner", "update planner"]:
        return auto_update_system_planner()

    if text in ["telemetry framework advisor", "telemetry advisor"]:
        return telemetry_framework_advisor()

    if text in ["crash logging framework", "crash logger", "crash logging"]:
        return crash_logging_framework()

    if text in ["local analytics engine", "local analytics"]:
        return local_analytics_engine()

    if text in ["user behavior tracker", "behavior tracker"]:
        return user_behavior_tracker()

    if text in ["session replay assistant", "session replay"]:
        return session_replay_assistant()

    if text in ["microsoft clarity assistant", "clarity assistant", "ms clarity assistant"]:
        return microsoft_clarity_assistant()

    if text in ["packaging analytics help", "291 300 help", "phases 291 300"]:
        return """PACKAGING / ANALYTICS COMMANDS — PHASES 291–300

291. windows installer generator
292. linux appimage assistant
293. mac packaging advisor
294. auto update system planner
295. telemetry framework advisor
296. crash logging framework
297. local analytics engine
298. user behavior tracker
299. session replay assistant
300. microsoft clarity assistant"""

    return None
