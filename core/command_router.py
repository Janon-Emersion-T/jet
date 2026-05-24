from core.patch_applier import apply_proposal
from core.file_writer import parse_write_command
from core.patch_proposer import propose_patch
from core.brain import ask_brain
from core.file_writer import parse_write_command
from core.memory import save_fact
from core.memory_search import (
    search_memory,
    get_relevant_memory,
    list_facts
)

from tools.browser_automation import open_and_read, google_search

from tools.system_tools import (
    run_safe_command,
    list_projects,
    inspect_folder,
    detect_project_stack,
    scan_project_files,
    read_project_file,
)

from core.capabilities import (
    list_capabilities,
    capability_status
)

from core.code_reviewer import review_code_file

from core.project_diagnostics import run_project_diagnostics, interpret_project_diagnostics

from core.intent_classifier import classify_intent

from tools.browser_tools import open_safe_site

import string


def route_command(user_input: str) -> str:

    text = user_input.lower().strip()

    clean_text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    intent = classify_intent(user_input)

    # =========================
    # CAPABILITIES
    # =========================

    if clean_text in [
        "capabilities",
        "list capabilities",
        "what can you do"
    ]:
        return list_capabilities()

    if clean_text.startswith("capability "):
        capability = clean_text.replace(
            "capability ",
            "",
            1
        ).strip()

        return capability_status(capability)

    # =========================
    # LIVE TOOL STATUS
    # =========================

    if intent == "weather":
        return (
            "Live weather is not connected yet. "
            "I cannot check real-time weather until "
            "a weather tool or API is added."
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
            "I cannot see or scan the environment "
            "until a camera module is added."
        )

    if intent == "email":
        return (
            "Email access is not connected yet. "
            "I cannot read or send emails "
            "until an email connector is added."
        )

    if intent == "calendar":
        return (
            "Calendar access is not connected yet. "
            "I cannot manage schedules "
            "until a calendar connector is added."
        )

    # =========================
    # BROWSER LAUNCHER
    # =========================

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
            "Say: open google, open youtube, "
            "open github, open gmail, "
            "open chatgpt, or open lkprofessionals."
        )

    # =========================
    # SAFE SYSTEM COMMANDS
    # =========================

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
        return run_safe_command(
            command_map[clean_text]
        )

    # =========================
    # PROJECTS
    # =========================

    if clean_text in [
        "list projects",
        "show projects",
        "find projects"
    ]:
        return list_projects()

    if clean_text.startswith("inspect folder "):

        folder = user_input.replace(
            "inspect folder ",
            "",
            1
        ).strip()

        return inspect_folder(folder)

    # =========================
    # MEMORY
    # =========================

    if clean_text.startswith("remember that "):

        fact = user_input.replace(
            "remember that ",
            "",
            1
        ).strip()

        return save_fact(fact)

    if clean_text in [
        "list facts",
        "show facts",
        "what do you remember"
    ]:
        return list_facts()

    if clean_text.startswith("search memory "):

        query = user_input.replace(
            "search memory ",
            "",
            1
        ).strip()

        return search_memory(query)

    # =========================
    # AI FALLBACK
    # =========================

    if text.startswith("apply proposal "):
        proposal_path = user_input.replace("apply proposal ", "", 1).strip()
        return apply_proposal(proposal_path)

    if text.startswith("propose patch "):
        command = user_input.replace("propose patch ", "", 1).strip()

        if ":::" not in command:
            return "Invalid format. Use: propose patch /path/to/file.py ::: instruction"

        target_file, instruction = command.split(":::", 1)

        return propose_patch(target_file.strip(), instruction.strip())

    if text.startswith("read file "):
        file_path = user_input.replace("read file ", "", 1).strip()
        return read_project_file(file_path)
    
    if text.startswith("review file "):
        file_path = user_input.replace("review file ", "", 1).strip()
        return review_code_file(file_path)
    
    if text.startswith("deep check "):
        folder = user_input.replace("deep check ", "", 1).strip()

        shortcuts = {
            "jarvis": "~/Projects/downloads/Jarvis",
            "current": ".",
        }

        folder = shortcuts.get(folder.lower(), folder)

        return run_project_diagnostics(folder)
    
    if text.startswith("analyze project "):
        folder = user_input.replace("analyze project ", "", 1).strip()

        shortcuts = {
            "jarvis": "~/Projects/downloads/Jarvis",
            "current": ".",
        }

        folder = shortcuts.get(folder.lower(), folder)

        return interpret_project_diagnostics(folder)
    
    if text.startswith("write file "):
        return parse_write_command(user_input)

    if text.startswith("detect stack "):
        folder = user_input.replace("detect stack ", "", 1).strip()
        return detect_project_stack(folder)

    if text.startswith("scan project "):
        folder = user_input.replace("scan project ", "", 1).strip()
        return scan_project_files(folder)

    relevant_memory = get_relevant_memory(
        user_input
    )

    prompt = f"""
You are JARVIS, Janon's private local AI assistant.

Relevant previous memory:
{relevant_memory if relevant_memory else "No relevant memory found."}

Rules:
- Use relevant memory only when it helps.
- Do not invent memories.
- Be direct, practical, and execution-focused.
- Never pretend to have sensors, GPS, cameras, weather feeds, internet access, or real-world awareness unless tools actually provide that data.
- If live data is needed, clearly say the required tool is not connected yet.
- If a command cannot be executed, explain why honestly.

User request:
{user_input}
"""

    return ask_brain(prompt)