from configparser import ConfigParser, Error as ConfigError
from dataclasses import dataclass
from pathlib import Path
import re
from typing import List, Optional, Tuple

from tools.project_context_tools import get_current_project_path


@dataclass
class Fail2banFinding:
    section: str
    directive: str
    severity: str
    file: str
    detail: str
    recommendation: str


SKIP = {".git", "node_modules", "vendor", "venv", "__pycache__", "storage", "dist", "build"}


def _is_fail2ban_config(file: Path) -> bool:
    name = file.name.lower()
    parent = file.parent.name.lower()
    return (
        name in {"jail.conf", "jail.local"}
        or (parent == "jail.d" and file.suffix.lower() in {".conf", ".local"})
        or name.startswith("fail2ban.") and file.suffix.lower() in {".conf", ".local"}
    )


def _duration_seconds(value: str) -> Optional[int]:
    match = re.fullmatch(r"\s*(\d+)\s*([smhd]?)\s*", value.lower())
    if not match:
        return None
    count = int(match.group(1))
    multiplier = {"": 1, "s": 1, "m": 60, "h": 3600, "d": 86400}[match.group(2)]
    return count * multiplier


def analyze_fail2ban(
    project: Optional[Path] = None,
) -> Tuple[Optional[Path], List[Fail2banFinding], int, Optional[str]]:
    root = Path(project).resolve() if project else get_current_project_path()
    if not root:
        return None, [], 0, "No current project selected. Use: use project <name-or-path>"

    findings: List[Fail2banFinding] = []
    files_reviewed = 0
    for file in Path(root).rglob("*"):
        if any(part in SKIP for part in file.parts) or not file.is_file() or not _is_fail2ban_config(file):
            continue
        files_reviewed += 1
        parser = ConfigParser(interpolation=None, strict=False)
        try:
            parser.read(file, encoding="utf-8")
        except (OSError, ConfigError):
            continue
        relative = str(file.relative_to(root))
        sections = ["DEFAULT"] + parser.sections()
        for section in sections:
            settings = parser.defaults() if section == "DEFAULT" else parser[section]
            ignored = settings.get("ignoreip", "")
            if "0.0.0.0/0" in ignored or "::/0" in ignored:
                findings.append(Fail2banFinding(
                    section,
                    "ignoreip",
                    "high",
                    relative,
                    "The ignore list exempts all addresses from bans.",
                    "Restrict `ignoreip` to explicitly trusted administrative sources.",
                ))

            if "ssh" not in section.lower():
                continue
            enabled = settings.get("enabled", "").strip().lower()
            if enabled in {"false", "no", "0", "off"}:
                findings.append(Fail2banFinding(
                    section,
                    "enabled",
                    "high",
                    relative,
                    "SSH brute-force protection is explicitly disabled.",
                    "Enable the SSH jail after confirming its log path and action configuration.",
                ))
            retries = settings.get("maxretry", "").strip()
            if retries.isdigit() and int(retries) > 5:
                findings.append(Fail2banFinding(
                    section,
                    "maxretry",
                    "medium",
                    relative,
                    f"SSH jail permits {retries} failed attempts before banning.",
                    "Use a lower retry threshold appropriate to legitimate administrative access.",
                ))
            seconds = _duration_seconds(settings.get("bantime", ""))
            if seconds is not None and seconds < 600:
                findings.append(Fail2banFinding(
                    section,
                    "bantime",
                    "medium",
                    relative,
                    "SSH ban duration is less than ten minutes.",
                    "Increase ban duration or use escalating bans for repeated attempts.",
                ))
    return Path(root), findings, files_reviewed, None


def fail2ban_analyzer(project: Optional[Path] = None) -> str:
    root, findings, files_reviewed, error = analyze_fail2ban(project)
    if error:
        return error
    lines = [
        "FAIL2BAN ANALYZER - PHASE 365",
        f"Project: {root}",
        "",
        "Mode: read-only Fail2ban jail configuration review.",
        f"Configuration files reviewed: {files_reviewed}",
        f"Review points: {len(findings)}",
        "",
    ]
    for finding in findings[:80]:
        lines.extend([
            f"- {finding.severity.upper()} [{finding.section}] {finding.directive} | {finding.file}",
            f"  Detail: {finding.detail}",
            f"  Recommendation: {finding.recommendation}",
        ])
    if files_reviewed == 0:
        lines.append("No tracked Fail2ban jail configuration files found in the selected project.")
    elif not findings:
        lines.append("No configured weak Fail2ban jail indicators detected.")
    lines.extend([
        "",
        "Safety:",
        "- This analyzer reviews tracked configuration only; it does not inspect active bans or logs.",
        "- No Fail2ban jail, firewall action, or service state was changed.",
    ])
    return "\n".join(lines)
