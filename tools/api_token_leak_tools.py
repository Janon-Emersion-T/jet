from dataclasses import dataclass
from pathlib import Path
import re
from typing import List, Optional, Pattern, Tuple

from tools.project_context_tools import get_current_project_path


@dataclass
class APITokenFinding:
    provider: str
    severity: str
    file: str
    line: int
    evidence: str
    recommendation: str


TOKEN_RULES: List[Tuple[str, str, Pattern[str], str]] = [
    (
        "GitHub",
        "critical",
        re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})"),
        "Revoke the token, replace it in a secret store, and review access logs.",
    ),
    (
        "Stripe live secret",
        "critical",
        re.compile(r"\bsk_live_[A-Za-z0-9]{16,}"),
        "Rotate the live key immediately and remove it from source/history.",
    ),
    (
        "Slack",
        "high",
        re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{16,}"),
        "Revoke the token and store the replacement outside tracked content.",
    ),
    (
        "Generic API token",
        "high",
        re.compile(
            r"(?i)\b(?:api[_-]?token|api[_-]?key|access[_-]?token)\b\s*[:=]\s*"
            r"['\"]([A-Za-z0-9_\-]{16,})['\"]"
        ),
        "Move credentials to environment/secret management and rotate exposed values.",
    ),
]
EXTENSIONS = {".py", ".php", ".js", ".ts", ".jsx", ".tsx", ".json", ".yaml", ".yml", ".ini", ".env"}
SPECIAL_FILES = {".env", ".env.local", ".env.production", ".env.staging"}
SKIP = {".git", "node_modules", "vendor", "venv", "__pycache__", "storage", "dist", "build"}


def _redact_token_evidence(line: str) -> str:
    evidence = line.strip()[:220]
    for _, _, pattern, _ in TOKEN_RULES:
        evidence = pattern.sub("<redacted-api-token>", evidence)
    return evidence


def detect_api_token_leaks(
    project: Optional[Path] = None,
) -> Tuple[Optional[Path], List[APITokenFinding], Optional[str]]:
    root = Path(project).resolve() if project else get_current_project_path()
    if not root:
        return None, [], "No current project selected. Use: use project <name-or-path>"

    findings: List[APITokenFinding] = []
    for file in Path(root).rglob("*"):
        if any(part in SKIP for part in file.parts) or not file.is_file():
            continue
        if file.suffix.lower() not in EXTENSIONS and file.name.lower() not in SPECIAL_FILES:
            continue
        if file.name in {"api_token_leak_tools.py"} or file.name.startswith("test_"):
            continue
        try:
            lines = file.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for number, line in enumerate(lines[:10000], start=1):
            for provider, severity, pattern, recommendation in TOKEN_RULES:
                if pattern.search(line):
                    findings.append(APITokenFinding(
                        provider,
                        severity,
                        str(file.relative_to(root)),
                        number,
                        _redact_token_evidence(line),
                        recommendation,
                    ))
    return Path(root), findings, None


def api_token_leak_detector(project: Optional[Path] = None) -> str:
    root, findings, error = detect_api_token_leaks(project)
    if error:
        return error
    lines = [
        "API TOKEN LEAK DETECTOR - PHASE 361",
        f"Project: {root}",
        "",
        "Mode: read-only credential exposure review with redacted output.",
        f"Potential leaks: {len(findings)}",
        "",
    ]
    for finding in findings[:80]:
        lines.extend([
            f"- {finding.severity.upper()} {finding.provider} token | {finding.file}:{finding.line}",
            f"  Evidence: {finding.evidence}",
            f"  Recommendation: {finding.recommendation}",
        ])
    if not findings:
        lines.append("No configured API token indicators detected.")
    lines.extend([
        "",
        "Safety:",
        "- Suspected token values are redacted from this output.",
        "- No credentials are verified, transmitted, rotated, or modified.",
    ])
    return "\n".join(lines)
