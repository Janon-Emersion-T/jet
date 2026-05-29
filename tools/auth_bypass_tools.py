from dataclasses import dataclass
from pathlib import Path
import re
from typing import List, Optional, Pattern, Tuple

from tools.project_context_tools import get_current_project_path


@dataclass
class AuthBypassFinding:
    framework: str
    risk: str
    severity: str
    file: str
    line: int
    evidence: str
    recommendation: str


AUTH_BYPASS_RULES: List[Tuple[str, str, str, Pattern[str], str]] = [
    (
        "Laravel",
        "Authentication middleware removed",
        "high",
        re.compile(r"\bwithoutMiddleware\s*\([^)\n]*(?:auth|authenticate)", re.IGNORECASE),
        "Retain authentication middleware for protected routes and document narrowly scoped exceptions.",
    ),
    (
        "Laravel",
        "Sensitive mutation route without visible auth middleware",
        "medium",
        re.compile(
            r"^(?!.*middleware\s*\([^)]*auth).*Route::(?:post|put|patch|delete)"
            r"\s*\([^;\n]*(?:admin|users?|account)",
            re.IGNORECASE,
        ),
        "Attach authentication and authorization middleware to privileged mutation routes.",
    ),
    (
        "Express",
        "Sensitive mutation handler without visible auth middleware",
        "medium",
        re.compile(
            r"\b(?:app|router)\.(?:post|put|patch|delete)\s*\(\s*['\"]/(?:admin|users?|account)"
            r"[^,\n]*,\s*(?:async\s+)?\(?\s*(?:req|request)\b",
            re.IGNORECASE,
        ),
        "Place verified authentication and authorization middleware before the handler.",
    ),
    (
        "Application config",
        "Authentication disabled by configuration",
        "high",
        re.compile(r"\b(?:disable_auth|auth_disabled|allow_unauthenticated)\s*=\s*(?:true|1)\b", re.IGNORECASE),
        "Do not ship authentication bypass switches enabled outside controlled test environments.",
    ),
]
EXTENSIONS = {".py", ".php", ".js", ".ts", ".jsx", ".tsx"}
SKIP = {".git", "node_modules", "vendor", "venv", "__pycache__", "storage", "dist", "build"}


def analyze_auth_bypass(
    project: Optional[Path] = None,
) -> Tuple[Optional[Path], List[AuthBypassFinding], Optional[str]]:
    root = Path(project).resolve() if project else get_current_project_path()
    if not root:
        return None, [], "No current project selected. Use: use project <name-or-path>"

    findings: List[AuthBypassFinding] = []
    for file in Path(root).rglob("*"):
        if any(part in SKIP for part in file.parts) or not file.is_file():
            continue
        if file.suffix.lower() not in EXTENSIONS or file.name.startswith("test_"):
            continue
        if file.name == "auth_bypass_tools.py":
            continue
        try:
            lines = file.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for number, line in enumerate(lines[:5000], start=1):
            for framework, risk, severity, pattern, recommendation in AUTH_BYPASS_RULES:
                if pattern.search(line):
                    findings.append(AuthBypassFinding(
                        framework,
                        risk,
                        severity,
                        str(file.relative_to(root)),
                        number,
                        line.strip()[:180],
                        recommendation,
                    ))
    return Path(root), findings, None


def auth_bypass_analyzer(project: Optional[Path] = None) -> str:
    root, findings, error = analyze_auth_bypass(project)
    if error:
        return error
    lines = [
        "AUTH BYPASS ANALYZER - PHASE 359",
        f"Project: {root}",
        "",
        "Mode: read-only authentication-control review.",
        f"Review points: {len(findings)}",
        "",
    ]
    for finding in findings[:80]:
        lines.extend([
            f"- {finding.severity.upper()} {finding.framework}: {finding.risk} | {finding.file}:{finding.line}",
            f"  Evidence: {finding.evidence}",
            f"  Recommendation: {finding.recommendation}",
        ])
    if not findings:
        lines.append("No configured authentication bypass indicators detected.")
    lines.extend([
        "",
        "Safety:",
        "- Static indicators require manual verification of middleware and authorization flow.",
        "- No routes, permissions, or authentication configuration were changed.",
    ])
    return "\n".join(lines)
