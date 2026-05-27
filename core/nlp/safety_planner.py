from dataclasses import asdict, dataclass, field
from datetime import datetime
import json
from pathlib import Path
import re
from typing import Dict, List, Optional


AUDIT_FILE = Path("storage/nlp/audit_trail.jsonl")
DANGEROUS_RULES = {
    r"\brm\s+-rf\b": "Recursive forced deletion can irreversibly remove files.",
    r"\b(?:drop|truncate)\s+(?:database|table)\b": "This can permanently destroy stored data.",
    r"\bmkfs\b|\bformat\s+(?:disk|drive)\b": "Formatting destroys filesystem contents.",
    r"\bdd\s+if=": "Raw disk writes can overwrite a disk or partition.",
    r"\bshutdown\b|\breboot\b": "This interrupts running services and active work.",
    r"\bforce\s+push\b|\bgit\s+push\s+.*--force": "Force pushing can overwrite shared history.",
}
WRITE_WORDS = {"write", "edit", "update", "delete", "remove", "deploy", "send", "apply", "install", "restart"}
READ_WORDS = {"show", "list", "read", "review", "inspect", "check", "search", "analyze", "status"}
ROLE_PERMISSIONS = {
    "viewer": {"read"},
    "operator": {"read", "write"},
    "admin": {"read", "write", "dangerous"},
}


@dataclass
class SafetyDecision:
    action_type: str
    safety_level: str
    requires_confirmation: bool
    allowed: bool
    reasons: List[str] = field(default_factory=list)
    alternatives: List[str] = field(default_factory=list)
    required_permission: str = "read"
    user_role: str = "operator"


def classify_action(text: str) -> str:
    words = set(re.findall(r"[a-z]+", (text or "").lower()))
    if words & WRITE_WORDS:
        return "write"
    if words & READ_WORDS:
        return "read"
    return "read"


def explain_danger(text: str) -> List[str]:
    return [reason for pattern, reason in DANGEROUS_RULES.items() if re.search(pattern, text or "", re.I)]


def suggest_safe_alternatives(text: str, reasons: List[str]) -> List[str]:
    lowered = (text or "").lower()
    alternatives = []
    if "rm " in lowered or "delete" in lowered or "remove" in lowered:
        alternatives.append("List the matching files first, then delete only explicitly confirmed targets.")
    if "drop " in lowered or "truncate " in lowered:
        alternatives.append("Create a database backup and preview affected tables before making schema changes.")
    if "force" in lowered and "push" in lowered:
        alternatives.append("Fetch and compare branch history, then use a normal push or reviewed force-with-lease.")
    if not alternatives and reasons:
        alternatives.append("Run a read-only inspection first and request approval before changing state.")
    return alternatives


def plan_safe_command(text: str, route_hint: Optional[str] = None,
                      user_role: str = "operator") -> SafetyDecision:
    reasons = explain_danger(text)
    action_type = classify_action(text)
    dangerous = bool(reasons)
    permission = "dangerous" if dangerous else action_type
    permissions = ROLE_PERMISSIONS.get(user_role, ROLE_PERMISSIONS["viewer"])
    allowed = permission in permissions
    requires_confirmation = dangerous or action_type == "write"
    if dangerous:
        level = "dangerous"
    elif action_type == "write":
        level = "needs_confirmation"
        reasons = ["This request changes local or external state and needs explicit approval."]
    else:
        level = "safe"
    if not allowed:
        reasons.append(f"Role '{user_role}' does not have '{permission}' permission.")
    return SafetyDecision(
        action_type=action_type,
        safety_level=level,
        requires_confirmation=requires_confirmation,
        allowed=allowed,
        reasons=reasons,
        alternatives=suggest_safe_alternatives(text, reasons),
        required_permission=permission,
        user_role=user_role,
    )


def gate_route(text: str, route_hint: Optional[str] = None, user_role: str = "operator") -> SafetyDecision:
    return plan_safe_command(text, route_hint, user_role)


def log_nlp_audit(text: str, intent: str, route_hint: Optional[str],
                  decision: SafetyDecision, metadata: Optional[Dict] = None) -> None:
    AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "text": text,
        "intent": intent,
        "route_hint": route_hint,
        "decision": asdict(decision),
        "metadata": metadata or {},
    }
    with AUDIT_FILE.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True) + "\n")


def recent_audit_entries(limit: int = 10) -> List[Dict]:
    if not AUDIT_FILE.exists():
        return []
    lines = AUDIT_FILE.read_text(encoding="utf-8", errors="ignore").splitlines()[-limit:]
    entries = []
    for line in lines:
        try:
            entries.append(json.loads(line))
        except ValueError:
            continue
    return entries
