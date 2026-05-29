from dataclasses import dataclass
from pathlib import Path
import re
from typing import List, Optional, Pattern, Tuple

from tools.project_context_tools import get_current_project_path


@dataclass
class VulnerabilityFinding:
    severity: str
    category: str
    file: str
    line: int
    evidence: str
    remediation: str


SCANNABLE_EXTENSIONS = {
    ".py", ".php", ".js", ".ts", ".jsx", ".tsx", ".vue", ".env", ".yml", ".yaml",
}
SKIP_DIRECTORIES = {
    ".git", ".jarvis_proposals", "__pycache__", "node_modules", "vendor", "venv",
    "dist", "build", "storage",
}
MAX_FILES = 400
MAX_LINES = 5000

RULES: List[Tuple[str, str, Pattern[str], str]] = [
    (
        "CRITICAL",
        "Hardcoded secret",
        re.compile(r"(?i)\b(?:password|api[_-]?key|secret|access[_-]?token)\s*=\s*['\"][^'\"]{8,}['\"]"),
        "Move credentials to environment variables or a secrets manager and rotate exposed values.",
    ),
    (
        "HIGH",
        "Command execution",
        re.compile(r"\b(?:eval|exec|shell_exec|system)\s*\(|subprocess\.[a-z_]+\([^)]*shell\s*=\s*True"),
        "Remove dynamic command execution or strictly validate allow-listed arguments.",
    ),
    (
        "HIGH",
        "TLS verification disabled",
        re.compile(r"\bverify\s*=\s*False\b"),
        "Enable certificate verification and configure trusted certificates explicitly.",
    ),
    (
        "HIGH",
        "Unsafe SQL construction",
        re.compile(r"(?i)(?:execute|query)\s*\(\s*(?:f['\"]|['\"].*(?:%s|\\{).*)"),
        "Use bound parameters or the framework query builder rather than string interpolation.",
    ),
    (
        "MEDIUM",
        "Debug mode enabled",
        re.compile(r"(?i)\b(?:APP_DEBUG|DEBUG)\s*=\s*(?:true|1)\b"),
        "Disable debug mode outside development environments.",
    ),
]


def _skip(path: Path) -> bool:
    return any(part in SKIP_DIRECTORIES for part in path.parts)


def _redact(line: str) -> str:
    if re.search(r"(?i)(?:password|api[_-]?key|secret|access[_-]?token)\s*=", line):
        return re.sub(r"(['\"])[^'\"]+(['\"])", r"\1<redacted>\2", line.strip())
    return line.strip()[:180]


def scan_vulnerabilities(project: Optional[Path] = None) -> Tuple[Optional[Path], List[VulnerabilityFinding], Optional[str]]:
    root = Path(project).resolve() if project else get_current_project_path()
    if not root:
        return None, [], "No current project selected. Use: use project <name-or-path>"

    findings: List[VulnerabilityFinding] = []
    scanned = 0
    for file in Path(root).rglob("*"):
        if scanned >= MAX_FILES:
            break
        if _skip(file) or not file.is_file() or (
            file.suffix.lower() not in SCANNABLE_EXTENSIONS and file.name.lower() != ".env"
        ):
            continue
        if file.name == "security_scanner_tools.py":
            continue
        scanned += 1
        try:
            lines = file.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for line_number, line in enumerate(lines[:MAX_LINES], start=1):
            for severity, category, pattern, remediation in RULES:
                if pattern.search(line):
                    findings.append(VulnerabilityFinding(
                        severity=severity,
                        category=category,
                        file=str(file.relative_to(root)),
                        line=line_number,
                        evidence=_redact(line),
                        remediation=remediation,
                    ))
                    break
    ordering = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
    findings.sort(key=lambda item: ordering.get(item.severity, 0), reverse=True)
    return Path(root), findings, None


def security_vulnerability_scanner(project: Optional[Path] = None) -> str:
    root, findings, error = scan_vulnerabilities(project)
    if error:
        return error
    lines = [
        "SECURITY VULNERABILITY SCANNER - PHASE 354",
        f"Project: {root}",
        "",
        "Mode: read-only heuristic source scan.",
        f"Findings: {len(findings)}",
        "",
    ]
    if not findings:
        lines.append("No configured vulnerability patterns were detected.")
    else:
        for index, finding in enumerate(findings[:50], start=1):
            lines.extend([
                f"{index}. {finding.severity} - {finding.category}",
                f"   File: {finding.file}:{finding.line}",
                f"   Evidence: {finding.evidence}",
                f"   Remediation: {finding.remediation}",
                "",
            ])
    lines.extend([
        "Safety:",
        "- Read-only static heuristic scan; findings require manual confirmation.",
        "- Secret-like evidence is redacted in output.",
        "- No alert is emailed unless an incident is explicitly reported.",
    ])
    return "\n".join(lines)
