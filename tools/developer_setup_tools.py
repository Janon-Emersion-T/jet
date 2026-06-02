import re
import shutil
import subprocess
import json
from pathlib import Path

from tools.project_context_tools import set_current_project, get_current_project_path

MAX_OUTPUT = 12000
SAFE_BASE_DIRS = [
    Path("/var/www"),
    Path.home() / "Projects",
    Path.home() / "Desktop",
    Path.home() / "Documents",
]


def _normalize(text: str) -> str:
    return " ".join((text or "").strip().split())


def _inside_safe_base(path: Path) -> bool:
    resolved = path.resolve()
    for base in SAFE_BASE_DIRS:
        try:
            resolved.relative_to(base.resolve())
            return True
        except ValueError:
            continue
    return False


def _validate_target_dir(target_dir: str) -> tuple[Path | None, str | None]:
    if not target_dir:
        return None, "Target directory is required."

    path = Path(target_dir).expanduser().resolve()
    if not _inside_safe_base(path):
        allowed = ", ".join(str(item) for item in SAFE_BASE_DIRS)
        return None, f"Blocked target path. Allowed base folders: {allowed}"

    if path.exists() and path.is_file():
        return None, "Target path points to a file, not a directory."

    if path.exists() and any(path.iterdir()):
        return None, "Target directory already exists and is not empty."

    return path, None


def _run(command: list[str], cwd: Path, timeout: int = 1800) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            command,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError:
        return False, f"Command not found: {command[0]}"
    except Exception as exc:
        return False, f"Command failed: {exc}"

    output = (result.stdout.strip() or result.stderr.strip() or "No output.")[:MAX_OUTPUT]
    return result.returncode == 0, output


def install_laravel_project(target_dir: str, company_name: str | None = None) -> str:
    path, error = _validate_target_dir(target_dir)
    if error:
        return error

    if shutil.which("composer") is None:
        return "Composer is not installed or not available in PATH."

    parent = path.parent
    parent.mkdir(parents=True, exist_ok=True)

    ok, output = _run(
        ["composer", "create-project", "laravel/laravel", path.name],
        cwd=parent,
        timeout=3600,
    )

    if not ok:
        return (
            "LARAVEL INSTALL FAILED\n"
            f"Target: {path}\n\n"
            f"{output}"
        )

    set_current_project(str(path))

    lines = [
        "LARAVEL PROJECT CREATED",
        f"Target: {path}",
        "Framework: Laravel",
    ]

    if company_name:
        lines.append(f"Company: {company_name}")

    lines.extend([
        "",
        "Current project context was updated automatically.",
        "",
        output,
    ])
    return "\n".join(lines)


