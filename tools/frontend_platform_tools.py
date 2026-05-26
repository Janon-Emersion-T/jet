from pathlib import Path
import json
import re

from tools.project_context_tools import get_current_project_path

SKIP_DIRS = {
    ".git", "node_modules", "vendor", "venv", "__pycache__",
    "storage", "bootstrap/cache", "dist", "build", ".next", ".astro"
}

FRONTEND_EXTENSIONS = {".js", ".jsx", ".ts", ".tsx", ".vue", ".astro"}


def _project():
    project = get_current_project_path()
    if not project:
        return None, "No current project selected.\nUse: use project <path-or-shortcut>"
    return Path(project), None


def _skip(path: Path):
    return any(part in SKIP_DIRS for part in path.parts)


def _files(project: Path, suffixes=None):
    suffixes = suffixes or FRONTEND_EXTENSIONS
    return [
        file for file in project.rglob("*")
        if file.is_file() and file.suffix.lower() in suffixes and not _skip(file)
    ]


def _read(path: Path):
    return path.read_text(errors="replace")


def _package(project: Path):
    package = project / "package.json"
    if not package.exists():
        return {}
    try:
        return json.loads(package.read_text(errors="replace"))
    except Exception:
        return {}


def _deps(project: Path):
    data = _package(project)
    deps = {}
    deps.update(data.get("dependencies", {}))
    deps.update(data.get("devDependencies", {}))
    return deps


def ui_consistency_checker():
    project, error = _project()
    if error:
        return error

    findings = []
    class_groups = {}

    for file in _files(project, {".jsx", ".tsx", ".js", ".ts", ".vue", ".astro"}):
        text = _read(file)
        class_values = re.findall(r'className=["`]([^"`]+)["`]|class=["`]([^"`]+)["`]', text)
        for pair in class_values:
            value = pair[0] or pair[1]
            tokens = value.split()
            for token in tokens:
                if token.startswith(("text-", "bg-", "p-", "px-", "py-", "m-", "rounded", "shadow")):
                    class_groups.setdefault(token, set()).add(str(file.relative_to(project)))

        if "style={{" in text:
            findings.append(f"- Inline React style found: {file.relative_to(project)}")
        if re.search(r'#[0-9a-fA-F]{3,6}', text):
            findings.append(f"- Hardcoded hex color found: {file.relative_to(project)}")
        if "px]" in text or re.search(r"\[\d+px\]", text):
            findings.append(f"- Arbitrary pixel Tailwind value found: {file.relative_to(project)}")

    repeated = [
        f"- Repeated utility `{token}` used in {len(paths)} files"
        for token, paths in class_groups.items()
        if len(paths) >= 8
    ]

    output = ["UI CONSISTENCY CHECKER — PHASE 281"]
    output.append("\nFindings:")
    output.extend(findings[:80] if findings else ["- No obvious UI consistency risks found."])
    output.append("\nReusable style signals:")
    output.extend(repeated[:40] if repeated else ["- No major repeated utility pattern detected."])
    return "\n".join(output)


def component_reuse_analyzer():
    project, error = _project()
    if error:
        return error

    files = _files(project, {".jsx", ".tsx", ".vue", ".astro"})
    components = []
    large_files = []

    for file in files:
        text = _read(file)
        name = file.stem
        exports = re.findall(r"export\s+default\s+function\s+(\w+)|function\s+(\w+)\s*\(", text)
        component_name = exports[0][0] or exports[0][1] if exports else name
        lines = len(text.splitlines())

        components.append((component_name, file.relative_to(project), lines))

        if lines > 250:
            large_files.append(f"- Large component candidate: {file.relative_to(project)} ({lines} lines)")

    duplicate_names = {}
    for name, path, _ in components:
        duplicate_names.setdefault(name.lower(), []).append(str(path))

    duplicates = [
        f"- Component name `{name}` appears in: {', '.join(paths[:5])}"
        for name, paths in duplicate_names.items()
        if len(paths) > 1
    ]

    output = ["COMPONENT REUSE ANALYZER — PHASE 282"]
    output.append(f"Components/files detected: {len(components)}")
    output.append("\nLarge components:")
    output.extend(large_files[:60] if large_files else ["- No oversized component files found."])
    output.append("\nPossible duplicate component names:")
    output.extend(duplicates[:40] if duplicates else ["- No obvious duplicate component names found."])
    return "\n".join(output)


