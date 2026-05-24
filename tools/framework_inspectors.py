from pathlib import Path
import re
import json

from tools.project_context_tools import get_current_project_path
from tools.system_tools import read_project_file


MAX_LINES = 120


def _project():
    project = get_current_project_path()
    if not project:
        return None, "No current project selected. Use: use project <name-or-path>"
    return project, None


def _read_text(path: Path) -> str:
    return path.read_text(errors="replace")


def _preview_file(path: Path, project: Path, max_lines: int = MAX_LINES) -> str:
    try:
        lines = _read_text(path).splitlines()
        preview = "\n".join(lines[:max_lines])
        if len(lines) > max_lines:
            preview += "\n[TRUNCATED]"
        return f"\n===== {path.relative_to(project)} =====\n{preview}"
    except Exception as e:
        return f"\n===== {path.relative_to(project)} =====\nRead error: {e}"


def analyze_python_traceback(error_text: str) -> str:
    if not error_text.strip():
        return "Paste a Python traceback after: analyze python traceback ::: <traceback>"

    lines = error_text.splitlines()

    exception_line = ""
    file_lines = []

    for line in lines:
        if line.strip().startswith("File "):
            file_lines.append(line.strip())
        if re.search(r"^[A-Za-z_][A-Za-z0-9_]*(Error|Exception|Warning):", line.strip()):
            exception_line = line.strip()

    result = ["PYTHON TRACEBACK ANALYZER"]

    if exception_line:
        result.append(f"\nException:\n- {exception_line}")
    else:
        result.append("\nException: Not clearly detected.")

    if file_lines:
        result.append("\nTrace path:")
        result.extend(f"- {line}" for line in file_lines[-8:])

    lower = error_text.lower()

    result.append("\nLikely cause:")
    if "modulenotfounderror" in lower:
        result.append("- Missing Python package or wrong import path.")
    elif "importerror" in lower:
        result.append("- Import exists but requested function/class may not exist or name is wrong.")
    elif "typeerror" in lower:
        result.append("- Function was called with wrong argument count/type.")
    elif "attributeerror" in lower:
        result.append("- Object does not have the requested method/property.")
    elif "filenotfounderror" in lower:
        result.append("- File path is wrong or file was not created.")
    elif "permissionerror" in lower:
        result.append("- File/folder permission issue.")
    elif "syntaxerror" in lower:
        result.append("- Python syntax is invalid.")
    else:
        result.append("- General runtime exception. Review the final exception line and last project file in trace.")

    result.append("\nRecommended next step:")
    result.append("- Inspect the last project file shown in the traceback and verify the exact function/class call.")

    return "\n".join(result)


def analyze_node_error(error_text: str) -> str:
    if not error_text.strip():
        return "Paste a Node/Vite/Electron error after: analyze node error ::: <error>"

    lower = error_text.lower()

    result = ["NODE ERROR ANALYZER"]

    result.append("\nLikely cause:")

    if "cannot find module" in lower:
        result.append("- Missing dependency or wrong import path.")
    elif "enoent" in lower:
        result.append("- File or directory does not exist.")
    elif "eaddrinuse" in lower:
        result.append("- Port already in use.")
    elif "vite" in lower and "manifest" in lower:
        result.append("- Vite build manifest missing. Run npm run build or check asset path.")
    elif "electron" in lower and "blank" in lower:
        result.append("- Electron window may be loading the wrong URL/path.")
    elif "syntaxerror" in lower:
        result.append("- JavaScript syntax error.")
    elif "typeerror" in lower:
        result.append("- Wrong value type, missing function, or undefined object.")
    else:
        result.append("- General Node/Electron/Vite runtime error.")

    result.append("\nRecommended next step:")
    result.append("- Check package.json scripts, imports, and the first project file mentioned in the stack.")

    stack_lines = [
        line.strip()
        for line in error_text.splitlines()
        if " at " in line or "Error:" in line or "Cannot" in line
    ]

    if stack_lines:
        result.append("\nRelevant lines:")
        result.extend(f"- {line}" for line in stack_lines[:12])

    return "\n".join(result)


