import string

from core.capabilities import list_capabilities, capability_status
from tools.system_tools import run_safe_command
from tools.browser_automation import open_and_read, google_search
from tools.browser_tools import open_safe_site

def handle_greeting(clean_text: str):
    greetings = {
        "hi",
        "hello",
        "hey",
        "hai",
        "yo",
        "good morning",
        "good afternoon",
        "good evening",
    }

    if clean_text in greetings:
        return (
            "Hello Janon. I am online and ready. "
            "You can ask me to build, check, fix, analyze, or plan something."
        )

    if clean_text in ["how are you", "how are you doing", "how is your day"]:
        return (
            "I am functioning properly, Janon. "
            "Systems are ready, routing is active, and I am waiting for your next instruction."
        )

    if clean_text in ["thanks", "thank you", "ok", "okay"]:
        return "Understood, Janon."

    return None

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

    return None

def handle_basic_routes(user_input: str, text: str, clean_text: str, intent: str):
    greeting_response = handle_greeting(clean_text)
    if greeting_response:
        return greeting_response
    
    integration_response = handle_unconnected_integrations(clean_text, intent)
    if integration_response:
        return integration_response
        
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
        if text.startswith("browser ") or text.startswith("google results ") or text.startswith("serp check ") or text.startswith("confirm browser action "):
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

    return None
