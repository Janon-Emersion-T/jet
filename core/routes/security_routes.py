from tools.security_response_tools import (
    incident_response_assistant,
    report_security_incident,
)
from tools.security_scanner_tools import security_vulnerability_scanner
from tools.owasp_analyzer_tools import owasp_analyzer
from tools.xss_risk_tools import xss_risk_detector
from tools.csrf_analyzer_tools import csrf_analyzer


def _after(user_input: str, prefix: str) -> str:
    return user_input[len(prefix):].strip()


def handle_security_routes(user_input: str, text: str, clean_text: str):
    if text in ["incident response assistant", "incident response", "security incident help", "353 help"]:
        return incident_response_assistant()

    for prefix in ["incident response for ", "help me respond to ", "assess security incident "]:
        if text.startswith(prefix):
            return incident_response_assistant(_after(user_input, prefix))

    for prefix in ["report security incident ", "escalate security incident "]:
        if text.startswith(prefix):
            return report_security_incident(_after(user_input, prefix))

    if text in [
        "security vulnerability scanner",
        "scan security vulnerabilities",
        "security vulnerability scan",
        "find security vulnerabilities",
    ]:
        return security_vulnerability_scanner()

    if text in ["354 help", "phase 354 help", "security scanner help"]:
        return (
            "SECURITY VULNERABILITY SCANNER COMMANDS - PHASE 354\n\n"
            "security vulnerability scanner\n"
            "scan security vulnerabilities\n"
            "find security vulnerabilities"
        )

    if text in ["owasp analyzer", "owasp scan", "check owasp risks", "analyze owasp"]:
        return owasp_analyzer()

    if text in ["355 help", "phase 355 help", "owasp help"]:
        return (
            "OWASP ANALYZER COMMANDS - PHASE 355\n\n"
            "owasp analyzer\n"
            "owasp scan\n"
            "check owasp risks"
        )

    if text in ["xss risk detector", "scan xss risks", "check xss", "xss scan"]:
        return xss_risk_detector()

    if text in ["356 help", "phase 356 help", "xss help"]:
        return (
            "XSS RISK DETECTOR COMMANDS - PHASE 356\n\n"
            "xss risk detector\n"
            "scan xss risks\n"
            "check xss"
        )

    if text in ["csrf analyzer", "scan csrf risks", "check csrf", "csrf scan"]:
        return csrf_analyzer()

    if text in ["357 help", "phase 357 help", "csrf help"]:
        return (
            "CSRF ANALYZER COMMANDS - PHASE 357\n\n"
            "csrf analyzer\n"
            "scan csrf risks\n"
            "check csrf"
        )

    return None
