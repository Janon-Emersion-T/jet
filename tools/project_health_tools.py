from pathlib import Path
import json
import subprocess
import ast
import re
import hashlib

from tools.project_context_tools import get_current_project_path

MAX_OUTPUT = 12000

SKIP_DIRS = {
    ".git", "node_modules", "vendor", "venv", "__pycache__",
    "storage", "bootstrap/cache", "dist", "build", ".next"
}


def _project():
    project = get_current_project_path()
    if not project:
        return None, "No current project selected. Use: use project <name-or-path>"
    return Path(project), None


def _skip(path: Path):
    return any(part in SKIP_DIRS for part in path.parts)


def _run(cmd, cwd, timeout=40):
    try:
        result = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout
        )
        output = (result.stdout.strip() or result.stderr.strip() or "No output.")
        return output[:MAX_OUTPUT]
    except FileNotFoundError:
        return f"Command not found: {cmd[0]}"
    except Exception as e:
        return f"Command failed: {e}"


def vite_build_checker():
    project, error = _project()
    if error:
        return error

    if not (project / "package.json").exists():
        return "package.json not found. This does not look like a Vite/Node project."

    return "VITE BUILD CHECKER\n\n" + _run(["npm", "run", "build"], project, timeout=90)


def npm_script_runner():
    project, error = _project()
    if error:
        return error

    package = project / "package.json"
    if not package.exists():
        return "package.json not found."

    data = json.loads(package.read_text(errors="replace"))
    scripts = data.get("scripts", {})

    if not scripts:
        return "No npm scripts found."

    lines = ["NPM SCRIPT RUNNER", "Available scripts:"]
    lines.extend(f"- npm run {name}: {cmd}" for name, cmd in scripts.items())
    lines.append("\nSafe mode: listing only. To execute, add a dedicated confirmed route later.")
    return "\n".join(lines)


def composer_script_runner():
    project, error = _project()
    if error:
        return error

    composer = project / "composer.json"
    if not composer.exists():
        return "composer.json not found."

    data = json.loads(composer.read_text(errors="replace"))
    scripts = data.get("scripts", {})

    if not scripts:
        return "No composer scripts found."

    lines = ["COMPOSER SCRIPT RUNNER", "Available scripts:"]
    for name, cmd in scripts.items():
        lines.append(f"- composer {name}: {cmd}")
    lines.append("\nSafe mode: listing only. No composer script executed.")
    return "\n".join(lines)


def python_test_runner():
    project, error = _project()
    if error:
        return error

    if (project / "pytest.ini").exists() or (project / "tests").exists():
        return "PYTHON TEST RUNNER\n\n" + _run(["python3", "-m", "pytest"], project, timeout=90)

    return "No pytest config/tests folder found."


def php_syntax_checker():
    project, error = _project()
    if error:
        return error

    findings = []
    for file in project.rglob("*.php"):
        if _skip(file):
            continue
        output = _run(["php", "-l", str(file)], project)
        if "No syntax errors detected" not in output:
            findings.append(f"{file.relative_to(project)}\n{output}")

    if not findings:
        return "PHP SYNTAX CHECKER\nNo PHP syntax errors found."

    return "PHP SYNTAX CHECKER\n\n" + "\n\n".join(findings[:40])


def js_syntax_checker():
    project, error = _project()
    if error:
        return error

    findings = []
    for file in list(project.rglob("*.js")) + list(project.rglob("*.jsx")):
        if _skip(file):
            continue
        content = file.read_text(errors="replace")
        if "<<<<<<<" in content or ">>>>>>>" in content:
            findings.append(f"- Merge conflict marker found: {file.relative_to(project)}")
        if "console.log(" in content:
            findings.append(f"- console.log found: {file.relative_to(project)}")

    if not findings:
        return "JS SYNTAX CHECKER\nNo obvious JS risks found."

    return "JS SYNTAX CHECKER\n\n" + "\n".join(findings[:100])


def css_tailwind_checker():
    project, error = _project()
    if error:
        return error

    findings = []

    if not (project / "tailwind.config.js").exists() and not (project / "tailwind.config.cjs").exists():
        findings.append("- Tailwind config not found.")

    for file in list(project.rglob("*.css")) + list(project.rglob("*.blade.php")):
        if _skip(file):
            continue
        text = file.read_text(errors="replace")
        if "@tailwind" in text:
            findings.append(f"- Tailwind directives found in {file.relative_to(project)}")

    return "CSS / TAILWIND CHECKER\n\n" + ("\n".join(findings) if findings else "No obvious CSS/Tailwind risks found.")


