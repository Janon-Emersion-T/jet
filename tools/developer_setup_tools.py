import re
import shutil
import subprocess
from pathlib import Path

from tools.project_context_tools import set_current_project

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


def infer_developer_setup_action(user_input: str, chat_context: str | None = None) -> dict:
    text = _normalize(user_input).lower()
    context = _normalize(chat_context or "").lower()
    combined = f"{text}\n{context}"

    laravel_match = re.search(
        r"(?:install|create|setup|set up|make).{0,40}\blaravel\b",
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

    return {"action": "unknown"}
