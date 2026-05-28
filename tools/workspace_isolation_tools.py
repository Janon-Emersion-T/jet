from __future__ import annotations

import json
from pathlib import Path


ISOLATION_DIR = Path("storage/workspace_isolation")


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


def ai_workspace_isolation() -> str:
    workspaces = _list_entries(ISOLATION_DIR / "workspaces.json", "workspaces")
    isolated = [item for item in workspaces if isinstance(item, dict) and bool(item.get("isolated", False))]
    shared = [item for item in workspaces if isinstance(item, dict) and bool(item.get("shared_tools", False))]
    policy_sets = sorted(
        {
            str(item.get("policy", "default"))
            for item in workspaces
            if isinstance(item, dict) and item.get("policy")
        }
    )
    return "\n".join(
        [
            "AI WORKSPACE ISOLATION - PHASE 506",
            "Mode: workspace-boundary overview.",
            f"Workspaces tracked: {len(workspaces)}",
            f"Isolated workspaces: {len(isolated)}",
            f"Shared-tool workspaces: {len(shared)}",
            f"Policy sets: {', '.join(policy_sets) if policy_sets else 'none'}",
            "Isolation rule: context, memory, approvals, files, and tool scopes should default to workspace-local boundaries.",
        ]
    )
