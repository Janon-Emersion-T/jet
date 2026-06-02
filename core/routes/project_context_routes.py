from tools.system_tools import (
    list_projects,
    inspect_folder,
    detect_project_stack,
    scan_project_files,
    read_project_file,
)

from core.code_reviewer import review_code_file
from core.project_diagnostics import run_project_diagnostics, interpret_project_diagnostics
from core.file_writer import parse_write_command

from tools.project_context_tools import (
    register_project_shortcut,
    list_project_shortcuts,
    list_recent_projects,
    set_current_project,
    show_current_project_context,
    auto_detect_active_project,
    read_multiple_files_safely,
)


def handle_project_context_routes(user_input: str, text: str, clean_text: str):
    if clean_text in [
        "list projects",
        "show projects",
        "find projects"
    ]:
        return list_projects()

    if clean_text.startswith("inspect folder "):
        folder = user_input.replace("inspect folder ", "", 1).strip()
        return inspect_folder(folder)

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

    if text.startswith("create file "):
        return parse_write_command(user_input.replace("create file ", "write file ", 1))

    if text.startswith("update file "):
        return parse_write_command(user_input.replace("update file ", "write file ", 1))

    if text.startswith("edit file "):
        return parse_write_command(user_input.replace("edit file ", "write file ", 1))

    if text.startswith("detect stack "):
        folder = user_input.replace("detect stack ", "", 1).strip()
        return detect_project_stack(folder)

    if text.startswith("scan project "):
        folder = user_input.replace("scan project ", "", 1).strip()
        return scan_project_files(folder)

    return None
