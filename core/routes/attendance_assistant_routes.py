from tools.attendance_assistant_tools import attendance_assistant


def handle_attendance_assistant_routes(user_input: str, text: str, clean_text: str):
    if text in ["attendance assistant", "analyze attendance", "attendance inspection", "staff attendance"]:
        return attendance_assistant()

    if text in ["349 help", "phase 349 help", "attendance help"]:
        return """ATTENDANCE ASSISTANT COMMANDS — PHASE 349

349. attendance assistant
     analyze attendance
     attendance inspection
     staff attendance
"""

    return None
