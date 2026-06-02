from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from core.brain import ask_brain
from tools.developer_setup_tools import (
    install_laravel_project,
    install_project_dependency,
    install_tailwind_for_project,
)
from tools.project_context_tools import set_current_project, get_current_project_path
from tools.system_tools import write_project_file
from core.patches.proposal_manager import ProposalManager


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


def _extract_json(text: str) -> dict | None:
    if not text:
        return None

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        return None

    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return None


def infer_web_development_action(user_input: str) -> dict:
    """
    Infer the most likely web development action from a natural language request.

    This keeps the web development route responsive even when the user speaks
    naturally instead of using a rigid command format.
    """
    text = _normalize(user_input).lower()

    action = {
        "action": "plan",
        "target_dir": None,
        "request": user_input,
    }

    target = _parse_target(user_input)
    if target:
        action["target_dir"] = str(target)

    if any(term in text for term in ["generate migration", "generate controller", "generate model", "generate view", "generate readme"]):
        action["action"] = "module"
        return action

    if any(term in text for term in ["plan", "roadmap", "break down", "task breakdown", "architecture", "audit", "review", "analyze"]):
        action["action"] = "plan"
        return action

    if any(term in text for term in [
        "create",
        "build",
        "make",
        "scaffold",
        "install laravel",
        "laravel web application",
        "laravel app",
        "web application",
        "web app",
        "saas",
    ]):
        action["action"] = "create"
        return action

    if target and any(term in text for term in ["laravel", "blade", "tailwind", "alpine", "vite", "project"]):
        action["action"] = "create"
        return action

    return action


def _parse_target(user_input: str, chat_context: str | None = None) -> Path | None:
    text = f"{user_input}\n{chat_context or ''}"
    match = re.search(r"(/[^\s`]+|~/[^\s`]+)", text)
    if not match:
        return None
    return Path(match.group(1)).expanduser().resolve()


def _target_exists_and_is_not_empty(path: Path) -> bool:
    return path.exists() and path.is_dir() and any(path.iterdir())


def _safe_write(path: Path, content: str, reason: str) -> str:
    path = path.expanduser().resolve()
    if not _inside_safe_base(path):
        return f"Blocked target path: {path}"

    if path.exists() and path.is_file():
        current_project = get_current_project_path()
        proposal_root = Path(current_project).resolve() if current_project and str(path).startswith(str(current_project)) else path.parent
        manager = ProposalManager(root=str(proposal_root))
        file_path = str(path.relative_to(proposal_root))
        proposal = manager.create_proposal(file_path, content, reason=reason)
        return (
            "WRITE PROPOSAL CREATED\n"
            f"Path: {path}\n"
            f"Proposal: {proposal['id']}\n"
            "Existing work was not overwritten."
        )

    if path.exists() and path.is_dir():
        return f"Blocked. Target path is a directory: {path}"

    return write_project_file(str(path), content)


