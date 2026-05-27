from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from tools.project_context_tools import get_current_project_path


@dataclass
class SSHConfigFinding:
    directive: str
    severity: str
    file: str
    line: int
    detail: str
    recommendation: str


INSECURE_DIRECTIVES: Dict[Tuple[str, str], Tuple[str, str, str]] = {
    ("permitrootlogin", "yes"): (
        "high",
        "Direct root SSH login is enabled.",
        "Set `PermitRootLogin no` and administer through named sudo-enabled accounts.",
    ),
    ("passwordauthentication", "yes"): (
        "medium",
        "Password authentication is enabled.",
        "Prefer key-based login and set `PasswordAuthentication no` after confirming access.",
    ),
    ("permitemptypasswords", "yes"): (
        "critical",
        "SSH accounts may authenticate with empty passwords.",
        "Set `PermitEmptyPasswords no` and audit local account credentials.",
    ),
    ("pubkeyauthentication", "no"): (
        "high",
        "Public-key authentication is disabled.",
        "Enable `PubkeyAuthentication yes` before disabling weaker login methods.",
    ),
    ("x11forwarding", "yes"): (
        "low",
        "X11 forwarding is enabled.",
        "Disable `X11Forwarding` unless graphical forwarding is explicitly required.",
    ),
}
SSH_NAMES = {"sshd_config", "ssh_config"}
SKIP = {".git", "node_modules", "vendor", "venv", "__pycache__", "storage", "dist", "build"}


def _is_ssh_config(file: Path) -> bool:
    lower = file.name.lower()
    return lower in SSH_NAMES or lower.startswith("sshd_config.") or lower.startswith("ssh_config.")


def check_ssh_configuration(
    project: Optional[Path] = None,
) -> Tuple[Optional[Path], List[SSHConfigFinding], int, Optional[str]]:
    root = Path(project).resolve() if project else get_current_project_path()
    if not root:
        return None, [], 0, "No current project selected. Use: use project <name-or-path>"

    findings: List[SSHConfigFinding] = []
    files_reviewed = 0
    for file in Path(root).rglob("*"):
        if any(part in SKIP for part in file.parts) or not file.is_file() or not _is_ssh_config(file):
            continue
        files_reviewed += 1
        try:
            lines = file.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for number, raw_line in enumerate(lines[:5000], start=1):
            line = raw_line.split("#", 1)[0].strip()
            if not line:
                continue
            pieces = line.split()
            if len(pieces) < 2:
                continue
            key, value = pieces[0].lower(), pieces[1].lower()
            rule = INSECURE_DIRECTIVES.get((key, value))
            if rule:
                severity, detail, recommendation = rule
                findings.append(SSHConfigFinding(
                    pieces[0],
                    severity,
                    str(file.relative_to(root)),
                    number,
                    detail,
                    recommendation,
                ))
    return Path(root), findings, files_reviewed, None


def ssh_configuration_checker(project: Optional[Path] = None) -> str:
    root, findings, files_reviewed, error = check_ssh_configuration(project)
    if error:
        return error
    lines = [
        "SSH CONFIGURATION CHECKER - PHASE 363",
        f"Project: {root}",
        "",
        "Mode: read-only SSH hardening review.",
        f"Configuration files reviewed: {files_reviewed}",
        f"Review points: {len(findings)}",
        "",
    ]
    for finding in findings[:80]:
        lines.extend([
            f"- {finding.severity.upper()} {finding.directive} | {finding.file}:{finding.line}",
            f"  Detail: {finding.detail}",
            f"  Recommendation: {finding.recommendation}",
        ])
    if files_reviewed == 0:
        lines.append("No SSH configuration files found in the selected project.")
    elif not findings:
        lines.append("No configured SSH hardening indicators detected.")
    lines.extend([
        "",
        "Safety:",
        "- This checker does not read live server settings unless they are included in the selected project.",
        "- No SSH configuration or service state was changed.",
    ])
    return "\n".join(lines)