def framer_motion_assistant():
    project, error = _project()
    if error:
        return error

    deps = _deps(project)
    installed = "framer-motion" in deps or "motion" in deps
    motion_files = []

    for file in _files(project, {".jsx", ".tsx", ".js", ".ts"}):
        text = _read(file)
        if "framer-motion" in text or "motion." in text or "<motion." in text:
            motion_files.append(f"- {file.relative_to(project)}")

    output = ["FRAMER MOTION ASSISTANT — PHASE 283"]
    output.append(f"framer-motion installed: {'YES' if installed else 'NO'}")
    output.append("\nMotion usage:")
    output.extend(motion_files[:60] if motion_files else ["- No Framer Motion usage detected."])
    output.append("\nSafe recommendation:")
    if installed:
        output.append("- Keep animations reusable with shared variants and avoid heavy page-wide motion.")
    else:
        output.append("- Add only when animation is needed. Do not install blindly.")
    return "\n".join(output)


def react_state_analyzer():
    project, error = _project()
    if error:
        return error

    findings = []

    for file in _files(project, {".jsx", ".tsx", ".js", ".ts"}):
        text = _read(file)
        use_state = len(re.findall(r"\buseState\s*\(", text))
        use_effect = len(re.findall(r"\buseEffect\s*\(", text))
        prop_drilling = len(re.findall(r"\bprops\.", text))

        if use_state >= 6:
            findings.append(f"- Heavy local state: {file.relative_to(project)} uses useState {use_state} times")
        if use_effect >= 4:
            findings.append(f"- Heavy side effects: {file.relative_to(project)} uses useEffect {use_effect} times")
        if prop_drilling >= 10:
            findings.append(f"- Possible prop drilling: {file.relative_to(project)} has {prop_drilling} props references")
        if "useEffect(" in text and "[]" not in text:
            findings.append(f"- Review useEffect dependencies: {file.relative_to(project)}")

    output = ["REACT STATE ANALYZER — PHASE 284"]
    output.extend(findings[:100] if findings else ["No obvious React state risks found."])
    return "\n".join(output)


def zustand_redux_analyzer():
    project, error = _project()
    if error:
        return error

    deps = _deps(project)
    has_zustand = "zustand" in deps
    has_redux = any(key in deps for key in ["redux", "@reduxjs/toolkit", "react-redux"])
    findings = []

    for file in _files(project, {".js", ".jsx", ".ts", ".tsx"}):
        text = _read(file)
        if "create(" in text and "zustand" in text:
            findings.append(f"- Zustand store usage: {file.relative_to(project)}")
        if "createSlice" in text or "configureStore" in text:
            findings.append(f"- Redux Toolkit usage: {file.relative_to(project)}")
        if "useSelector" in text or "useDispatch" in text:
            findings.append(f"- Redux hook usage: {file.relative_to(project)}")

    output = ["ZUSTAND / REDUX ANALYZER — PHASE 285"]
    output.append(f"Zustand dependency: {'YES' if has_zustand else 'NO'}")
    output.append(f"Redux dependency: {'YES' if has_redux else 'NO'}")
    output.append("\nDetected usage:")
    output.extend(findings[:100] if findings else ["- No Zustand/Redux usage detected."])
    return "\n".join(output)


def vue_component_analyzer():
    project, error = _project()
    if error:
        return error

    files = _files(project, {".vue"})
    if not files:
        return "VUE COMPONENT ANALYZER — PHASE 286\nNo Vue component files found."

    findings = []
    for file in files:
        text = _read(file)
        if "<script setup" in text:
            mode = "script setup"
        elif "<script" in text:
            mode = "classic script"
        else:
            mode = "template only"

        if text.count("<template") != text.count("</template>"):
            findings.append(f"- Template mismatch risk: {file.relative_to(project)}")
        if "v-html" in text:
            findings.append(f"- v-html security review needed: {file.relative_to(project)}")

        findings.append(f"- {file.relative_to(project)} | {mode}")

    return "VUE COMPONENT ANALYZER — PHASE 286\n" + "\n".join(findings[:120])


