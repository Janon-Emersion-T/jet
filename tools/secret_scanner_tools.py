from dataclasses import dataclass
from pathlib import Path
import re
from typing import List, Optional, Pattern, Tuple

from tools.project_context_tools import get_current_project_path


@dataclass
class SecretFinding:
    secret_type: str
    severity: str
    file: str
    line: int
    evidence: str
    recommendation: str


SECRET_RULES: List[Tuple[str, str, Pattern[str], str]] = [
    (
        "Private key material",
        "critical",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "Remove private keys from project files, replace the key, and store it in secured key management.",
    ),
    (
        "AWS access key identifier",
        "critical",
        re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        "Disable or rotate the associated credential and review cloud access activity.",
    ),
    (
        "Embedded credential assignment",
        "high",
        re.compile(
            r"(?i)\b(?:db_password|database_password|password|secret_key|client_secret)\b\s*[:=]\s*"
            r"['\"]([^'\"]{8,})['\"]"
        ),
        "Move secret values to a protected environment or secret manager and rotate exposed credentials.",
    ),
    (
        "Credential in database URL",
        "high",
        re.compile(r"(?i)\b(?:mysql|postgres(?:ql)?|mongodb(?:\+srv)?)://[^:\s/]+:[^@\s/]+@"),
        "Use a secret-backed database URL and rotate the exposed database password.",
    ),
]
EXTENSIONS = {
    ".py", ".php", ".js", ".ts", ".jsx", ".tsx", ".json", ".yaml", ".yml",
    ".ini", ".conf", ".config", ".pem", ".key",
}
SPECIAL_FILES = {".env", ".env.local", ".env.production", ".env.staging"}
SKIP = {".git", "node_modules", "vendor", "venv", "__pycache__", "storage", "dist", "build"}


def _redact_secret_evidence(line: str) -> str:
    evidence = line.strip()[:220]
    for _, _, pattern, _ in SECRET_RULES:
        evidence = pattern.sub("<redacted-secret>", evidence)
    return evidence


def scan_secrets(
    project: Optional[Path] = None,
) -> Tuple[Optional[Path], List[SecretFinding], Optional[str]]:
    root = Path(project).resolve() if project else get_current_project_path()
    if not root:
        return None, [], "No current project selected. Use: use project <name-or-path>"

    findings: List[SecretFinding] = []
    for file in Path(root).rglob("*"):
        if any(part in SKIP for part in file.parts) or not file.is_file():
            continue
        if file.suffix.lower() not in EXTENSIONS and file.name.lower() not in SPECIAL_FILES:
            continue
        if file.name == "secret_scanner_tools.py" or file.name.startswith("test_"):
            continue
        try:
            lines = file.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for number, line in enumerate(lines[:10000], start=1):
            for secret_type, severity, pattern, recommendation in SECRET_RULES:
                if pattern.search(line):
                    findings.append(SecretFinding(
                        secret_type,
                        severity,
                        str(file.relative_to(root)),
                        number,
                        _redact_secret_evidence(line),
                        recommendation,
                    ))
    return Path(root), findings, None


def secret_scanner(project: Optional[Path] = None) -> str:
    root, findings, error = scan_secrets(project)
    if error:
        return error
    lines = [
        "SECRET SCANNER - PHASE 362",
        f"Project: {root}",
        "",
        "Mode: read-only secret exposure review with redacted output.",
        f"Potential secrets: {len(findings)}",
        "",
    ]
    for finding in findings[:80]:
        lines.extend([
            f"- {finding.severity.upper()} {finding.secret_type} | {finding.file}:{finding.line}",
            f"  Evidence: {finding.evidence}",
            f"  Recommendation: {finding.recommendation}",
        ])
    if not findings:
        lines.append("No configured secret indicators detected.")
    lines.extend([
        "",
        "Safety:",
        "- Suspected secret values are redacted from this output.",
        "- No credentials are accessed, validated, transmitted, or modified.",
    ])
    return "\n".join(lines)
