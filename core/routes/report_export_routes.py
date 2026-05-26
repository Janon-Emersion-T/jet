from tools.report_export_tools import export_project_health_pdf


def handle_report_export_routes(user_input: str, text: str, clean_text: str):
    if text in ["pdf report exporter", "export pdf report", "export project health pdf"]:
        return export_project_health_pdf()

    if text in ["338 help", "phase 338 help", "report export help"]:
        return """REPORT EXPORT COMMANDS — PHASE 338

338. export project health pdf
"""

    return None
