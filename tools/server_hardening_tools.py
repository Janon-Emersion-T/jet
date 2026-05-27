from dataclasses import dataclass
from pathlib import Path
import re
from typing import List, Optional, Pattern, Tuple

from tools.project_context_tools import get_current_project_path


@dataclass
class ServerHardeningFinding:
    area: str
    risk: str
    severity: str
    file: str
    line: int
    evidence: str
    recommendation: str


HARDENING_RULES: List[Tuple[str, str, str, Pattern[str], str]] = [
    (
        "Kernel network",
        "IPv4 forwarding is enabled",
        "medium",
        re.compile(r"^\s*net\.ipv4\.ip_forward\s*=\s*1\s*$", re.IGNORECASE),
        "Disable IP forwarding unless the host is intentionally acting as a router or gateway.",
    ),
    (
        "Kernel network",
        "SYN cookie protection is disabled",
        "high",
        re.compile(r"^\s*net\.ipv4\.tcp_syncookies\s*=\s*0\s*$", re.IGNORECASE),
        "Enable `net.ipv4.tcp_syncookies = 1` for baseline SYN flood resistance.",
    ),
    (
        "Kernel visibility",
        "Kernel pointer exposure is relaxed",
        "medium",
        re.compile(r"^\s*kernel\.kptr_restrict\s*=\s*0\s*$", re.IGNORECASE),
        "Set `kernel.kptr_restrict = 2` on production hosts where operationally compatible.",
    ),
    (
        "Nginx",
        "Server version disclosure is enabled",
        "low",
        re.compile(r"^\s*server_tokens\s+on\s*;", re.IGNORECASE),
        "Set `server_tokens off;` to reduce unnecessary version disclosure.",
    ),
    (
        "Apache",
        "Verbose server signature is enabled",
        "low",
        re.compile(r"^\s*ServerSignature\s+On\b", re.IGNORECASE),
        "Set `ServerSignature Off` and minimize public server version detail.",
    ),
    (
        "PHP",
        "PHP version exposure is enabled",
        "low",
        re.compile(r"^\s*expose_php\s*=\s*On\b", re.IGNORECASE),
        "Set `expose_php = Off` for public production deployments.",
    ),
]
SKIP = {".git", "node_modules", "vendor", "venv", "__pycache__", "storage", "dist", "build"}


def _is_hardening_config(file: Path) -> bool:
    name = file.name.lower()
    return (
        "sysctl" in name
        or "nginx" in name
        or "apache" in name
        or name in {"httpd.conf", "php.ini"}
        or name.endswith(".sysctl")
    )


def assess_server_hardening(
    project: Optional[Path] = None,
) -> Tuple[Optional[Path], List[ServerHardeningFinding], int, Optional[str]]:
    root = Path(project).resolve() if project else get_current_project_path()
    if not root:
        return None, [], 0, "No current project selected. Use: use project <name-or-path>"

    findings: List[ServerHardeningFinding] = []
    files_reviewed = 0
    for file in Path(root).rglob("*"):
        if any(part in SKIP for part in file.parts) or not file.is_file() or not _is_hardening_config(file):
            continue
        if file.name == "server_hardening_tools.py" or file.name.startswith("test_"):
            continue
        files_reviewed += 1
        try:
            lines = file.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for number, line in enumerate(lines[:5000], start=1):
            for area, risk, severity, pattern, recommendation in HARDENING_RULES:
                if pattern.search(line):
                    findings.append(ServerHardeningFinding(
                        area,
                        risk,
                        severity,
                        str(file.relative_to(root)),
                        number,
                        line.strip()[:180],
                        recommendation,
                    ))
    return Path(root), findings, files_reviewed, None


def server_hardening_advisor(project: Optional[Path] = None) -> str:
    root, findings, files_reviewed, error = assess_server_hardening(project)
    if error:
        return error
    lines = [
        "SERVER HARDENING ADVISOR - PHASE 366",
        f"Project: {root}",
        "",
        "Mode: read-only host configuration hardening review.",
        f"Configuration files reviewed: {files_reviewed}",
        f"Review points: {len(findings)}",
        "",
    ]
    for finding in findings[:80]:
        lines.extend([
            f"- {finding.severity.upper()} {finding.area}: {finding.risk} | {finding.file}:{finding.line}",
            f"  Evidence: {finding.evidence}",
            f"  Recommendation: {finding.recommendation}",
        ])
    if files_reviewed == 0:
        lines.append("No tracked sysctl, web-server, or PHP hardening configuration files were found.")
    elif not findings:
        lines.append("No configured server hardening indicators detected.")
    lines.extend([
        "",
        "Companion reviews:",
        "- Use `ssh configuration checker`, `firewall assistant`, and `fail2ban analyzer` for focused controls.",
        "",
        "Safety:",
        "- This advisor reviews tracked configuration only; it does not inspect a live host.",
        "- No system setting, service, package, or firewall rule was changed.",
    ])
    return "\n".join(lines)
