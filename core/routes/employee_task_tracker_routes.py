from tools.employee_task_tracker_tools import employee_task_tracker


def handle_employee_task_tracker_routes(user_input: str, text: str, clean_text: str):
    if text in ["employee task tracker", "task tracker", "analyze employee tasks", "staff task tracker"]:
        return employee_task_tracker()

    if text in ["348 help", "phase 348 help", "employee task help", "task tracker help"]:
        return """EMPLOYEE TASK TRACKER COMMANDS — PHASE 348

348. employee task tracker
     task tracker
     analyze employee tasks
     staff task tracker
"""

    return None
