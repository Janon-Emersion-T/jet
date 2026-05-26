import os
import re
import json
from pathlib import Path

from tools.project_context_tools import get_current_project_path


BUILD_DIRS = ["dist", "build", "public/build", ".next/static"]
SOURCE_EXTENSIONS = [".js", ".jsx", ".ts", ".tsx", ".vue", ".blade.php", ".html", ".css"]


def _project():
    project = get_current_project_path()
    if not project:
        return None, "No current project context set."
    return Path(project), None


def _read_text(path: Path) -> str:
    try:
        return path.read_text(errors="ignore")
    except Exception:
        return ""


def _files(project: Path, extensions=None):
    extensions = extensions or SOURCE_EXTENSIONS
    ignored = {"node_modules", ".git", "vendor", "venv", "__pycache__"}
    result = []

    for root, dirs, files in os.walk(project):
        dirs[:] = [d for d in dirs if d not in ignored]
        for file in files:
            path = Path(root) / file
            if path.suffix in extensions or file.endswith(".blade.php"):
                result.append(path)

    return result


def _format_size(size):
    if size >= 1024 * 1024:
        return f"{size / (1024 * 1024):.2f} MB"
    if size >= 1024:
        return f"{size / 1024:.2f} KB"
    return f"{size} B"


def _find_build_files(project: Path, extensions):
    found = []
    for folder in BUILD_DIRS:
        target = project / folder
        if target.exists():
            for path in target.rglob("*"):
                if path.is_file() and path.suffix in extensions:
                    found.append(path)
    return found


def vite_chunk_analyzer() -> str:
    project, error = _project()
    if error:
        return error

    manifest = project / "public" / "build" / ".vite" / "manifest.json"
    if not manifest.exists():
        manifest = project / "public" / "build" / "manifest.json"

    if not manifest.exists():
        return "VITE CHUNK ANALYZER — PHASE 271\nNo Vite manifest found. Run npm run build first."

    try:
        data = json.loads(_read_text(manifest))
    except Exception as e:
        return f"VITE CHUNK ANALYZER — PHASE 271\nFailed to read manifest: {e}"

    lines = ["VITE CHUNK ANALYZER — PHASE 271", f"Manifest: {manifest}", ""]
    chunks = []

    for key, item in data.items():
        file_name = item.get("file")
        if not file_name:
            continue
        chunk_path = manifest.parent.parent / file_name if ".vite" in str(manifest.parent) else manifest.parent / file_name
        size = chunk_path.stat().st_size if chunk_path.exists() else 0
        chunks.append((key, file_name, size))

    chunks.sort(key=lambda x: x[2], reverse=True)

    lines.append(f"Chunks detected: {len(chunks)}")
    for key, file_name, size in chunks[:30]:
        lines.append(f"- {_format_size(size)} | {file_name} | source: {key}")

    if not chunks:
        lines.append("No chunk entries found.")

    return "\n".join(lines)


def js_bundle_size_analyzer() -> str:
    project, error = _project()
    if error:
        return error

    js_files = _find_build_files(project, [".js"])
    lines = ["JS BUNDLE SIZE ANALYZER — PHASE 272", ""]

    if not js_files:
        return "\n".join(lines + ["No built JS files found. Run npm run build first."])

    total = sum(path.stat().st_size for path in js_files)
    lines.append(f"JS files found: {len(js_files)}")
    lines.append(f"Total JS size: {_format_size(total)}")
    lines.append("")
    lines.append("Largest JS bundles:")

    for path in sorted(js_files, key=lambda p: p.stat().st_size, reverse=True)[:20]:
        lines.append(f"- {_format_size(path.stat().st_size)} | {path.relative_to(project)}")

    if total > 1024 * 1024:
        lines.append("")
        lines.append("Warning: Total JS bundle is above 1 MB. Review lazy loading and vendor splitting.")

    return "\n".join(lines)


