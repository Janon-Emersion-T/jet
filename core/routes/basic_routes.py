import string

from core.capabilities import list_capabilities, capability_status
from tools.system_tools import run_safe_command
from tools.browser_automation import open_and_read, google_search
from tools.browser_tools import open_safe_site


def handle_basic_routes(user_input: str, text: str, clean_text: str, intent: str):
    if clean_text in [
        "capabilities",
        "list capabilities",
        "what can you do"
    ]:
        return list_capabilities()

    if clean_text.startswith("capability "):
        capability = clean_text.replace("capability ", "", 1).strip()
        return capability_status(capability)

    if intent == "weather":
        return (
            "Live weather is not connected yet. "
            "I cannot check real-time weather until a weather tool or API is added."
        )

    if intent == "location":
        return (
            "Live location detection is not connected yet. "
            "I can remember your saved country if you told me, "
            "but I cannot detect your current GPS/location automatically."
        )

    if intent == "camera":
        return (
            "Camera access is not connected yet. "
            "I cannot see or scan the environment until a camera module is added."
        )

    if intent == "email":
        return (
            "Email access is not connected yet. "
            "I cannot read or send emails until an email connector is added."
        )

    if intent == "calendar":
        return (
            "Calendar access is not connected yet. "
            "I cannot manage schedules until a calendar connector is added."
        )

    if clean_text.startswith("search google for "):
        query = user_input.lower().replace("search google for ", "", 1).strip()
        return google_search(query)

    if clean_text.startswith("open "):
        site = clean_text.replace("open ", "", 1).strip()

        known_sites = {
            "google": "https://google.com",
            "youtube": "https://youtube.com",
            "github": "https://github.com",
            "chatgpt": "https://chatgpt.com",
            "gmail": "https://gmail.com",
            "lkprofessionals": "https://lkprofessionals.com"
        }

        if site in known_sites:
            return open_and_read(known_sites[site])

        return open_safe_site(site)

    if intent == "browser_control":
        return (
            "Browser launcher is active. "
            "Say: open google, open youtube, open github, open gmail, "
            "open chatgpt, or open lkprofessionals."
        )

    command_map = {
        "show current folder": "pwd",
        "where am i": "pwd",
        "list files": "ls",
        "show files": "ls",
        "show disk usage": "disk",
        "show memory usage": "memory",
        "show date": "date",
        "who am i": "whoami",
        "python version": "python version",
        "node version": "node version",
        "npm version": "npm version",
        "git version": "git version",
    }

    if clean_text in command_map:
        return run_safe_command(command_map[clean_text])

    return None
