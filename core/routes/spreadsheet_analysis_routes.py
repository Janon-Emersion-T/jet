from tools.spreadsheet_analysis_tools import spreadsheet_analysis_engine


def handle_spreadsheet_analysis_routes(user_input: str, text: str, clean_text: str):
    if text in ["spreadsheet analysis engine", "analyze spreadsheets", "spreadsheet analyzer"]:
        return spreadsheet_analysis_engine()

    if text in ["340 help", "phase 340 help", "spreadsheet analysis help"]:
        return """SPREADSHEET ANALYSIS COMMANDS — PHASE 340

340. spreadsheet analysis engine
"""

    return None
