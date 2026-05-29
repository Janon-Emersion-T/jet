from dataclasses import dataclass
from pathlib import Path
import re
from typing import List, Optional, Pattern, Tuple

from tools.project_context_tools import get_current_project_path


@dataclass
class OWASPFinding:
    category: str
    severity: str
    file: str
    line: int
    evidence: str
    guidance: str


OWASP_RULES: List[Tuple[str, str, Pattern[str], str]] = [
    (
        "A01 Broken Access Control",
        "HIGH",
        re.compile(r"(?i)(?:route|app)\.(?:delete|post|put|patch)\([^\\n]*(?:admin|users|delete)[^\\n]*\)"),
        "Verify authentication and authorization middleware protects state-changing routes.",
    ),
    (
        "A02 Cryptographic Failures",
        "HIGH",
        re.compile(r"(?i)\b(?:md5|sha1)\s*\(|verify\s*=\s*False|(?:password|secret|token)\s*=\s*['\"][^'\"]{6,}['\"]"),
        "Use modern cryptography, TLS verification, and secret storage outside source code.",
    ),
    (
        "A03 Injection",
        "CRITICAL",
        re.compile(r"(?i)\b(?:eval|exec|shell_exec|system)\s*\(|(?:execute|query)\s*\(\s*f['\"]"),
        "Avoid dynamic execution and parameterize all database operations.",
    ),
    (
        "A05 Security Misconfiguration",
        "MEDIUM",
        re.compile(r"(?i)\b(?:APP_DEBUG|DEBUG)\s*=\s*(?:true|1)\b|allow_origins\s*=\s*\[\s*['\"]\*['\"]"),
        "Disable debug and restrictive-origin exceptions outside local development.",
    ),
    (
        "A07 Identification and Authentication Failures",
        "HIGH",
        re.compile(r"(?i)(?:jwt|session|cookie).*(?:verify\s*=\s*False|secure\s*=\s*False)"),
        "Enforce token verification and secure session/cookie attributes.",
    ),
]
EXTENSIONS = {".py", ".php", ".js", ".ts", ".jsx", ".tsx", ".vue", ".yml", ".yaml"}
SKIP = {".git", "node_modules", "vendor", "venv", "__pycache__", "storage", "dist", "build"}


def _redact(text: str) -> str:
    if re.search(r"(?i)(?:password|secret|token)\s*=", text):
        return re.sub(r"(['\"])[^'\"]+(['\"])", r"\1<redacted>\2", text.strip())
    return text.strip()[:180]


def analyze_owasp(project: Optional[Path] = None) -> Tuple[Optional[Path], List[OWASPFinding], Optional[str]]:
    root = Path(project).resolve() if project else get_current_project_path()
    if not root:
        return None, [], "No current project selected. Use: use project <name-or-path>"

    findings: List[OWASPFinding] = []
    for file in Path(root).rglob("*"):
        if any(part in SKIP for part in file.parts) or not file.is_file():
            continue
        if file.suffix.lower() not in EXTENSIONS and file.name.lower() != ".env":
            continue
        if file.name in {"owasp_analyzer_tools.py", "security_scanner_tools.py"}:
            continue
        try:
            lines = file.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for number, line in enumerate(lines[:5000], start=1):
            for category, severity, pattern, guidance in OWASP_RULES:
                if pattern.search(line):
                    findings.append(OWASPFinding(
                        category, severity, str(file.relative_to(root)), number,
                        _redact(line), guidance,
                    ))
                    break
    weight = {"CRITICAL": 3, "HIGH": 2, "MEDIUM": 1}
    findings.sort(key=lambda item: weight[item.severity], reverse=True)
    return Path(root), findings, None


def owasp_analyzer(project: Optional[Path] = None) -> str:
    root, findings, error = analyze_owasp(project)
    if error:
        return error
    lines = [
        "OWASP ANALYZER - PHASE 355",
        f"Project: {root}",
        "",
        "Mode: read-only OWASP-oriented heuristic review.",
        f"Findings: {len(findings)}",
        "",
    ]
    for item in findings[:60]:
        lines.extend([
            f"- {item.severity} | {item.category} | {item.file}:{item.line}",
            f"  Evidence: {item.evidence}",
            f"  Guidance: {item.guidance}",
        ])
    if not findings:
        lines.append("No configured OWASP indicators detected.")
    lines.extend([
        "",
        "Safety:",
        "- This is static heuristic screening, not proof of exploitability.",
        "- Sensitive evidence is redacted and no files are changed.",
    ])
    return "\n".join(lines)
