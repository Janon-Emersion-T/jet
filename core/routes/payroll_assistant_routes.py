from tools.payroll_assistant_tools import payroll_assistant


def handle_payroll_assistant_routes(user_input: str, text: str, clean_text: str):
    if text in ["payroll assistant", "analyze payroll", "payroll inspection"]:
        return payroll_assistant()

    if text in ["346 help", "phase 346 help", "payroll help"]:
        return """PAYROLL ASSISTANT COMMANDS — PHASE 346

346. payroll assistant
     analyze payroll
     payroll inspection
"""

    return None
