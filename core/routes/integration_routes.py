from tools.integration_tools import (
    calendar_integration_help,
    gmail_integration_help,
    contact_integration_help,
    whatsapp_draft_assistant,
    integration_help,
)


def handle_integration_routes(user_input: str, text: str, clean_text: str):
    if text in ["integration help", "calendar gmail contact help"]:
        return integration_help()

    if text in ["calendar integration status", "calendar integration"]:
        return calendar_integration_help()

    if text in ["gmail integration status", "gmail integration"]:
        return gmail_integration_help()

    if text in ["contact integration status", "contact integration"]:
        return contact_integration_help()

    if text.startswith("whatsapp draft for "):
        request = user_input.replace("whatsapp draft for ", "", 1).strip()
        return whatsapp_draft_assistant(request)

    return None