def blade_syntax_risk_checker():
    project, error = _project()
    if error:
        return error

    findings = []
    for file in project.rglob("*.blade.php"):
        if _skip(file):
            continue
        text = file.read_text(errors="replace")
        opens = text.count("@if") + text.count("@foreach") + text.count("@forelse")
        closes = text.count("@endif") + text.count("@endforeach") + text.count("@endforelse")
        if opens != closes:
            findings.append(f"- Possible Blade directive mismatch: {file.relative_to(project)}")
        if "@csrf" not in text and "<form" in text.lower():
            findings.append(f"- Form without visible @csrf: {file.relative_to(project)}")

    return "BLADE SYNTAX RISK CHECKER\n\n" + ("\n".join(findings[:100]) if findings else "No obvious Blade risks found.")


def project_todo_scanner():
    project, error = _project()
    if error:
        return error

    findings = []
    pattern = re.compile(r"(TODO|FIXME|HACK|XXX)", re.IGNORECASE)

    for file in project.rglob("*"):
        if _skip(file) or not file.is_file():
            continue
        if file.suffix.lower() not in [".py", ".php", ".js", ".jsx", ".ts", ".tsx", ".css", ".blade.php"]:
            continue

        for i, line in enumerate(file.read_text(errors="replace").splitlines(), start=1):
            stripped = line.strip()

            if "TODO/FIXME/HACK" in stripped or "TODO|FIXME|HACK|XXX" in stripped:
                continue

            if "project_todo_scanner" in stripped:
                continue

            if pattern.search(stripped):
                findings.append(f"- {file.relative_to(project)}:{i} {stripped}")

    return "PROJECT TODO SCANNER\n\n" + ("\n".join(findings[:150]) if findings else "No TODO/FIXME/HACK markers found.")


def code_smell_detector():
    project, error = _project()
    if error:
        return error

    findings = []

    for file in project.rglob("*"):
        if _skip(file) or not file.is_file():
            continue
        if file.suffix.lower() not in [".py", ".php", ".js", ".jsx"]:
            continue

        lines = file.read_text(errors="replace").splitlines()

        if len(lines) > 500:
            findings.append(f"- Large file over 500 lines: {file.relative_to(project)} ({len(lines)} lines)")

        for i, line in enumerate(lines, start=1):
            if "eval(" in line or "shell=True" in line:
                findings.append(f"- Risky execution pattern: {file.relative_to(project)}:{i}")

    return "CODE SMELL DETECTOR\n\n" + ("\n".join(findings[:120]) if findings else "No obvious code smells found.")


def duplicate_code_detector():
    project, error = _project()
    if error:
        return error

    hashes = {}
    duplicates = []

    for file in project.rglob("*"):
        if _skip(file) or not file.is_file():
            continue
        if file.suffix.lower() not in [".py", ".php", ".js", ".jsx", ".blade.php"]:
            continue

        content = file.read_text(errors="replace").strip()
        if len(content) < 100:
            continue

        h = hashlib.sha256(content.encode("utf-8")).hexdigest()
        if h in hashes:
            duplicates.append(f"- {file.relative_to(project)} duplicates {hashes[h]}")
        else:
            hashes[h] = file.relative_to(project)

    return "DUPLICATE CODE DETECTOR\n\n" + ("\n".join(duplicates[:80]) if duplicates else "No exact duplicate files found.")


def dead_file_detector():
    project, error = _project()
    if error:
        return error

    suspicious = []
    for file in project.rglob("*"):
        if _skip(file) or not file.is_file():
            continue
        name = file.name.lower()
        if name.endswith((".bak", ".old", ".backup", ".tmp")) or "copy" in name:
            suspicious.append(f"- {file.relative_to(project)}")

    return "DEAD FILE DETECTOR\n\n" + ("\n".join(suspicious[:100]) if suspicious else "No obvious dead/backup files found.")


def missing_import_detector():
    project, error = _project()
    if error:
        return error

    findings = []

    for file in project.rglob("*.py"):
        if _skip(file):
            continue
        try:
            ast.parse(file.read_text(errors="replace"))
        except SyntaxError as e:
            findings.append(f"- Python syntax/import parse risk: {file.relative_to(project)}:{e.lineno} {e.msg}")

    return "MISSING IMPORT DETECTOR\n\n" + ("\n".join(findings[:100]) if findings else "No Python parse-level import risks found.")


