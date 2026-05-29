from __future__ import annotations

import json
from pathlib import Path


OPS_CENTER_DIR = Path("storage/ops_center")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _list_entries(path: Path, key: str):
    payload = _safe_json(path, {key: []})
    if isinstance(payload, dict) and isinstance(payload.get(key), list):
        return payload[key]
    if isinstance(payload, list):
        return payload
    return []


def department_specific_ai_agents() -> str:
    departments = _list_entries(OPS_CENTER_DIR / "departments.json", "departments")
    enabled = [item for item in departments if isinstance(item, dict) and bool(item.get("agent_enabled", False))]
    labels = [str(item.get("name", "unknown")) for item in departments[:5] if isinstance(item, dict)]
    return "\n".join(
        [
            "DEPARTMENT-SPECIFIC AI AGENTS - PHASE 507",
            "Mode: departmental agent roster overview.",
            f"Departments tracked: {len(departments)}",
            f"Departments with enabled agents: {len(enabled)}",
            f"Preview: {', '.join(labels) if labels else 'none'}",
            "Guideline: each department agent should inherit shared safety rules while preserving domain-specific context and escalation paths.",
        ]
    )


def ai_operations_center_dashboard() -> str:
    widgets = _list_entries(OPS_CENTER_DIR / "dashboard.json", "widgets")
    alerts = _list_entries(OPS_CENTER_DIR / "dashboard.json", "alerts")
    return "\n".join(
        [
            "AI OPERATIONS CENTER DASHBOARD - PHASE 508",
            "Mode: operations-center summary.",
            f"Widgets tracked: {len(widgets)}",
            f"Active alerts: {len(alerts)}",
            "Purpose: centralize agent health, approvals, failures, throughput, and risk signals for one operator view.",
        ]
    )


def global_event_stream_processor() -> str:
    streams = _list_entries(OPS_CENTER_DIR / "event_streams.json", "streams")
    consumers = sum(int(item.get("consumers", 0) or 0) for item in streams if isinstance(item, dict))
    lagging = [item for item in streams if isinstance(item, dict) and int(item.get("lag", 0) or 0) > 0]
    return "\n".join(
        [
            "GLOBAL EVENT STREAM PROCESSOR - PHASE 509",
            "Mode: event-stream topology overview.",
            f"Streams tracked: {len(streams)}",
            f"Consumers declared: {consumers}",
            f"Lagging streams: {len(lagging)}",
            "Design note: preserve ordering, replayability, and tenant-aware filtering before event traffic becomes a control plane.",
        ]
    )


def ai_task_dependency_graph() -> str:
    tasks = _list_entries(OPS_CENTER_DIR / "dependency_graph.json", "tasks")
    edges = _list_entries(OPS_CENTER_DIR / "dependency_graph.json", "edges")
    blocked = [item for item in tasks if isinstance(item, dict) and bool(item.get("blocked", False))]
    return "\n".join(
        [
            "AI TASK DEPENDENCY GRAPH - PHASE 510",
            "Mode: dependency-graph overview.",
            f"Tasks represented: {len(tasks)}",
            f"Dependency edges: {len(edges)}",
            f"Blocked tasks: {len(blocked)}",
            "Use case: expose sequencing, bottlenecks, retries, and ownership before autonomous scheduling grows larger.",
        ]
    )
