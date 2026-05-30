from core.basic_conversation import handle_basic_conversation
from core.capabilities import list_capabilities, capability_status

from tools.system_tools import run_safe_command
from tools.browser_automation import open_and_read, google_search
from tools.browser_tools import open_safe_site

from tools.weather_location_tools import (
    extract_weather_city,
    format_saved_location,
    get_weather_for_city,
    get_weather_for_saved_location,
)


def handle_unconnected_integrations(clean_text: str, intent: str):
    calendar_terms = {
        "calendar",
        "calender",
        "my calendar",
        "my calender",
        "open calendar",
        "open calender",
        "show calendar",
        "show calender",
        "today calendar",
        "today calender",
        "schedule",
        "my schedule",
        "today schedule",
        "show my schedule",
        "what is my schedule",
        "what is on my calendar",
        "what is on my calender",
    }

    email_terms = {
        "email",
        "mail",
        "gmail",
        "inbox",
        "my email",
        "my mail",
        "open email",
        "open gmail",
        "show email",
        "show gmail",
        "read email",
        "read gmail",
        "check email",
        "check gmail",
        "check my email",
        "check my gmail",
    }

    camera_terms = {
        "camera",
        "open camera",
        "see camera",
        "scan camera",
        "look through camera",
    }

    if intent == "calendar" or clean_text in calendar_terms:
        return (
            "Calendar access is not connected yet. "
            "I cannot read, view, create, or manage real calendar events until a calendar connector is added. "
            "I will not invent calendar events."
        )

    if intent == "email" or clean_text in email_terms:
        return (
            "Email access is not connected yet. "
            "I cannot read, send, or manage real emails until an email connector is added. "
            "I will not invent email content."
        )

    if intent == "camera" or clean_text in camera_terms:
        return (
            "Camera access is not connected yet. "
            "I cannot see or scan the environment until a camera module is added."
        )

    return None


def handle_basic_routes(user_input: str, text: str, clean_text: str, intent: str):
    """
    Basic route handler.

    Order matters:
    1. Block fake external-tool access.
    2. Handle real location/weather.
    3. Handle deterministic local commands.
    4. Handle browser launcher commands.
    5. Use dynamic local conversation as the final basic fallback.
    """

    integration_response = handle_unconnected_integrations(clean_text, intent)
    if integration_response:
        return integration_response

    if clean_text in [
        "location",
        "my location",
        "current location",
        "where am i",
        "where am i located",
    ]:
        return format_saved_location()

    weather_city = extract_weather_city(clean_text)
    if weather_city:
        return get_weather_for_city(weather_city)

    if clean_text in [
        "weather",
        "today weather",
        "current weather",
        "weather today",
        "check weather",
        "check the weather",
        "what is the weather",
        "what's the weather",
        "weather here",
        "weather near me",
        "weather for my location",
    ] or intent == "weather":
        return get_weather_for_saved_location()

    if clean_text in [
        "capabilities",
        "list capabilities",
        "what can you do",
        "what are your capabilities",
        "show capabilities",
    ]:
        return list_capabilities()

    if clean_text.startswith("capability "):
        capability = clean_text.replace("capability ", "", 1).strip()
        return capability_status(capability)

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
            "lkprofessionals": "https://lkprofessionals.com",
        }

        if site in known_sites:
            return open_and_read(known_sites[site])

        return open_safe_site(site)

    if intent == "browser_control":
        if (
            text.startswith("browser ")
            or text.startswith("google results ")
            or text.startswith("serp check ")
            or text.startswith("confirm browser action ")
        ):
            return None

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

    return handle_basic_conversation(user_input)