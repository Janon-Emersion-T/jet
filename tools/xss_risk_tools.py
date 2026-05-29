from dataclasses import dataclass
from pathlib import Path
import re
from typing import List, Optional, Pattern, Tuple

from tools.project_context_tools import get_current_project_path


@dataclass
class XSSFinding:
    framework: str
    risk: str
    file: str
    line: int
    evidence: str
    recommendation: str


XSS_RULES: List[Tuple[str, str, Pattern[str], str]] = [
    (
        "DOM",
        "Direct innerHTML assignment",
        re.compile(r"\.innerHTML\s*="),
        "Use textContent or sanitize trusted HTML before insertion.",
    ),
    (
        "DOM",
        "document.write rendering",
        re.compile(r"\bdocument\.write\s*\("),
        "Render through safe DOM APIs rather than document.write.",
    ),
    (
        "React",
        "dangerouslySetInnerHTML sink",
        re.compile(r"\bdangerouslySetInnerHTML\s*="),
        "Avoid raw HTML or sanitize content before using this React escape hatch.",
    ),
    (
        "Vue",
        "v-html sink",
        re.compile(r"\bv-html\s*="),
        "Render text normally or sanitize values before binding to v-html.",
    ),
    (
        "Laravel Blade",
        "Unescaped Blade output",
        re.compile(r"\{!!\s*.+?\s*!!\}"),
        "Prefer escaped Blade output `{{ ... }}` unless sanitized HTML is required.",
    ),
]
EXTENSIONS = {".html", ".php", ".js", ".ts", ".jsx", ".tsx", ".vue"}
SKIP = {".git", "node_modules", "vendor", "venv", "__pycache__", "storage", "dist", "build"}


def detect_xss_risks(project: Optional[Path] = None) -> Tuple[Optional[Path], List[XSSFinding], Optional[str]]:
    root = Path(project).resolve() if project else get_current_project_path()
    if not root:
        return None, [], "No current project selected. Use: use project <name-or-path>"

    findings: List[XSSFinding] = []
    for file in Path(root).rglob("*"):
        if any(part in SKIP for part in file.parts) or not file.is_file():
            continue
        if file.suffix.lower() not in EXTENSIONS and not file.name.lower().endswith(".blade.php"):
            continue
        if file.name == "xss_risk_tools.py":
            continue
        try:
            lines = file.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for number, line in enumerate(lines[:5000], start=1):
            for framework, risk, pattern, recommendation in XSS_RULES:
                if pattern.search(line):
                    findings.append(XSSFinding(
                        framework, risk, str(file.relative_to(root)), number,
                        line.strip()[:180], recommendation,
                    ))
    return Path(root), findings, None


def xss_risk_detector(project: Optional[Path] = None) -> str:
    root, findings, error = detect_xss_risks(project)
    if error:
        return error
    lines = [
        "XSS RISK DETECTOR - PHASE 356",
        f"Project: {root}",
        "",
        "Mode: read-only rendering-sink review.",
        f"Potential sinks: {len(findings)}",
        "",
    ]
    for finding in findings[:80]:
        lines.extend([
            f"- {finding.framework}: {finding.risk} | {finding.file}:{finding.line}",
            f"  Evidence: {finding.evidence}",
            f"  Recommendation: {finding.recommendation}",
        ])
    if not findings:
        lines.append("No configured XSS sink indicators detected.")
    lines.extend([
        "",
        "Safety:",
        "- Findings identify review points; they are not confirmed exploits.",
        "- No content is rendered and no source file is changed.",
    ])
    return "\n".join(lines)