def _project_dir_from_hint(target_dir: str | None = None) -> tuple[Path | None, str | None]:
    if target_dir:
        path = Path(target_dir).expanduser().resolve()
    else:
        current = get_current_project_path()
        if not current:
            return None, "No current project selected. Use a path or set the project context first."
        path = Path(current).resolve()

    if not path.exists() or not path.is_dir():
        return None, "Project directory not found."

    if not _inside_safe_base(path):
        allowed = ", ".join(str(item) for item in SAFE_BASE_DIRS)
        return None, f"Blocked project path. Allowed base folders: {allowed}"

    return path, None


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def install_tailwind_for_project(target_dir: str | None = None) -> str:
    project_dir, error = _project_dir_from_hint(target_dir)
    if error:
        return error

    package_json = project_dir / "package.json"
    if not package_json.exists():
        return "package.json not found in the target project."

    data = _read_json(package_json)
    dev_dependencies = data.get("devDependencies", {})
    dependencies = data.get("dependencies", {})
    all_dependencies = {**dependencies, **dev_dependencies}

    already_has_tailwind = "tailwindcss" in all_dependencies
    already_has_vite_plugin = "@tailwindcss/vite" in all_dependencies

    vite_config = project_dir / "vite.config.js"
    app_css = project_dir / "resources" / "css" / "app.css"
    node_modules = project_dir / "node_modules"

    commands_run: list[str] = []

    if not already_has_tailwind or not already_has_vite_plugin:
        ok, output = _run(
            ["npm", "install", "-D", "tailwindcss", "@tailwindcss/vite"],
            cwd=project_dir,
            timeout=1800,
        )
        commands_run.append("npm install -D tailwindcss @tailwindcss/vite")
        if not ok:
            return (
                "TAILWIND INSTALL FAILED\n"
                f"Project: {project_dir}\n\n"
                f"{output}"
            )

    elif not node_modules.exists():
        ok, output = _run(["npm", "install"], cwd=project_dir, timeout=1800)
        commands_run.append("npm install")
        if not ok:
            return (
                "PROJECT DEPENDENCY INSTALL FAILED\n"
                f"Project: {project_dir}\n\n"
                f"{output}"
            )

    notes: list[str] = []

    if vite_config.exists():
        vite_content = vite_config.read_text(encoding="utf-8", errors="replace")
        if "@tailwindcss/vite" in vite_content and "tailwindcss()" in vite_content:
            notes.append("Vite Tailwind plugin already configured.")
        else:
            notes.append("Tailwind package installed, but vite.config.js still needs Tailwind plugin wiring.")
    else:
        notes.append("vite.config.js not found. Tailwind install completed without Vite wiring.")

    if app_css.exists():
        css_content = app_css.read_text(encoding="utf-8", errors="replace")
        if "@import 'tailwindcss';" in css_content or '@import "tailwindcss";' in css_content:
            notes.append("App CSS already imports Tailwind.")
        else:
            app_css.write_text("@import 'tailwindcss';\n\n" + css_content, encoding="utf-8")
            notes.append("Added Tailwind import to resources/css/app.css.")
    else:
        notes.append("resources/css/app.css not found.")

    ok, build_output = _run(["npm", "run", "build"], cwd=project_dir, timeout=1800)
    commands_run.append("npm run build")
    if not ok:
        return (
            "TAILWIND SETUP PARTIALLY COMPLETE\n"
            f"Project: {project_dir}\n"
            + ("\n".join(f"- {note}" for note in notes) if notes else "")
            + "\n\nBuild verification failed:\n"
            + build_output
        )

    set_current_project(str(project_dir))

    lines = [
        "TAILWIND SETUP COMPLETE",
        f"Project: {project_dir}",
        f"Tailwind dependency present: {'YES' if already_has_tailwind else 'ADDED'}",
        f"Tailwind Vite plugin present: {'YES' if already_has_vite_plugin else 'ADDED'}",
        "",
        "Checks:",
    ]
    lines.extend(f"- {note}" for note in notes)
    lines.append("")
    lines.append("Commands executed:")
    lines.extend(f"- {command}" for command in commands_run)
    lines.append("")
    lines.append(build_output)
    return "\n".join(lines)


def infer_developer_setup_action(user_input: str, chat_context: str | None = None) -> dict:
    text = _normalize(user_input).lower()
    context = _normalize(chat_context or "").lower()
    combined = f"{text}\n{context}"
    current_project = get_current_project_path()

    laravel_match = re.search(
        r"(?:install|create|setup|set up|make).{0,40}\blaravel\b",
        combined,
        flags=re.I | re.S,
    )
    tailwind_match = re.search(
        r"(?:install|setup|set up|configure|add).{0,40}\btailwind\b",
        combined,
        flags=re.I | re.S,
    )
    explicit_path_match = re.search(
        r"(/var/www/[a-zA-Z0-9._-]+|~/[a-zA-Z0-9_./-]+)",
        combined,
    )
    base_www_match = re.search(r"/var/www/?", combined)
    folder_name_match = re.search(
        r"folder named\s+([a-zA-Z0-9._-]+)|named\s+([a-zA-Z0-9._-]+)\s+and install laravel",
        combined,
        flags=re.I,
    )

    company_match = re.search(
        r'company name\s+"([^"]+)"|company name\s+\'([^\']+)\'',
        combined,
        flags=re.I,
    )
    company_name = None
    if company_match:
        company_name = next((group for group in company_match.groups() if group), None)

    target_dir = explicit_path_match.group(1) if explicit_path_match else None

    if not target_dir and base_www_match and folder_name_match:
        folder_name = next((group for group in folder_name_match.groups() if group), None)
        if folder_name:
            target_dir = f"/var/www/{folder_name}"

    if laravel_match and target_dir:
        return {
            "action": "install_laravel",
            "target_dir": target_dir,
            "company_name": company_name,
        }

    if tailwind_match:
        if target_dir:
            return {
                "action": "install_tailwind",
                "target_dir": target_dir,
            }
        if "same project" in combined or "current project" in combined or current_project:
            return {
                "action": "install_tailwind",
                "target_dir": str(current_project) if current_project else None,
            }

    return {"action": "unknown"}