def astro_project_analyzer():
    project, error = _project()
    if error:
        return error

    deps = _deps(project)
    astro_config = any((project / name).exists() for name in ["astro.config.mjs", "astro.config.js", "astro.config.ts"])
    astro_files = _files(project, {".astro"})

    output = ["ASTRO PROJECT ANALYZER — PHASE 287"]
    output.append(f"Astro dependency: {'YES' if 'astro' in deps else 'NO'}")
    output.append(f"Astro config found: {'YES' if astro_config else 'NO'}")
    output.append(f"Astro files found: {len(astro_files)}")

    if astro_files:
        output.append("\nAstro pages/components:")
        output.extend(f"- {file.relative_to(project)}" for file in astro_files[:80])

    return "\n".join(output)


def nextjs_analyzer():
    project, error = _project()
    if error:
        return error

    deps = _deps(project)
    has_next = "next" in deps
    app_dir = project / "app"
    pages_dir = project / "pages"
    next_config = any((project / name).exists() for name in ["next.config.js", "next.config.mjs", "next.config.ts"])

    findings = []
    if app_dir.exists():
        findings.append("- App Router detected: app/")
    if pages_dir.exists():
        findings.append("- Pages Router detected: pages/")
    if app_dir.exists() and pages_dir.exists():
        findings.append("- Mixed App Router and Pages Router. Review routing strategy.")
    if not next_config:
        findings.append("- next.config file not found.")

    route_files = []
    for pattern in ["page.*", "layout.*", "route.*"]:
        route_files.extend(app_dir.rglob(pattern) if app_dir.exists() else [])

    output = ["NEXT.JS ANALYZER — PHASE 288"]
    output.append(f"Next.js dependency: {'YES' if has_next else 'NO'}")
    output.append(f"Next config found: {'YES' if next_config else 'NO'}")
    output.append("\nFindings:")
    output.extend(findings if findings else ["- No obvious Next.js structure risks found."])
    output.append(f"\nApp route files detected: {len(route_files)}")
    output.extend(f"- {file.relative_to(project)}" for file in route_files[:80])
    return "\n".join(output)


def electron_packaging_assistant():
    project, error = _project()
    if error:
        return error

    deps = _deps(project)
    package = _package(project)
    scripts = package.get("scripts", {})
    has_electron = "electron" in deps
    has_builder = "electron-builder" in deps
    has_forge = "@electron-forge/cli" in deps

    output = ["ELECTRON PACKAGING ASSISTANT — PHASE 289"]
    output.append(f"Electron dependency: {'YES' if has_electron else 'NO'}")
    output.append(f"electron-builder: {'YES' if has_builder else 'NO'}")
    output.append(f"electron-forge: {'YES' if has_forge else 'NO'}")
    output.append("\nPackage scripts:")
    output.extend(f"- npm run {name}: {cmd}" for name, cmd in scripts.items())
    output.append("\nSafe recommendation:")
    output.append("- This phase is read-only. Packaging commands must be added later as confirm-based actions.")
    return "\n".join(output)


def cross_platform_build_helper():
    project, error = _project()
    if error:
        return error

    package = _package(project)
    scripts = package.get("scripts", {})
    findings = []

    for name, cmd in scripts.items():
        if "rm -rf" in cmd:
            findings.append(f"- Unix-only cleanup command in script `{name}`")
        if "cp " in cmd:
            findings.append(f"- Unix-only copy command in script `{name}`")
        if "export " in cmd:
            findings.append(f"- Unix-only environment variable syntax in script `{name}`")
        if "\\" in cmd:
            findings.append(f"- Windows-style path usage in script `{name}`")

    output = ["CROSS-PLATFORM BUILD HELPER — PHASE 290"]
    output.append("Build portability findings:")
    output.extend(findings[:80] if findings else ["- No obvious cross-platform script risks found."])
    output.append("\nRecommendation:")
    output.append("- Prefer Node-based scripts, cross-env, rimraf, and path-safe tooling for Windows/Linux/macOS compatibility.")
    return "\n".join(output)
