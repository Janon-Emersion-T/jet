from tools.financial_report_tools import financial_report_assistant


def handle_financial_report_routes(user_input: str, text: str, clean_text: str):
    if text in ["financial report assistant", "finance report assistant", "analyze financial report"]:
        return financial_report_assistant()

    if text in ["341 help", "phase 341 help", "financial report help"]:
        return """FINANCIAL REPORT COMMANDS — PHASE 341

341. financial report assistant
"""

    return None
