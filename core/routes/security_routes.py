from tools.security_response_tools import (
    incident_response_assistant,
    report_security_incident,
)
from tools.security_scanner_tools import security_vulnerability_scanner
from tools.owasp_analyzer_tools import owasp_analyzer
from tools.xss_risk_tools import xss_risk_detector
from tools.csrf_analyzer_tools import csrf_analyzer
from tools.sql_injection_risk_tools import sql_injection_risk_detector
from tools.auth_bypass_tools import auth_bypass_analyzer
from tools.file_upload_security_tools import file_upload_security_checker
from tools.api_token_leak_tools import api_token_leak_detector
from tools.secret_scanner_tools import secret_scanner
from tools.ssh_configuration_tools import ssh_configuration_checker
from tools.firewall_assistant_tools import firewall_assistant


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

    if text in ["sql injection risk detector", "scan sql injection risks", "check sql injection", "sql injection scan"]:
        return sql_injection_risk_detector()

    if text in ["358 help", "phase 358 help", "sql injection help"]:
        return (
            "SQL INJECTION RISK DETECTOR COMMANDS - PHASE 358\n\n"
            "sql injection risk detector\n"
            "scan sql injection risks\n"
            "check sql injection"
        )

    if text in ["auth bypass analyzer", "scan auth bypass risks", "check auth bypass", "auth bypass scan"]:
        return auth_bypass_analyzer()

    if text in ["359 help", "phase 359 help", "auth bypass help"]:
        return (
            "AUTH BYPASS ANALYZER COMMANDS - PHASE 359\n\n"
            "auth bypass analyzer\n"
            "scan auth bypass risks\n"
            "check auth bypass"
        )

    if text in ["file upload security checker", "scan file upload risks", "check file uploads", "upload security scan"]:
        return file_upload_security_checker()

    if text in ["360 help", "phase 360 help", "file upload help"]:
        return (
            "FILE UPLOAD SECURITY CHECKER COMMANDS - PHASE 360\n\n"
            "file upload security checker\n"
            "scan file upload risks\n"
            "check file uploads"
        )

    if text in ["api token leak detector", "scan api token leaks", "check token leaks", "token leak scan"]:
        return api_token_leak_detector()

    if text in ["361 help", "phase 361 help", "api token help"]:
        return (
            "API TOKEN LEAK DETECTOR COMMANDS - PHASE 361\n\n"
            "api token leak detector\n"
            "scan api token leaks\n"
            "check token leaks"
        )

    if text in ["secret scanner", "scan secrets", "check secret leaks", "secret scan"]:
        return secret_scanner()

    if text in ["362 help", "phase 362 help", "secret scanner help"]:
        return (
            "SECRET SCANNER COMMANDS - PHASE 362\n\n"
            "secret scanner\n"
            "scan secrets\n"
            "check secret leaks"
        )

    if text in ["ssh configuration checker", "scan ssh configuration", "check ssh config", "ssh hardening scan"]:
        return ssh_configuration_checker()

    if text in ["363 help", "phase 363 help", "ssh config help"]:
        return (
            "SSH CONFIGURATION CHECKER COMMANDS - PHASE 363\n\n"
            "ssh configuration checker\n"
            "scan ssh configuration\n"
            "check ssh config"
        )

    if text in ["firewall assistant", "scan firewall configuration", "check firewall rules", "firewall security scan"]:
        return firewall_assistant()

    if text in ["364 help", "phase 364 help", "firewall help"]:
        return (
            "FIREWALL ASSISTANT COMMANDS - PHASE 364\n\n"
            "firewall assistant\n"
            "scan firewall configuration\n"
            "check firewall rules"
        )

    return None