def _run_checked(command: list[str], cwd: Path, label: str, timeout: int = 1800) -> str:
    result = subprocess.run(
        command,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    output = (result.stdout.strip() or result.stderr.strip() or "No output.")
    if result.returncode != 0:
        raise RuntimeError(f"{label} failed:\n{output}")
    return output


def build_web_development_plan(user_input: str, chat_context: str | None = None) -> dict:
    prompt = f"""
You are Jarvis's web development agent.
Turn the request into a production-grade build plan for a software company project.

Return strict JSON only with this schema:
{{
  "objective": "short summary",
  "target_path": "/absolute/path or null",
  "stack": ["Laravel", "Blade", "Tailwind", "Alpine", "Vite", "MySQL"],
  "project_type": "new_app|existing_app|module|fix|audit|plan",
  "confirmation_needed": true|false,
  "steps": [
    {{
      "step": 1,
      "title": "short title",
      "action": "tool or action name",
      "notes": "what to do",
      "commands": ["optional shell commands"],
      "files": ["optional file paths"]
    }}
  ],
  "risks": ["short risk items"],
  "validation": ["how to verify the result"]
}}

Rules:
- Prefer dynamic, stack-aware steps over canned boilerplate.
- If the request is for a Laravel app, include Breeze, roles/permissions, Blade, Tailwind, Alpine, Vite, README, migrations, controllers, models, views, and tests where relevant.
- Never overwrite existing work without confirmation.
- If the target folder already exists and has files, set confirmation_needed to true.
- Keep the plan realistic and executable.

Chat context:
{chat_context if chat_context else "No active context."}

Request:
{user_input}
"""

    raw = ask_brain(prompt, route_hint="fast", max_tokens=700)
    data = _extract_json(raw) or {}

    target_path = _parse_target(user_input, chat_context)
    if target_path and not data.get("target_path"):
        data["target_path"] = str(target_path)

    data.setdefault("objective", _normalize(user_input))
    data.setdefault("stack", ["Laravel", "Blade", "Tailwind", "Alpine", "Vite", "MySQL"])
    data.setdefault("project_type", "plan")
    data.setdefault("confirmation_needed", False)
    data.setdefault("steps", [])
    data.setdefault("risks", [])
    data.setdefault("validation", [])

    if target_path and _target_exists_and_is_not_empty(target_path):
        data["confirmation_needed"] = True
        data.setdefault("risks", []).append("Target directory already contains work and must not be overwritten without confirmation.")

    return data


def format_web_development_plan(plan: dict) -> str:
    lines = [
        "WEB DEVELOPMENT PLAN",
        f"Objective: {plan.get('objective', 'Unknown')}",
        f"Target: {plan.get('target_path', 'Not specified')}",
        f"Project type: {plan.get('project_type', 'plan')}",
        f"Confirmation needed: {'YES' if plan.get('confirmation_needed') else 'NO'}",
        "",
        "Steps:",
    ]

    for step in plan.get("steps", []):
        lines.append(f"- {step.get('step', '?')}. {step.get('title', 'Untitled')}")
        if step.get("notes"):
            lines.append(f"  Notes: {step['notes']}")
        if step.get("commands"):
            lines.append(f"  Commands: {', '.join(step['commands'])}")
        if step.get("files"):
            lines.append(f"  Files: {', '.join(step['files'])}")

    if plan.get("risks"):
        lines.append("")
        lines.append("Risks:")
        lines.extend(f"- {risk}" for risk in plan["risks"])

    if plan.get("validation"):
        lines.append("")
        lines.append("Validation:")
        lines.extend(f"- {item}" for item in plan["validation"])

    return "\n".join(lines)


def _install_laravel_stack(target_dir: Path) -> str:
    result = install_laravel_project(str(target_dir))
    if "FAILED" in result or "Blocked" in result:
        return result

    set_current_project(str(target_dir))

    notes = [result]

    notes.append(install_project_dependency("laravel/breeze", target_dir=str(target_dir), user_input="composer require laravel/breeze"))
    notes.append(install_project_dependency("spatie/laravel-permission", target_dir=str(target_dir), user_input="composer require spatie/laravel-permission"))

    try:
        notes.append(_run_checked(["php", "artisan", "breeze:install", "blade", "--no-interaction"], target_dir, "Breeze install"))
        notes.append(_run_checked(["npm", "install"], target_dir, "npm install"))
        notes.append(_run_checked(["npm", "run", "build"], target_dir, "npm build"))
    except RuntimeError as exc:
        return (
            "LARAVEL STACK PROVISIONING FAILED\n"
            f"Target: {target_dir}\n\n"
            f"{exc}"
        )

    notes.append(install_tailwind_for_project(str(target_dir)))

    return "\n\n".join(notes)


def _generate_readme(target_dir: Path, objective: str, plan: dict) -> str:
    readme_path = target_dir / "README.md"
    prompt = f"""
Write a production-ready README.md for this Laravel project.

Include:
- Project name
- Description
- Stack
- Key modules
- Install steps
- Environment setup
- Database setup
- Build/deploy steps for Ubuntu and Apache
- Testing steps

Use concise but complete markdown.

Project objective:
{objective}

Plan:
{json.dumps(plan, indent=2)}
"""

    content = ask_brain(prompt, route_hint="fast", max_tokens=1800)
    return _safe_write(readme_path, content, "Generated README from web development agent")


def generate_laravel_scaffold_bundle(target_dir: Path, objective: str, plan: dict) -> str:
    prompt = f"""
You are generating a production-ready Laravel 12 SaaS starter bundle.

Return strict JSON only with this schema:
{{
  "files": [
    {{
      "path": "relative/path/from/project/root.php or .blade.php or .md",
      "content": "full file contents"
    }}
  ],
  "notes": ["short implementation notes"]
}}

Requirements:
- Use Blade + Tailwind CSS + Alpine.js + Vite.
- Include a clean dashboard shell with sidebar navigation and responsive layout.
- Include model/controller/request/migration/view scaffolding for projects and tasks.
- Include README.md with install, environment, database, build, and deployment steps.
- Include code comments only where helpful.
- Keep the output production-grade and modular.
- Never overwrite existing work without warning in the content itself.

Project objective:
{objective}

Plan:
{json.dumps(plan, indent=2)}
"""

    raw = ask_brain(prompt, route_hint="fast", max_tokens=5000)
    data = _extract_json(raw) or {}
    files = data.get("files", [])
    if not isinstance(files, list) or not files:
        return "Jarvis could not generate a scaffold bundle from the current request."

    output = ["GENERATED LARAVEL SCAFFOLD BUNDLE"]
    for item in files:
        if not isinstance(item, dict):
            continue

        relative_path = (item.get("path") or "").strip()
        content = item.get("content") or ""
        if not relative_path or not content:
            continue

        target = target_dir / relative_path
        result = _safe_write(target, content, f"Generated scaffold file: {relative_path}")
        output.append(f"- {relative_path}: {result}")

    notes = data.get("notes", [])
    if notes:
        output.append("")
        output.append("Notes:")
        output.extend(f"- {note}" for note in notes if note)

    return "\n".join(output)


def create_laravel_app_from_request(user_input: str, chat_context: str | None = None) -> str:
    plan = build_web_development_plan(user_input, chat_context)
    target_text = plan.get("target_path") or _parse_target(user_input, chat_context)

    if not target_text:
        return format_web_development_plan(plan)

    target_dir = Path(target_text).expanduser().resolve()
    if not _inside_safe_base(target_dir):
        return f"Blocked target path: {target_dir}"

    if _target_exists_and_is_not_empty(target_dir):
        return (
            "CONFIRMATION REQUIRED\n"
            f"Target already contains files: {target_dir}\n"
            "Jarvis will not overwrite existing work without confirmation.\n\n"
            + format_web_development_plan(plan)
        )

    result_lines = [
        "WEB DEVELOPMENT EXECUTION",
        f"Target: {target_dir}",
        "",
        _install_laravel_stack(target_dir),
    ]

    result_lines.append("")
    result_lines.append(_generate_readme(target_dir, plan.get("objective", _normalize(user_input)), plan))
    result_lines.append("")
    result_lines.append(generate_laravel_scaffold_bundle(target_dir, plan.get("objective", _normalize(user_input)), plan))

    return "\n".join(result_lines)


def generate_laravel_module(request: str, chat_context: str | None = None) -> str:
    plan = build_web_development_plan(request, chat_context)
    return format_web_development_plan(plan)