def frontend_performance_profiler() -> str:
    project, error = _project()
    if error:
        return error

    files = _files(project)
    issues = []

    patterns = [
        ("Large dependency import", r"from ['\"](lodash|moment|chart\.js|three|framer-motion)['\"]"),
        ("Console usage", r"\bconsole\.(log|warn|error)\("),
        ("Possible blocking timeout", r"setTimeout\s*\("),
        ("Heavy loop risk", r"\.map\s*\(.*\.map\s*\("),
        ("Unoptimized image tag", r"<img(?![^>]*loading=)"),
    ]

    for path in files:
        text = _read_text(path)
        rel = path.relative_to(project)
        for label, pattern in patterns:
            count = len(re.findall(pattern, text, re.S))
            if count:
                issues.append((label, rel, count))

    lines = ["FRONTEND PERFORMANCE PROFILER — PHASE 273", ""]
    if not issues:
        lines.append("No obvious frontend performance risks found.")
        return "\n".join(lines)

    for label, rel, count in issues[:60]:
        lines.append(f"- {label}: {rel} ({count})")

    return "\n".join(lines)


def tailwind_class_optimizer() -> str:
    project, error = _project()
    if error:
        return error

    files = _files(project)
    long_classes = []
    duplicate_classes = []

    for path in files:
        text = _read_text(path)
        rel = path.relative_to(project)
        matches = re.findall(r'class(Name)?=["\']([^"\']+)["\']', text)

        for _, class_text in matches:
            classes = class_text.split()
            if len(classes) > 25:
                long_classes.append((rel, len(classes), class_text[:160]))
            if len(classes) != len(set(classes)):
                duplicate_classes.append((rel, class_text[:160]))

    lines = ["TAILWIND CLASS OPTIMIZER — PHASE 274", ""]

    lines.append(f"Long class groups: {len(long_classes)}")
    for rel, count, sample in long_classes[:30]:
        lines.append(f"- {rel} | {count} classes | {sample}")

    lines.append("")
    lines.append(f"Duplicate class groups: {len(duplicate_classes)}")
    for rel, sample in duplicate_classes[:30]:
        lines.append(f"- {rel} | {sample}")

    if not long_classes and not duplicate_classes:
        lines.append("No obvious Tailwind class optimization issues found.")

    return "\n".join(lines)


def css_dead_class_detector() -> str:
    project, error = _project()
    if error:
        return error

    css_files = _files(project, [".css"])
    source_files = _files(project)

    source_text = "\n".join(_read_text(path) for path in source_files if path.suffix != ".css")
    defined_classes = set()

    for css in css_files:
        text = _read_text(css)
        for item in re.findall(r"\.([a-zA-Z_][\w-]*)", text):
            defined_classes.add(item)

    unused = sorted([cls for cls in defined_classes if cls not in source_text])

    lines = ["CSS DEAD CLASS DETECTOR — PHASE 275", ""]
    lines.append(f"CSS classes detected: {len(defined_classes)}")
    lines.append(f"Possibly unused classes: {len(unused)}")
    lines.append("")

    for cls in unused[:80]:
        lines.append(f"- .{cls}")

    if not unused:
        lines.append("No obvious dead CSS classes found.")

    lines.append("")
    lines.append("Note: Dynamic classes may create false positives.")

    return "\n".join(lines)


def accessibility_checker() -> str:
    project, error = _project()
    if error:
        return error

    files = _files(project)
    issues = []

    checks = [
        ("Image missing alt", r"<img(?![^>]*alt=)"),
        ("Button missing readable label risk", r"<button[^>]*>\s*</button>"),
        ("Input missing label risk", r"<input(?![^>]*(aria-label|id)=)"),
        ("Anchor without href", r"<a(?![^>]*href=)"),
        ("Missing lang attribute risk", r"<html(?![^>]*lang=)"),
    ]

    for path in files:
        text = _read_text(path)
        rel = path.relative_to(project)
        for label, pattern in checks:
            count = len(re.findall(pattern, text, re.I | re.S))
            if count:
                issues.append((label, rel, count))

    lines = ["ACCESSIBILITY CHECKER — PHASE 276", ""]

    if not issues:
        lines.append("No obvious accessibility issues found.")
        return "\n".join(lines)

    for label, rel, count in issues[:80]:
        lines.append(f"- {label}: {rel} ({count})")

    return "\n".join(lines)


