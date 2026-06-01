import requests
from typing import Dict, List, Any

from core.channels.social_channel_config import get_social_channel


def extract_whatsapp_text_messages(payload: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Extract text messages from WhatsApp Business Cloud API webhook payload.
    """

    messages_found = []

    entries = payload.get("entry", [])

    for entry in entries:
        changes = entry.get("changes", [])

        for change in changes:
            value = change.get("value", {})
            messages = value.get("messages", [])

            for message in messages:
                if message.get("type") != "text":
                    continue

                from_number = message.get("from", "")
                message_id = message.get("id", "")
                text_body = message.get("text", {}).get("body", "").strip()

                if not from_number or not text_body:
                    continue

                messages_found.append({
                    "from": from_number,
                    "message_id": message_id,
                    "text": text_body,
                })

    return messages_found


def send_whatsapp_message(to_number: str, message: str) -> Dict[str, Any]:
    """
    Send WhatsApp text message using Meta WhatsApp Business Cloud API.
    """

    config = get_social_channel("whatsapp")

    access_token = config.get("access_token", "")
    phone_number_id = config.get("phone_number_id", "")
    api_version = config.get("api_version", "v20.0")

    if not config.get("enabled"):
        return {
            "ok": False,
            "error": "WhatsApp channel is disabled.",
        }

    if not access_token:
        return {
            "ok": False,
            "error": "WhatsApp access token is missing.",
        }

    if not phone_number_id:
        return {
            "ok": False,
            "error": "WhatsApp phone number ID is missing.",
        }

    url = f"https://graph.facebook.com/{api_version}/{phone_number_id}/messages"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": message[:4000],
        },
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=20,
        )

        try:
            data = response.json()
        except ValueError:
            data = {"raw": response.text}

        return {
            "ok": response.ok,
            "status_code": response.status_code,
            "data": data,
        }

    except requests.RequestException as error:
        return {
            "ok": False,
            "error": str(error),
        }
