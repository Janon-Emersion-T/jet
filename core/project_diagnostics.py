from pathlib import Path
import subprocess

from core.brain import ask_brain

from tools.system_tools import detect_project_stack, scan_project_files

def run_project_diagnostics(folder_path: str) -> str:
    path = Path(folder_path).expanduser()

    if not path.exists() or not path.is_dir():
        return "Project folder not found."

    report = []

    report.append(f"Diagnostics for: {path}")
    report.append("\n=== Stack Detection ===")
    report.append(detect_project_stack(str(path)))

    report.append("\n=== Project Files ===")
    report.append(scan_project_files(str(path)))

    report.append("\n=== Git Status ===")
    report.append(_run_command(["git", "status", "--short"], path))

    report.append("\n=== Python Syntax Check ===")
    report.append(_check_python_syntax(path))

    report.append("\n=== Dependency Files ===")
    report.append(_check_dependency_files(path))

    return "\n".join(report)


def _run_command(command: list, cwd: Path) -> str:
    try:
        result = subprocess.run(
            command,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=30
        )

        output = result.stdout.strip() or result.stderr.strip()
        return output if output else "No output."

    except Exception as e:
        return f"Command error: {e}"


def _check_python_syntax(path: Path) -> str:
    py_files = [
        p for p in path.rglob("*.py")
        if "venv" not in str(p) and ".git" not in str(p)
    ]

    if not py_files:
        return "No Python files found."

    errors = []

    for file in py_files[:50]:
        result = subprocess.run(
            ["python3", "-m", "py_compile", str(file)],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            errors.append(f"{file}:\n{result.stderr}")

    if not errors:
        return "Python syntax check passed."

    return "\n\n".join(errors)


def _check_dependency_files(path: Path) -> str:
    files = [
        "requirements.txt",
        "pyproject.toml",
        "package.json",
        "composer.json",
        "artisan",
        "vite.config.js"
    ]

    found = []

    for file in files:
        if (path / file).exists():
            found.append(f"- {file}")

    if not found:
        return "No common dependency files found."

    return "Found dependency/project files:\n" + "\n".join(found)

def interpret_project_diagnostics(folder_path: str) -> str:
    raw_report = run_project_diagnostics(folder_path)

    prompt = f"""
You are JARVIS, Janon's local senior software engineer.

Analyze this project diagnostic report.

Return:
1. Overall project health
2. Critical issues
3. Medium-priority issues
4. Recommended next steps
5. Whether the project is safe to continue building

Be direct. Do not exaggerate.

DIAGNOSTIC REPORT:
{raw_report}
"""

    interpretation = ask_brain(prompt)

    return f"{raw_report}\n\n=== JARVIS Interpretation ===\n{interpretation}"