from pathlib import Path
import re
from tools.project_context_tools import get_current_project_path

SKIP_DIRS = {
    ".git", "node_modules", "vendor", "venv", "__pycache__",
    "storage", "bootstrap/cache", "dist", "build", ".next"
}

CODE_EXTENSIONS = [".py", ".php", ".js", ".jsx", ".blade.php"]


def _project():
    project = get_current_project_path()
    if not project:
        return None, 'No current project selected.\nUse: use project <name-or-path>'
    return Path(project), None


def _skip(path: Path):
    return any(part in SKIP_DIRS for part in path.parts)


def _code_files(project: Path):
    files = []
    for file in project.rglob("*"):
        if _skip(file) or not file.is_file():
            continue
        if file.suffix.lower() in CODE_EXTENSIONS or file.name.endswith(".blade.php"):
            files.append(file)
    return files


def _rel(project, file):
    return str(file.relative_to(project))


def refactor_planner():
    project, error = _project()
    if error:
        return error

    findings = []
    for file in _code_files(project):
        text = file.read_text(errors="replace")
        lines = text.splitlines()

        if len(lines) > 400:
            findings.append(f"- Split large file: {_rel(project, file)} ({len(lines)} lines)")

        function_count = len(re.findall(r"\bfunction\s+\w+|\bdef\s+\w+", text))
        if function_count > 15:
            findings.append(f"- Too many functions in one file: {_rel(project, file)} ({function_count})")

        if text.count("if ") + text.count("elif ") + text.count("else") > 40:
            findings.append(f"- High branching complexity: {_rel(project, file)}")

    return "REFACTOR PLANNER — PHASE 221\n\n" + (
        "\n".join(findings[:120]) if findings else "No major refactor targets detected."
    )


def architecture_consistency_checker():
    project, error = _project()
    if error:
        return error

    findings = []

    expected = [
        "core",
        "core/routes",
        "tools",
        "storage",
    ]

    for folder in expected:
        if not (project / folder).exists():
            findings.append(f"- Missing expected folder: {folder}")

    router = project / "core" / "command_router.py"
    if router.exists():
        lines = router.read_text(errors="replace").splitlines()
        if len(lines) > 100:
            findings.append("- command_router.py is growing too large. Keep it lightweight.")

    for file in (project / "core" / "routes").glob("*.py") if (project / "core" / "routes").exists() else []:
        text = file.read_text(errors="replace")
        if "def handle_" not in text and file.name != "__init__.py":
            findings.append(f"- Route file may not expose handler function: {_rel(project, file)}")

    return "ARCHITECTURE CONSISTENCY CHECKER — PHASE 222\n\n" + (
        "\n".join(findings) if findings else "Architecture looks consistent with the modular route-driven system."
    )


def naming_convention_analyzer():
    project, error = _project()
    if error:
        return error

    findings = []

    for file in _code_files(project):
        name = file.name

        if file.suffix == ".py" and not re.match(r"^[a-z0-9_]+\.py$", name):
            findings.append(f"- Python file should use snake_case: {_rel(project, file)}")

        if file.suffix == ".php":
            text = file.read_text(errors="replace")
            classes = re.findall(r"\bclass\s+([A-Za-z0-9_]+)", text)
            for cls in classes:
                if not re.match(r"^[A-Z][A-Za-z0-9]+$", cls):
                    findings.append(f"- PHP class should use PascalCase: {cls} in {_rel(project, file)}")

        text = file.read_text(errors="replace")
        bad_functions = re.findall(r"\b(def|function)\s+([A-Z][A-Za-z0-9_]*)", text)
        for _, fn in bad_functions:
            findings.append(f"- Function should usually use camelCase/snake_case, not PascalCase: {fn} in {_rel(project, file)}")

    return "NAMING CONVENTION ANALYZER — PHASE 223\n\n" + (
        "\n".join(findings[:120]) if findings else "No obvious naming convention issues detected."
    )


def solid_principle_analyzer():
    project, error = _project()
    if error:
        return error

    findings = []

    for file in _code_files(project):
        text = file.read_text(errors="replace")
        lines = text.splitlines()

        if len(lines) > 500:
            findings.append(f"- SRP risk: {_rel(project, file)} is very large.")

        class_count = len(re.findall(r"\bclass\s+\w+", text))
        if class_count > 5:
            findings.append(f"- SRP risk: many classes in one file: {_rel(project, file)}")

        if "new " in text and "interface " not in text and file.suffix == ".php":
            findings.append(f"- DIP risk: direct object construction found in {_rel(project, file)}")

        if re.search(r"if\s*\(.*type|switch\s*\(", text):
            findings.append(f"- OCP risk: type/switch branching may need polymorphism in {_rel(project, file)}")

    return "SOLID PRINCIPLE ANALYZER — PHASE 224\n\n" + (
        "\n".join(findings[:120]) if findings else "No obvious SOLID risks detected."
    )


