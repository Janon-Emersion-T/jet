from tools.security_response_tools import (
    incident_response_assistant,
    report_security_incident,
)


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

    return None