def missing_route_detector():
    project, error = _project()
    if error:
        return error

    if not (project / "routes").exists():
        return "routes folder not found."

    route_refs = []
    for file in project.rglob("*.blade.php"):
        if _skip(file):
            continue
        text = file.read_text(errors="replace")
        route_refs.extend(re.findall(r"route\(['\"]([^'\"]+)['\"]", text))

    if not route_refs:
        return "MISSING ROUTE DETECTOR\nNo Blade route() references found."

    web = ""
    for route_file in (project / "routes").glob("*.php"):
        web += route_file.read_text(errors="replace")

    missing = [r for r in sorted(set(route_refs)) if r not in web]

    return "MISSING ROUTE DETECTOR\n\n" + ("\n".join(f"- {r}" for r in missing) if missing else "No obvious missing named routes found.")


def missing_view_detector():
    project, error = _project()
    if error:
        return error

    findings = []
    views_root = project / "resources" / "views"

    if not views_root.exists():
        return "resources/views folder not found."

    for file in project.rglob("*.php"):
        if _skip(file):
            continue
        text = file.read_text(errors="replace")
        refs = re.findall(r"view\(['\"]([^'\"]+)['\"]", text)

        for ref in refs:
            view_path = views_root / (ref.replace(".", "/") + ".blade.php")
            if not view_path.exists():
                findings.append(f"- Missing view `{ref}` referenced in {file.relative_to(project)}")

    return "MISSING VIEW DETECTOR\n\n" + ("\n".join(findings[:100]) if findings else "No obvious missing views found.")


def missing_component_detector():
    project, error = _project()
    if error:
        return error

    views_root = project / "resources" / "views"
    components_root = views_root / "components"

    if not views_root.exists():
        return "resources/views folder not found."

    findings = []

    for file in project.rglob("*.blade.php"):
        if _skip(file):
            continue
        text = file.read_text(errors="replace")
        refs = re.findall(r"<x-([a-zA-Z0-9._:-]+)", text)

        for ref in refs:
            clean = ref.split(":")[0].replace(".", "/")
            possible = components_root / f"{clean}.blade.php"
            if not possible.exists():
                findings.append(f"- Possible missing component <x-{ref}> in {file.relative_to(project)}")

    return "MISSING COMPONENT DETECTOR\n\n" + ("\n".join(sorted(set(findings))[:100]) if findings else "No obvious missing Blade components found.")


def db_config_checker():
    project, error = _project()
    if error:
        return error

    env = project / ".env"
    if not env.exists():
        return "DB CONFIG CHECKER\n.env not found."

    text = env.read_text(errors="replace")
    keys = ["DB_CONNECTION", "DB_HOST", "DB_PORT", "DB_DATABASE", "DB_USERNAME"]
    lines = ["DB CONFIG CHECKER"]

    for key in keys:
        match = re.search(rf"^{key}=(.*)$", text, re.MULTILINE)
        if match:
            value = match.group(1)
            if key in ["DB_PASSWORD"]:
                value = "***"
            lines.append(f"- {key}: {value}")
        else:
            lines.append(f"- Missing: {key}")

    return "\n".join(lines)


def migration_status_checker():
    project, error = _project()
    if error:
        return error

    if not (project / "artisan").exists():
        return "Laravel artisan file not found."

    return "MIGRATION STATUS CHECKER\n\n" + _run(["php", "artisan", "migrate:status"], project, timeout=60)


def safe_artisan_runner():
    project, error = _project()
    if error:
        return error

    if not (project / "artisan").exists():
        return "Laravel artisan file not found."

    safe_commands = [
        "about",
        "route:list",
        "view:clear",
        "config:clear",
        "cache:clear",
        "migrate:status",
    ]

    lines = ["SAFE ARTISAN RUNNER", "Allowed safe commands:"]
    lines.extend(f"- php artisan {cmd}" for cmd in safe_commands)
    lines.append("\nExecution should be confirm-based in the next write-safe phase.")
    return "\n".join(lines)


def project_health_score():
    checks = [
        project_todo_scanner,
        code_smell_detector,
        dead_file_detector,
        missing_view_detector,
        missing_component_detector,
        db_config_checker,
    ]

    score = 100
    report = ["PROJECT HEALTH SCORE"]

    for check in checks:
        result = check()
        issue_count = result.count("- ")
        score -= min(issue_count * 2, 15)
        report.append(f"\n{result}")

    score = max(score, 0)
    report.insert(1, f"Score: {score}/100")

    if score >= 85:
        report.insert(2, "Status: Healthy")
    elif score >= 65:
        report.insert(2, "Status: Needs cleanup")
    else:
        report.insert(2, "Status: Risky")

    return "\n".join(report)