def clean_code_scorer():
    project, error = _project()
    if error:
        return error

    score = 100
    issues = []

    for file in _code_files(project):
        text = file.read_text(errors="replace")
        lines = text.splitlines()

        if len(lines) > 400:
            score -= 3
            issues.append(f"- Large file: {_rel(project, file)}")

        if "TODO" in text or "FIXME" in text:
            score -= 1
            issues.append(f"- TODO/FIXME found: {_rel(project, file)}")

        if "print(" in text or "console.log(" in text:
            score -= 1
            issues.append(f"- Debug output found: {_rel(project, file)}")

        if text.count("try:") > 10 or text.count("catch") > 10:
            score -= 1
            issues.append(f"- Heavy exception handling: {_rel(project, file)}")

    score = max(score, 0)

    if score >= 85:
        status = "Clean"
    elif score >= 65:
        status = "Needs cleanup"
    else:
        status = "Risky"

    return f"CLEAN CODE SCORER — PHASE 225\n\nScore: {score}/100\nStatus: {status}\n\n" + (
        "\n".join(issues[:120]) if issues else "No major clean-code issues detected."
    )


def design_pattern_detector():
    project, error = _project()
    if error:
        return error

    patterns = []

    for file in _code_files(project):
        text = file.read_text(errors="replace")
        rel = _rel(project, file)

        if "Factory" in text:
            patterns.append(f"- Factory pattern hint: {rel}")

        if "Observer" in text or "Event" in text or "Listener" in text:
            patterns.append(f"- Observer/Event pattern hint: {rel}")

        if "Repository" in text:
            patterns.append(f"- Repository pattern hint: {rel}")

        if "Service" in text:
            patterns.append(f"- Service layer hint: {rel}")

        if "Middleware" in text:
            patterns.append(f"- Middleware pattern hint: {rel}")

    return "DESIGN PATTERN DETECTOR — PHASE 226\n\n" + (
        "\n".join(sorted(set(patterns))[:120]) if patterns else "No obvious design pattern usage detected."
    )


def service_container_analyzer():
    project, error = _project()
    if error:
        return error

    findings = []

    providers = project / "app" / "Providers"
    if not providers.exists():
        return "SERVICE CONTAINER ANALYZER — PHASE 227\n\nNo Laravel app/Providers folder found."

    for file in providers.rglob("*.php"):
        text = file.read_text(errors="replace")
        rel = _rel(project, file)

        if "bind(" in text:
            findings.append(f"- Binding found: {rel}")

        if "singleton(" in text:
            findings.append(f"- Singleton found: {rel}")

        if "register()" in text and "bind(" not in text and "singleton(" not in text:
            findings.append(f"- Provider register() has no obvious bindings: {rel}")

    return "SERVICE CONTAINER ANALYZER — PHASE 227\n\n" + (
        "\n".join(findings) if findings else "No service container bindings detected."
    )


def laravel_middleware_analyzer():
    project, error = _project()
    if error:
        return error

    middleware_dir = project / "app" / "Http" / "Middleware"
    if not middleware_dir.exists():
        return "LARAVEL MIDDLEWARE ANALYZER — PHASE 228\n\nNo app/Http/Middleware folder found."

    findings = []

    for file in middleware_dir.rglob("*.php"):
        text = file.read_text(errors="replace")
        rel = _rel(project, file)

        if "handle(" not in text:
            findings.append(f"- Middleware missing handle() method: {rel}")

        if "return $next($request)" not in text and "$next($request)" not in text:
            findings.append(f"- Middleware may not pass request forward: {rel}")

    return "LARAVEL MIDDLEWARE ANALYZER — PHASE 228\n\n" + (
        "\n".join(findings) if findings else "Middleware files look structurally okay."
    )


def api_route_analyzer():
    project, error = _project()
    if error:
        return error

    api = project / "routes" / "api.php"
    if not api.exists():
        return "API ROUTE ANALYZER — PHASE 229\n\nroutes/api.php not found."

    text = api.read_text(errors="replace")
    routes = re.findall(r"Route::(get|post|put|patch|delete|apiResource|resource)\(", text)

    lines = [
        "API ROUTE ANALYZER — PHASE 229",
        "",
        f"Total API route declarations detected: {len(routes)}",
    ]

    for method in sorted(set(routes)):
        lines.append(f"- {method}: {routes.count(method)}")

    if "middleware(" not in text:
        lines.append("- Warning: No obvious middleware usage in api.php")

    return "\n".join(lines)


def rest_compliance_checker():
    project, error = _project()
    if error:
        return error

    api = project / "routes" / "api.php"
    if not api.exists():
        return "REST COMPLIANCE CHECKER — PHASE 230\n\nroutes/api.php not found."

    text = api.read_text(errors="replace")
    findings = []

    if re.search(r"Route::get\([^)]*(create|store|delete|update)", text, re.IGNORECASE):
        findings.append("- Possible REST violation: GET route used for create/store/update/delete action.")

    if re.search(r"Route::post\([^)]*(delete|remove)", text, re.IGNORECASE):
        findings.append("- Possible REST violation: POST used for delete/remove action.")

    if "apiResource" not in text and "Route::resource" not in text:
        findings.append("- Consider Route::apiResource for standard REST controllers.")

    if not re.search(r"\{[a-zA-Z_]+\}", text):
        findings.append("- No parameterized resource routes detected.")

    return "REST COMPLIANCE CHECKER — PHASE 230\n\n" + (
        "\n".join(findings) if findings else "API routes look reasonably REST-aligned."
    )
