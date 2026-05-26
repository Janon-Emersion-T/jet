from tools.accounting_anomaly_tools import accounting_anomaly_detector


def handle_accounting_anomaly_routes(user_input: str, text: str, clean_text: str):
    if text in ["accounting anomaly detector", "detect accounting anomalies", "accounting anomalies"]:
        return accounting_anomaly_detector()

    if text in ["342 help", "phase 342 help", "accounting anomaly help"]:
        return """ACCOUNTING ANOMALY COMMANDS — PHASE 342

342. accounting anomaly detector
"""

    return None
