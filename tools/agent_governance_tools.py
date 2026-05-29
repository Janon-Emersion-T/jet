from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from tools.agent_orchestration_tools import AGENTS
from tools.infrastructure_monitoring_tools import (
    backup_verification_engine,
    cpu_ram_monitoring_assistant,
    disk_health_checker,
    uptime_monitoring_assistant,
)
from tools.operator_tools import REMOTE_APPROVAL_DIR


@dataclass
class DelegationDecision:
    role: str
    confidence: float
    reason: str


AGENT_TASK_MAP: Dict[str, str] = {
    "finance": "finance",
    "schedule": "scheduling",
    "calendar": "scheduling",
    "browser": "browser",
    "deploy": "deployment",
    "monitor": "monitoring",
    "seo": "seo",
    "marketing": "marketing",
    "code": "coding",
    "research": "research",
    "security": "security",
}


def finance_agent(task: str = "review budget impact") -> str:
    return (
        "FINANCE AGENT - PHASE 401\n"
        f"Task: {task}\n"
        "Focus: cost analysis, pricing tradeoffs, ROI framing, and financial risk.\n"
        "Output: financial recommendation brief.\n"
        "Safety: advisory only; no ledger, payment, or invoice data was changed."
    )


def scheduling_agent(task: str = "coordinate deadlines and meetings") -> str:
    return (
        "SCHEDULING AGENT - PHASE 402\n"
        f"Task: {task}\n"
        "Focus: timeline sequencing, calendar constraints, and dependency ordering.\n"
        "Output: proposed schedule.\n"
        "Safety: no calendar or meeting invitation was created."
    )


def autonomous_browser_agent(task: str = "inspect a page workflow") -> str:
    return (
        "AUTONOMOUS BROWSER AGENT - PHASE 403\n"
        f"Task: {task}\n"
        "Focus: page reading, approval-based navigation, and safe extraction planning.\n"
        "Output: browser action plan.\n"
        "Safety: no browser action was executed by this agent."
    )


def autonomous_deployment_agent(task: str = "prepare deployment plan") -> str:
    return (
        "AUTONOMOUS DEPLOYMENT AGENT - PHASE 404\n"
        f"Task: {task}\n"
        "Focus: deployment sequencing, backup checks, rollback planning, and approvals.\n"
        "Output: deployment readiness plan.\n"
        "Safety: no deployment command was executed."
    )


def autonomous_monitoring_agent() -> str:
    lines = [
        "AUTONOMOUS MONITORING AGENT - PHASE 405",
        "Mode: read-only operational summary.",
        "",
        cpu_ram_monitoring_assistant(),
        "",
        disk_health_checker(),
        "",
        uptime_monitoring_assistant(),
        "",
        backup_verification_engine(),
    ]
    return "\n".join(lines)


def ai_swarm_coordination(task: str = "ship a safe feature") -> str:
    route = ["planner", "coding", "security", "critic", "research"]
    lines = [
        "AI SWARM COORDINATION - PHASE 406",
        f"Task: {task}",
        "Swarm route:",
    ]
    lines += [f"{index}. {AGENTS[name].name}" for index, name in enumerate(route, 1)]
    lines.append("Safety: coordination plan only; no agent executed tools.")
    return "\n".join(lines)


def agent_task_marketplace() -> str:
    lines = [
        "AGENT TASK MARKETPLACE - PHASE 407",
        "Available specialist agents:",
    ]
    lines += [f"- {name}: {role.responsibility}" for name, role in AGENTS.items()]
    lines += [
        "- finance: financial recommendation brief",
        "- scheduling: timeline and calendar planning",
        "- browser: page workflow planning",
        "- deployment: deployment readiness planning",
        "- monitoring: operational summary planning",
        "Safety: listing only; no task was assigned.",
    ]
    return "\n".join(lines)


def role_based_ai_delegation(task: str = "review infrastructure risks") -> str:
    lowered = task.lower()
    role = "research"
    confidence = 0.45
    reason = "Fallback to research for ambiguous requests."
    for keyword, mapped in AGENT_TASK_MAP.items():
        if keyword in lowered:
            role = mapped
            confidence = 0.85
            reason = f"Matched keyword `{keyword}`."
            break
    if role in AGENTS:
        label = AGENTS[role].name
    else:
        label = role.title()
    return (
        "ROLE-BASED AI DELEGATION - PHASE 408\n"
        f"Task: {task}\n"
        f"Delegated role: {label}\n"
        f"Confidence: {confidence:.2f}\n"
        f"Reason: {reason}\n"
        "Safety: delegation recommendation only; no task was dispatched."
    )


def human_approval_gateway() -> str:
    REMOTE_APPROVAL_DIR.mkdir(parents=True, exist_ok=True)
    approvals = sorted(REMOTE_APPROVAL_DIR.glob("*.json"))
    return (
        "HUMAN APPROVAL GATEWAY - PHASE 409\n"
        f"Pending approval records directory: {REMOTE_APPROVAL_DIR}\n"
        f"Stored approval files: {len(approvals)}\n"
        "Policy: high-risk actions should remain approval-gated before execution.\n"
        "Safety: no approval state was changed."
    )


def action_logging_framework() -> str:
    event_log = Path("storage/events/events.log")
    line_count = 0
    if event_log.exists():
        try:
            line_count = len(event_log.read_text(encoding="utf-8", errors="replace").splitlines())
        except OSError:
            line_count = 0
    return (
        "ACTION LOGGING FRAMEWORK - PHASE 410\n"
        f"Event log path: {event_log}\n"
        f"Recorded entries: {line_count}\n"
        "Recommendation: pair action logs with approval IDs and decision traces.\n"
        "Safety: log inspection only; no records were altered."
    )

