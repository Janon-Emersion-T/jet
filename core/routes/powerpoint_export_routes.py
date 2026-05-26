from tools.powerpoint_export_tools import generate_project_health_powerpoint


def handle_powerpoint_export_routes(user_input: str, text: str, clean_text: str):
    if text in ["powerpoint generator", "generate powerpoint", "export powerpoint", "export project health powerpoint"]:
        return generate_project_health_powerpoint()

    if text in ["339 help", "phase 339 help", "powerpoint export help"]:
        return """POWERPOINT EXPORT COMMANDS — PHASE 339

339. export project health powerpoint
"""

    return None
