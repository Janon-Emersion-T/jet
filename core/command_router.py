from tools.project_analyzers import (
    summarize_project_structure,
    analyze_laravel_project,
    analyze_react_project,
    analyze_python_project,
    analyze_electron_project,
)
from tools.project_context_tools import (
    register_project_shortcut,
    list_project_shortcuts,
    list_recent_projects,
    set_current_project,
    show_current_project_context,
    auto_detect_active_project,
    read_multiple_files_safely,
)

from core.patches.safe_writer import SafeWriter
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

    # =========================
    # PHASES 26-30: PROJECT ANALYZERS
    # =========================

    if text in ["summarize project", "project structure", "summarize project structure"]:
        return summarize_project_structure()

    if text in ["analyze laravel", "laravel analyzer", "analyze laravel project"]:
        return analyze_laravel_project()

    if text in ["analyze react", "react analyzer", "analyze react project"]:
        return analyze_react_project()

    if text in ["analyze python", "python analyzer", "analyze python project"]:
        return analyze_python_project()

    if text in ["analyze electron", "electron analyzer", "analyze electron project"]:
        return analyze_electron_project()

        # =========================
    # PHASES 21-25: PROJECT CONTEXT SYSTEM
    # =========================

    if text.startswith("register project "):
        command = user_input.replace("register project ", "", 1).strip()

        if ":::" not in command:
            return "Invalid format. Use: register project name ::: /path/to/project"

        name, path = command.split(":::", 1)
        return register_project_shortcut(name.strip(), path.strip())

    if text in ["project shortcuts", "list project shortcuts", "show project shortcuts"]:
        return list_project_shortcuts()

    if text.startswith("use project "):
        project = user_input.replace("use project ", "", 1).strip()
        return set_current_project(project)

    if text in ["recent projects", "show recent projects", "list recent projects"]:
        return list_recent_projects()

    if text in ["current project", "show current project", "project context"]:
        return show_current_project_context()

    if text in ["auto project", "detect active project", "auto detect project"]:
        return auto_detect_active_project()

    if text.startswith("read files "):
        files_text = user_input.replace("read files ", "", 1).strip()
        return read_multiple_files_safely(files_text)

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
    
        # =========================
    # PHASES 17-20: SAFE PATCH WORKFLOW
    # =========================

    if text in ["list proposals", "show proposals"]:
        writer = SafeWriter(root=".")
        proposals = writer.list_proposals()

        if not proposals:
            return "No proposals found."

        lines = ["Stored proposals:"]
        for p in proposals:
            status = "rolled_back" if p.get("rolled_back") else "applied" if p.get("applied") else "pending"
            lines.append(
                f"- {p['id']} | {status} | {p['file_path']} | {p.get('reason', 'No reason')}"
            )

        return "\n".join(lines)

    if text.startswith("diff proposal "):
        proposal_id = user_input.replace("diff proposal ", "", 1).strip()
        writer = SafeWriter(root=".")
        return writer.diff_proposal(proposal_id)

    if text.startswith("compare proposal "):
        proposal_id = user_input.replace("compare proposal ", "", 1).strip()
        writer = SafeWriter(root=".")
        comparison = writer.compare_proposal(proposal_id)

        if isinstance(comparison, dict) and comparison.get("error"):
            return comparison["message"]

        return (
            "PATCH COMPARISON MODE\n\n"
            "===== OLD FILE =====\n"
            f"{comparison['old']}\n\n"
            "===== NEW FILE =====\n"
            f"{comparison['new']}\n\n"
            "===== DIFF =====\n"
            f"{comparison['diff']}"
        )

    if text.startswith("apply proposal "):
        proposal_id = user_input.replace("apply proposal ", "", 1).strip()
        writer = SafeWriter(root=".")
        return writer.apply_proposal(proposal_id, confirm=False)

    if text.startswith("confirm apply proposal "):
        proposal_id = user_input.replace("confirm apply proposal ", "", 1).strip()
        writer = SafeWriter(root=".")
        return writer.apply_proposal(proposal_id, confirm=True)

    if text.startswith("rollback proposal "):
        proposal_id = user_input.replace("rollback proposal ", "", 1).strip()
        writer = SafeWriter(root=".")
        return writer.rollback_proposal(proposal_id)

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