def wcag_compliance_advisor() -> str:
    project, error = _project()
    if error:
        return error

    return "\n".join([
        "WCAG COMPLIANCE ADVISOR — PHASE 277",
        "",
        "Read-only advisory checklist:",
        "- Use semantic headings in correct order.",
        "- Every image needs meaningful alt text unless decorative.",
        "- Forms need labels, error messages, and keyboard access.",
        "- Interactive elements must be reachable using keyboard only.",
        "- Text and UI controls need sufficient color contrast.",
        "- Avoid relying only on color to communicate meaning.",
        "- Add focus-visible states for links, buttons, and inputs.",
        "- Use aria attributes only when native HTML cannot solve the issue.",
        "",
        "Recommended next upgrade: integrate axe-core or Lighthouse later as an optional external audit.",
    ])


def color_contrast_analyzer() -> str:
    project, error = _project()
    if error:
        return error

    files = _files(project, [".css", ".html", ".vue", ".jsx", ".tsx", ".blade.php"])
    colors = {}

    for path in files:
        text = _read_text(path)
        for color in re.findall(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b", text):
            colors[color.lower()] = colors.get(color.lower(), 0) + 1

    lines = ["COLOR CONTRAST ANALYZER — PHASE 278", ""]
    lines.append(f"Hard-coded hex colors found: {len(colors)}")

    for color, count in sorted(colors.items(), key=lambda x: x[1], reverse=True)[:50]:
        lines.append(f"- {color} ({count})")

    lines.append("")
    lines.append("Note: This detects color usage only. Full contrast ratio needs computed foreground/background pairs.")

    return "\n".join(lines)


def responsive_layout_analyzer() -> str:
    project, error = _project()
    if error:
        return error

    files = _files(project)
    issues = []

    checks = [
        ("Fixed width risk", r"\bw-\[[0-9]+px\]|\bwidth:\s*[0-9]+px"),
        ("Fixed height risk", r"\bh-\[[0-9]+px\]|\bheight:\s*[0-9]+px"),
        ("Overflow hidden risk", r"overflow-hidden"),
        ("Large absolute positioning risk", r"\babsolute\b"),
        ("No responsive breakpoint classes", r"class(Name)?=[\"'](?![^\"']*\b(sm|md|lg|xl|2xl):)"),
    ]

    for path in files:
        text = _read_text(path)
        rel = path.relative_to(project)
        for label, pattern in checks:
            count = len(re.findall(pattern, text, re.I | re.S))
            if count:
                issues.append((label, rel, count))

    lines = ["RESPONSIVE LAYOUT ANALYZER — PHASE 279", ""]

    if not issues:
        lines.append("No obvious responsive layout risks found.")
        return "\n".join(lines)

    for label, rel, count in issues[:80]:
        lines.append(f"- {label}: {rel} ({count})")

    return "\n".join(lines)


def mobile_first_audit() -> str:
    project, error = _project()
    if error:
        return error

    files = _files(project)
    mobile_signals = 0
    desktop_first_risks = []

    for path in files:
        text = _read_text(path)
        rel = path.relative_to(project)

        mobile_signals += len(re.findall(r"\b(sm|md|lg|xl|2xl):", text))

        if re.search(r"\bgrid-cols-[3-9]\b", text) and not re.search(r"\b(sm|md|lg|xl|2xl):grid-cols-", text):
            desktop_first_risks.append((rel, "Grid columns without responsive breakpoint"))

        if re.search(r"\bflex-row\b", text) and not re.search(r"\b(sm|md|lg|xl|2xl):flex-row\b", text):
            desktop_first_risks.append((rel, "flex-row may be desktop-first"))

    lines = ["MOBILE-FIRST AUDIT — PHASE 280", ""]
    lines.append(f"Responsive breakpoint signals: {mobile_signals}")
    lines.append(f"Desktop-first risks: {len(desktop_first_risks)}")
    lines.append("")

    for rel, issue in desktop_first_risks[:60]:
        lines.append(f"- {issue}: {rel}")

    if not desktop_first_risks:
        lines.append("No obvious mobile-first risks found.")

    return "\n".join(lines)
