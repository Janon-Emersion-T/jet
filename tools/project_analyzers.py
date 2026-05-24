from pathlib import Path
import json

from tools.project_context_tools import get_current_project_path


SKIP_DIRS = {
    ".git", "node_modules", "vendor", "venv", "__pycache__",
    "storage", "bootstrap/cache", "dist", "build", ".next"
}


def _safe_project():
    project = get_current_project_path()
    if not project:
        return None, "No current project selected. Use: use project <name-or-path>"
    return project, None


def _count_files(project: Path):
    counts = {}

    for item in project.rglob("*"):
        if any(part in SKIP_DIRS for part in item.parts):
            continue

        if item.is_file():
            suffix = item.suffix or "[no extension]"
            counts[suffix] = counts.get(suffix, 0) + 1

    return counts


def summarize_project_structure() -> str:
    project, error = _safe_project()
    if error:
        return error

    lines = [f"PROJECT STRUCTURE SUMMARY\nProject: {project}\n"]

    important_dirs = []
    important_files = []

    for item in sorted(project.iterdir()):
        if item.name in SKIP_DIRS:
            continue

        if item.is_dir():
            important_dirs.append(item.name)
        else:
            important_files.append(item.name)

    lines.append("Top-level folders:")
    lines.extend(f"- {name}" for name in important_dirs[:40])

    lines.append("\nTop-level files:")
    lines.extend(f"- {name}" for name in important_files[:40])

    counts = _count_files(project)
    lines.append("\nFile type count:")
    for ext, count in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:20]:
        lines.append(f"- {ext}: {count}")

    return "\n".join(lines)


def analyze_laravel_project() -> str:
    project, error = _safe_project()
    if error:
        return error

    indicators = {
        "artisan": project / "artisan",
        "composer.json": project / "composer.json",
        "routes/web.php": project / "routes" / "web.php",
        "routes/api.php": project / "routes" / "api.php",
        "app/Models": project / "app" / "Models",
        "app/Http/Controllers": project / "app" / "Http" / "Controllers",
        "database/migrations": project / "database" / "migrations",
        "resources/views": project / "resources" / "views",
    }

    found = [name for name, path in indicators.items() if path.exists()]

    if not found:
        return "This does not look like a Laravel project."

    lines = [f"LARAVEL PROJECT ANALYZER\nProject: {project}\n"]

    lines.append("Detected Laravel indicators:")
    lines.extend(f"- {name}" for name in found)

    composer = project / "composer.json"
    if composer.exists():
        try:
            data = json.loads(composer.read_text(errors="replace"))
            lines.append("\nComposer package name:")
            lines.append(f"- {data.get('name', 'Not defined')}")

            require = data.get("require", {})
            lines.append("\nMain PHP dependencies:")
            for package, version in list(require.items())[:20]:
                lines.append(f"- {package}: {version}")
        except Exception as e:
            lines.append(f"\ncomposer.json read error: {e}")

    return "\n".join(lines)


def analyze_react_project() -> str:
    project, error = _safe_project()
    if error:
        return error

    package_file = project / "package.json"

    if not package_file.exists():
        return "This does not look like a React/Node project. package.json not found."

    try:
        data = json.loads(package_file.read_text(errors="replace"))
    except Exception as e:
        return f"package.json read error: {e}"

    deps = {}
    deps.update(data.get("dependencies", {}))
    deps.update(data.get("devDependencies", {}))

    react_detected = "react" in deps or (project / "src").exists()

    if not react_detected:
        return "package.json found, but React was not clearly detected."

    lines = [f"REACT PROJECT ANALYZER\nProject: {project}\n"]

    lines.append("Scripts:")
    for name, script in data.get("scripts", {}).items():
        lines.append(f"- {name}: {script}")

    lines.append("\nDetected frontend dependencies:")
    for package in ["react", "react-dom", "vite", "next", "tailwindcss", "typescript", "electron"]:
        if package in deps:
            lines.append(f"- {package}: {deps[package]}")

    src = project / "src"
    if src.exists():
        components = list(src.rglob("*.jsx")) + list(src.rglob("*.tsx")) + list(src.rglob("*.js"))
        lines.append(f"\nSource files detected: {len(components)}")

    return "\n".join(lines)


def analyze_python_project() -> str:
    project, error = _safe_project()
    if error:
        return error

    indicators = [
        project / "main.py",
        project / "requirements.txt",
        project / "pyproject.toml",
        project / "setup.py",
    ]

    if not any(path.exists() for path in indicators):
        return "This does not look like a Python project."

    lines = [f"PYTHON PROJECT ANALYZER\nProject: {project}\n"]

    lines.append("Detected Python indicators:")
    for path in indicators:
        if path.exists():
            lines.append(f"- {path.name}")

    py_files = [
        file for file in project.rglob("*.py")
        if not any(part in SKIP_DIRS for part in file.parts)
    ]

    lines.append(f"\nPython files detected: {len(py_files)}")

    req = project / "requirements.txt"
    if req.exists():
        lines.append("\nrequirements.txt packages:")
        packages = [
            line.strip()
            for line in req.read_text(errors="replace").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        lines.extend(f"- {pkg}" for pkg in packages[:40])

    important_modules = ["core", "tools", "storage", "voice", "frontend"]
    lines.append("\nImportant folders:")
    for folder in important_modules:
        if (project / folder).exists():
            lines.append(f"- {folder}")

    return "\n".join(lines)


def analyze_electron_project() -> str:
    project, error = _safe_project()
    if error:
        return error

    package_file = project / "package.json"

    if not package_file.exists():
        return "This does not look like an Electron project. package.json not found."

    try:
        data = json.loads(package_file.read_text(errors="replace"))
    except Exception as e:
        return f"package.json read error: {e}"

    deps = {}
    deps.update(data.get("dependencies", {}))
    deps.update(data.get("devDependencies", {}))

    electron_detected = (
        "electron" in deps
        or (project / "electron").exists()
        or "electron" in str(data.get("scripts", {})).lower()
    )

    if not electron_detected:
        return "package.json found, but Electron was not clearly detected."

    lines = [f"ELECTRON PROJECT ANALYZER\nProject: {project}\n"]

    lines.append("Electron indicators detected.")

    lines.append("\nScripts:")
    for name, script in data.get("scripts", {}).items():
        lines.append(f"- {name}: {script}")

    if "electron" in deps:
        lines.append(f"\nElectron version: {deps['electron']}")

    electron_dir = project / "electron"
    if electron_dir.exists():
        files = list(electron_dir.rglob("*"))
        lines.append(f"\nElectron folder files detected: {len([f for f in files if f.is_file()])}")

    return "\n".join(lines)
