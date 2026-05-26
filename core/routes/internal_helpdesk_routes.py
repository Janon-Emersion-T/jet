from tools.internal_helpdesk_tools import internal_helpdesk_system


def handle_internal_helpdesk_routes(user_input: str, text: str, clean_text: str):
    if text in ["internal helpdesk system", "helpdesk system", "helpdesk assistant", "analyze helpdesk"]:
        return internal_helpdesk_system()

    if text in ["350 help", "phase 350 help", "helpdesk help"]:
        return """INTERNAL HELPDESK SYSTEM COMMANDS — PHASE 350

350. internal helpdesk system
     helpdesk system
     helpdesk assistant
     analyze helpdesk
"""

    return None
