from tools.bug_severity_tools import bug_severity_classifier


def handle_bug_severity_routes(user_input: str, text: str, clean_text: str):
    if text in [
        "bug severity classifier",
        "classify bug severity",
        "bug severity scan",
        "analyze bug severity",
        "severity classifier",
    ]:
        return bug_severity_classifier()

    if text in ["352 help", "phase 352 help", "bug severity help"]:
        return """BUG SEVERITY CLASSIFIER COMMANDS — PHASE 352

352. bug severity classifier
     classify bug severity
     bug severity scan
     analyze bug severity
     severity classifier
"""

    return None