def auto_fix_proposal_from_error(error_text: str) -> str:
    if not error_text.strip():
        return "Paste an error after: propose fix from error ::: <error>"

    project, error = _project()
    if error:
        return error

    lower = error_text.lower()
    result = ["AUTO-FIX PROPOSAL FROM ERROR", f"Project: {project}\n"]

    if "modulenotfounderror" in lower:
        result.append("Suggested fix:")
        result.append("- Add the missing package to requirements.txt if it is external.")
        result.append("- Or fix the import path if it is a local module.")
    elif "importerror" in lower:
        result.append("Suggested fix:")
        result.append("- Open the imported file and verify the function/class name exists.")
        result.append("- Rename either the import or the actual function/class for consistency.")
    elif "typeerror" in lower and "positional argument" in lower:
        result.append("Suggested fix:")
        result.append("- Check the function definition and update the caller to pass the correct number of arguments.")
    elif "vite" in lower and "manifest" in lower:
        result.append("Suggested fix:")
        result.append("- Run npm install and npm run build.")
        result.append("- Confirm public/build/manifest.json exists.")
    elif "route [" in lower and "not defined" in lower:
        result.append("Suggested fix:")
        result.append("- Add the missing Laravel route name in routes/web.php or update the Blade/controller reference.")
    elif "permission denied" in lower:
        result.append("Suggested fix:")
        result.append("- Fix file ownership and permissions for storage and bootstrap/cache.")
    else:
        result.append("Suggested fix:")
        result.append("- Inspect the final error line and the last project file in the stack trace.")
        result.append("- Then create a patch proposal for the smallest safe change.")

    result.append("\nSafety rule:")
    result.append("- This is advisory only. No file was changed.")

    return "\n".join(result)


def inspect_routes() -> str:
    project, error = _project()
    if error:
        return error

    candidates = [
        project / "routes" / "web.php",
        project / "routes" / "api.php",
        project / "routes" / "console.php",
        project / "routes" / "channels.php",
    ]

    found = [p for p in candidates if p.exists()]

    if not found:
        return "No Laravel route files found."

    output = [f"ROUTE INSPECTOR\nProject: {project}"]

    route_pattern = re.compile(r"Route::(get|post|put|patch|delete|resource|middleware|prefix|group)\((.*?)\)", re.DOTALL)

    for file in found:
        content = _read_text(file)
        matches = route_pattern.findall(content)

        output.append(f"\n===== {file.relative_to(project)} =====")
        output.append(f"Route-like entries detected: {len(matches)}")

        named = re.findall(r"->name\(['\"](.+?)['\"]\)", content)
        if named:
            output.append("Named routes:")
            output.extend(f"- {name}" for name in named[:50])

        output.append(_preview_file(file, project, 80))

    return "\n".join(output)


def inspect_laravel_controllers() -> str:
    project, error = _project()
    if error:
        return error

    folder = project / "app" / "Http" / "Controllers"

    if not folder.exists():
        return "Laravel controllers folder not found."

    files = list(folder.rglob("*.php"))

    output = [f"LARAVEL CONTROLLER INSPECTOR\nProject: {project}", f"Controllers found: {len(files)}"]

    for file in files[:20]:
        content = _read_text(file)
        class_match = re.search(r"class\s+(\w+)", content)
        methods = re.findall(r"public function\s+(\w+)\s*\(", content)

        output.append(f"\n- {file.relative_to(project)}")
        if class_match:
            output.append(f"  Class: {class_match.group(1)}")
        if methods:
            output.append(f"  Public methods: {', '.join(methods[:20])}")

    return "\n".join(output)


def inspect_laravel_models() -> str:
    project, error = _project()
    if error:
        return error

    folder = project / "app" / "Models"

    if not folder.exists():
        return "Laravel models folder not found."

    files = list(folder.rglob("*.php"))

    output = [f"LARAVEL MODEL INSPECTOR\nProject: {project}", f"Models found: {len(files)}"]

    for file in files[:30]:
        content = _read_text(file)
        class_match = re.search(r"class\s+(\w+)", content)
        fillable = re.search(r"protected\s+\$fillable\s*=\s*\[(.*?)\];", content, re.DOTALL)
        relationships = re.findall(r"public function\s+(\w+)\s*\(\)\s*{[^}]*return\s+\$this->(hasMany|belongsTo|hasOne|belongsToMany)", content, re.DOTALL)

        output.append(f"\n- {file.relative_to(project)}")
        if class_match:
            output.append(f"  Model: {class_match.group(1)}")
        if fillable:
            fields = re.findall(r"['\"](.+?)['\"]", fillable.group(1))
            output.append(f"  Fillable: {', '.join(fields[:30])}")
        if relationships:
            output.append("  Relationships:")
            for name, rel_type in relationships[:20]:
                output.append(f"  - {name}: {rel_type}")

    return "\n".join(output)


