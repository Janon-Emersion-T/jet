from pathlib import Path
import json
import subprocess
import re

from tools.project_context_tools import get_current_project_path


MAX_OUTPUT = 12000


def _project():
    project = get_current_project_path()
    if not project:
        return None, "No current project selected. Use: use project <name-or-path>"
    return project, None


def _run_git(project: Path, args: list[str]) -> str:
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=str(project),
            capture_output=True,
            text=True,
            timeout=20
        )
        output = result.stdout.strip() or result.stderr.strip()
        return output[:MAX_OUTPUT] if output else "No output."
    except Exception as e:
        return f"Git command error: {e}"


def inspect_dependencies() -> str:
    project, error = _project()
    if error:
        return error

    lines = [f"DEPENDENCY INSPECTOR\nProject: {project}\n"]

    req = project / "requirements.txt"
    package = project / "package.json"
    composer = project / "composer.json"

    if req.exists():
        lines.append("Python dependencies:")
        deps = [
            line.strip()
            for line in req.read_text(errors="replace").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        lines.extend(f"- {dep}" for dep in deps[:80])

    if package.exists():
        lines.append("\nNode dependencies:")
        try:
            data = json.loads(package.read_text(errors="replace"))
            deps = {}
            deps.update(data.get("dependencies", {}))
            deps.update(data.get("devDependencies", {}))
            lines.extend(f"- {k}: {v}" for k, v in list(deps.items())[:80])
        except Exception as e:
            lines.append(f"package.json read error: {e}")

    if composer.exists():
        lines.append("\nPHP Composer dependencies:")
        try:
            data = json.loads(composer.read_text(errors="replace"))
            deps = data.get("require", {})
            lines.extend(f"- {k}: {v}" for k, v in list(deps.items())[:80])
        except Exception as e:
            lines.append(f"composer.json read error: {e}")

    if len(lines) <= 2:
        return "No dependency files found."

    return "\n".join(lines)


def package_vulnerability_warning() -> str:
    project, error = _project()
    if error:
        return error

    lines = [f"PACKAGE VULNERABILITY WARNING\nProject: {project}\n"]
    lines.append("This is a local warning scan, not a live security audit.")

    risky_patterns = [
        "eval", "exec", "pickle", "subprocess", "shell=True",
        "request", "urllib", "pyaudio", "playwright"
    ]

    findings = []

    for file in project.rglob("*.py"):
        if any(part in file.parts for part in ["venv", ".git", "__pycache__"]):
            continue

        try:
            content = file.read_text(errors="replace")
            for pattern in risky_patterns:
                if pattern in content:
                    findings.append(f"- {file.relative_to(project)} contains `{pattern}`")
        except Exception:
            continue

    if not findings:
        lines.append("\nNo obvious risky package/code usage found.")
    else:
        lines.append("\nPotential review areas:")
        lines.extend(findings[:80])

    lines.append("\nFor real audits, run:")
    lines.append("- pip-audit")
    lines.append("- npm audit")
    lines.append("- composer audit")

    return "\n".join(lines)


def git_branch_detector() -> str:
    project, error = _project()
    if error:
        return error

    branch = _run_git(project, ["branch", "--show-current"])
    branches = _run_git(project, ["branch", "--all"])

    return f"GIT BRANCH DETECTOR\nProject: {project}\n\nCurrent branch:\n{branch}\n\nBranches:\n{branches}"


def git_commit_summarizer() -> str:
    project, error = _project()
    if error:
        return error

    log = _run_git(project, ["log", "--oneline", "-10"])
    return f"GIT COMMIT SUMMARIZER\nProject: {project}\n\nRecent commits:\n{log}"


def git_safe_status_mode() -> str:
    project, error = _project()
    if error:
        return error

    status = _run_git(project, ["status", "--short"])
    branch = _run_git(project, ["branch", "--show-current"])

    if status == "No output.":
        status = "Working tree clean."

    return f"GIT SAFE STATUS MODE\nProject: {project}\nBranch: {branch}\n\nStatus:\n{status}"


def git_diff_reader() -> str:
    project, error = _project()
    if error:
        return error

    diff = _run_git(project, ["diff", "--", "."])
    if diff == "No output.":
        return "No unstaged Git diff found."

    return f"GIT DIFF READER\nProject: {project}\n\n{diff}"


def git_commit_assistant() -> str:
    project, error = _project()
    if error:
        return error

    status = _run_git(project, ["status", "--short"])
    diff_stat = _run_git(project, ["diff", "--stat"])
    staged_stat = _run_git(project, ["diff", "--cached", "--stat"])

    if status == "No output.":
        return "Working tree clean. No commit needed."

    message = "Update project tooling and developer assistant features"

    lowered = status.lower()
    if "dev_ops_tools.py" in lowered or "project_analyzers.py" in lowered:
        message = "Add developer operations tools"
    elif "command_router.py" in lowered:
        message = "Update command routing logic"
    elif "requirements.txt" in lowered:
        message = "Update Python dependencies"

    return (
        "GIT COMMIT ASSISTANT\n"
        f"Project: {project}\n\n"
        "Changed files:\n"
        f"{status}\n\n"
        "Unstaged diff summary:\n"
        f"{diff_stat}\n\n"
        "Staged diff summary:\n"
        f"{staged_stat}\n\n"
        "Suggested commit message:\n"
        f"{message}\n\n"
        "Safe commands:\n"
        "git add .\n"
        f"git commit -m \"{message}\"\n"
    )


def git_ignore_inspector() -> str:
    project, error = _project()
    if error:
        return error

    ignore = project / ".gitignore"

    recommended = [
        "venv/",
        "__pycache__/",
        ".env",
        "*.pyc",
        "node_modules/",
        "vendor/",
        "storage/logs/",
        ".jarvis_proposals/",
    ]

    if not ignore.exists():
        return ".gitignore not found.\n\nRecommended entries:\n" + "\n".join(f"- {x}" for x in recommended)

    content = ignore.read_text(errors="replace")
    missing = [item for item in recommended if item not in content]

    lines = [f"GIT IGNORE INSPECTOR\nProject: {project}\n"]
    lines.append("Current .gitignore found.")

    if missing:
        lines.append("\nRecommended missing entries:")
        lines.extend(f"- {item}" for item in missing)
    else:
        lines.append("\n.gitignore looks acceptable for this project.")

    return "\n".join(lines)


def read_error_logs() -> str:
    project, error = _project()
    if error:
        return error

    log_candidates = [
        project / "storage" / "logs" / "laravel.log",
        project / "logs" / "error.log",
        project / "error.log",
        project / "storage" / "logs" / "app.log",
    ]

    found = [p for p in log_candidates if p.exists() and p.is_file()]

    if not found:
        return "No known error log files found."

    output = [f"ERROR LOG READER\nProject: {project}"]

    for log in found:
        content = log.read_text(errors="replace")
        tail = content[-8000:]
        output.append(f"\n===== {log.relative_to(project)} =====\n{tail}")

    return "\n".join(output)


def analyze_laravel_log() -> str:
    project, error = _project()
    if error:
        return error

    log = project / "storage" / "logs" / "laravel.log"

    if not log.exists():
        return "Laravel log not found at storage/logs/laravel.log"

    content = log.read_text(errors="replace")
    recent = content[-20000:]

    patterns = {
        "Route errors": r"Route \[.*?\] not defined|404|NotFoundHttpException",
        "Database errors": r"SQLSTATE|QueryException|could not find driver",
        "Permission errors": r"Permission denied|failed to open stream",
        "View errors": r"View .* not found|Unable to locate a class or view",
        "Vite errors": r"ViteManifestNotFoundException|manifest.json",
        "General exceptions": r"ERROR|Exception|Stack trace",
    }

    lines = [f"LARAVEL LOG ANALYZER\nProject: {project}\n"]

    for label, pattern in patterns.items():
        matches = re.findall(pattern, recent, re.IGNORECASE)
        lines.append(f"- {label}: {len(matches)}")

    lines.append("\nRecent log tail:")
    lines.append(recent[-6000:])

    return "\n".join(lines)
