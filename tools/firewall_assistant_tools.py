from dataclasses import dataclass
from pathlib import Path
import re
from typing import List, Optional, Pattern, Tuple

from tools.project_context_tools import get_current_project_path


@dataclass
class FirewallFinding:
    firewall: str
    risk: str
    severity: str
    file: str
    line: int
    evidence: str
    recommendation: str


FIREWALL_RULES: List[Tuple[str, str, str, Pattern[str], str]] = [
    (
        "iptables",
        "Inbound default policy accepts all traffic",
        "high",
        re.compile(r"^\s*:INPUT\s+ACCEPT\b|^\s*iptables\s+-P\s+INPUT\s+ACCEPT\b", re.IGNORECASE),
        "Use a default-deny inbound policy and explicitly allow only required services.",
    ),
    (
        "iptables",
        "Unrestricted inbound accept rule",
        "high",
        re.compile(r"^\s*(?:iptables\s+)?-A\s+INPUT\s+-j\s+ACCEPT\s*$", re.IGNORECASE),
        "Restrict inbound accept rules by trusted source, interface, state, or required port.",
    ),
    (
        "nftables",
        "Inbound chain accepts traffic by default",
        "high",
        re.compile(r"\bhook\s+input\b[^;{]*\bpolicy\s+accept\b|\bpolicy\s+accept\s*;", re.IGNORECASE),
        "Set an input-chain drop policy and add narrow allow rules for required access.",
    ),
    (
        "UFW",
        "UFW default inbound policy allows traffic",
        "high",
        re.compile(r'^\s*DEFAULT_INPUT_POLICY\s*=\s*["\']ACCEPT["\']|^\s*ufw\s+default\s+allow\s+incoming\b', re.IGNORECASE),
        "Set the default incoming policy to deny and permit required services explicitly.",
    ),
    (
        "UFW",
        "Insecure remote service is exposed",
        "medium",
        re.compile(r"^\s*ufw\s+allow\s+(?:23|telnet)\b", re.IGNORECASE),
        "Remove Telnet exposure and use SSH with key-based authentication where remote access is needed.",
    ),
]
SKIP = {".git", "node_modules", "vendor", "venv", "__pycache__", "storage", "dist", "build"}


def _is_firewall_config(file: Path) -> bool:
    name = file.name.lower()
    return any(token in name for token in ("ufw", "iptables", "nftables", "firewall")) or name.endswith(".rules")


def inspect_firewall_configuration(
    project: Optional[Path] = None,
) -> Tuple[Optional[Path], List[FirewallFinding], int, Optional[str]]:
    root = Path(project).resolve() if project else get_current_project_path()
    if not root:
        return None, [], 0, "No current project selected. Use: use project <name-or-path>"

    findings: List[FirewallFinding] = []
    files_reviewed = 0
    for file in Path(root).rglob("*"):
        if any(part in SKIP for part in file.parts) or not file.is_file() or not _is_firewall_config(file):
            continue
        if file.name == "firewall_assistant_tools.py" or file.name.startswith("test_"):
            continue
        files_reviewed += 1
        try:
            lines = file.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for number, line in enumerate(lines[:5000], start=1):
            for firewall, risk, severity, pattern, recommendation in FIREWALL_RULES:
                if pattern.search(line):
                    findings.append(FirewallFinding(
                        firewall,
                        risk,
                        severity,
                        str(file.relative_to(root)),
                        number,
                        line.strip()[:180],
                        recommendation,
                    ))
    return Path(root), findings, files_reviewed, None


def firewall_assistant(project: Optional[Path] = None) -> str:
    root, findings, files_reviewed, error = inspect_firewall_configuration(project)
    if error:
        return error
    lines = [
        "FIREWALL ASSISTANT - PHASE 364",
        f"Project: {root}",
        "",
        "Mode: read-only firewall posture review.",
        f"Configuration files reviewed: {files_reviewed}",
        f"Review points: {len(findings)}",
        "",
    ]
    for finding in findings[:80]:
        lines.extend([
            f"- {finding.severity.upper()} {finding.firewall}: {finding.risk} | {finding.file}:{finding.line}",
            f"  Evidence: {finding.evidence}",
            f"  Recommendation: {finding.recommendation}",
        ])
    if files_reviewed == 0:
        lines.append("No tracked firewall configuration files found in the selected project.")
    elif not findings:
        lines.append("No configured permissive firewall indicators detected.")
    lines.extend([
        "",
        "Safety:",
        "- This assistant reviews project files only; it does not inspect live host firewall state.",
        "- No firewall rules were executed, applied, or changed.",
    ])
    return "\n".join(lines)