def inspect_laravel_migrations() -> str:
    project, error = _project()
    if error:
        return error

    folder = project / "database" / "migrations"

    if not folder.exists():
        return "Laravel migrations folder not found."

    files = sorted(folder.glob("*.php"))

    output = [f"LARAVEL MIGRATION INSPECTOR\nProject: {project}", f"Migrations found: {len(files)}"]

    for file in files[:50]:
        content = _read_text(file)
        tables = re.findall(r"Schema::(?:create|table)\(['\"](.+?)['\"]", content)
        columns = re.findall(r"\$table->(\w+)\(['\"](.+?)['\"]", content)

        output.append(f"\n- {file.name}")
        if tables:
            output.append(f"  Tables: {', '.join(tables)}")
        if columns:
            formatted = [f"{name}:{col_type}" for col_type, name in columns[:25]]
            output.append(f"  Columns: {', '.join(formatted)}")

    return "\n".join(output)


def inspect_laravel_blade() -> str:
    project, error = _project()
    if error:
        return error

    folder = project / "resources" / "views"

    if not folder.exists():
        return "Laravel Blade views folder not found."

    files = list(folder.rglob("*.blade.php"))

    output = [f"LARAVEL BLADE INSPECTOR\nProject: {project}", f"Blade files found: {len(files)}"]

    for file in files[:50]:
        content = _read_text(file)
        extends = re.findall(r"@extends\(['\"](.+?)['\"]\)", content)
        sections = re.findall(r"@section\(['\"](.+?)['\"]", content)
        components = re.findall(r"<x-([\w\-.]+)", content)

        output.append(f"\n- {file.relative_to(project)}")
        if extends:
            output.append(f"  Extends: {', '.join(extends)}")
        if sections:
            output.append(f"  Sections: {', '.join(sections)}")
        if components:
            output.append(f"  Components: {', '.join(sorted(set(components))[:20])}")

    return "\n".join(output)


def inspect_livewire() -> str:
    project, error = _project()
    if error:
        return error

    folders = [
        project / "app" / "Livewire",
        project / "app" / "Http" / "Livewire",
        project / "resources" / "views" / "livewire",
    ]

    found_files = []

    for folder in folders:
        if folder.exists():
            found_files.extend(list(folder.rglob("*")))

    found_files = [f for f in found_files if f.is_file()]

    if not found_files:
        return "Livewire files not found."

    output = [f"LIVEWIRE INSPECTOR\nProject: {project}", f"Livewire-related files found: {len(found_files)}"]

    for file in found_files[:50]:
        output.append(f"- {file.relative_to(project)}")

    return "\n".join(output)


def inspect_filament() -> str:
    project, error = _project()
    if error:
        return error

    folders = [
        project / "app" / "Filament",
        project / "app" / "Providers" / "Filament",
    ]

    found_files = []

    for folder in folders:
        if folder.exists():
            found_files.extend(list(folder.rglob("*.php")))

    composer = project / "composer.json"
    filament_dependency = False

    if composer.exists():
        try:
            data = json.loads(composer.read_text(errors="replace"))
            deps = {}
            deps.update(data.get("require", {}))
            deps.update(data.get("require-dev", {}))
            filament_dependency = any("filament" in key for key in deps.keys())
        except Exception:
            pass

    if not found_files and not filament_dependency:
        return "Filament files/dependency not found."

    output = [f"FILAMENT INSPECTOR\nProject: {project}"]

    if filament_dependency:
        output.append("Filament dependency detected in composer.json.")

    output.append(f"Filament PHP files found: {len(found_files)}")

    for file in found_files[:50]:
        output.append(f"- {file.relative_to(project)}")

    return "\n".join(output)
