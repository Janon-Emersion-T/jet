from __future__ import annotations

import json
from pathlib import Path


COGNITION_DIR = Path("storage/collaborative_cognition")


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


def distributed_autonomous_agent_mesh() -> str:
    nodes = _list_entries(COGNITION_DIR / "agent_mesh.json", "nodes")
    links = _list_entries(COGNITION_DIR / "agent_mesh.json", "links")
    healthy = [item for item in nodes if isinstance(item, dict) and item.get("status", "healthy") == "healthy"]
    return "\n".join(
        [
            "DISTRIBUTED AUTONOMOUS AGENT MESH - PHASE 501",
            "Mode: mesh-topology overview.",
            f"Nodes tracked: {len(nodes)}",
            f"Healthy nodes: {len(healthy)}",
            f"Mesh links: {len(links)}",
            "Design note: keep routing, trust, quorum, and failure containment explicit before widening autonomous coordination.",
        ]
    )


def cross_device_synchronized_cognition() -> str:
    devices = _list_entries(COGNITION_DIR / "device_sync.json", "devices")
    sync_items = _list_entries(COGNITION_DIR / "device_sync.json", "pending")
    converged = [item for item in devices if isinstance(item, dict) and bool(item.get("in_sync", False))]
    return "\n".join(
        [
            "CROSS-DEVICE SYNCHRONIZED COGNITION - PHASE 502",
            "Mode: cross-device cognition sync overview.",
            f"Devices tracked: {len(devices)}",
            f"Devices in sync: {len(converged)}",
            f"Pending sync items: {len(sync_items)}",
            "Constraint: preserve causality, merge safety, and owner visibility before auto-propagating memory or plans.",
        ]
    )


def persistent_ai_identity_layer() -> str:
    identities = _list_entries(COGNITION_DIR / "identity.json", "identities")
    personas = sorted(
        {
            str(item.get("persona", "default"))
            for item in identities
            if isinstance(item, dict) and item.get("persona")
        }
    )
    return "\n".join(
        [
            "PERSISTENT AI IDENTITY LAYER - PHASE 503",
            "Mode: identity-profile overview.",
            f"Identity profiles: {len(identities)}",
            f"Personas represented: {', '.join(personas) if personas else 'none'}",
            "Identity scope: memory boundaries, style continuity, permissions, and user-visible provenance.",
        ]
    )


def multi_user_access_framework() -> str:
    users = _list_entries(COGNITION_DIR / "users.json", "users")
    roles = _list_entries(COGNITION_DIR / "users.json", "roles")
    active = [item for item in users if isinstance(item, dict) and bool(item.get("active", True))]
    return "\n".join(
        [
            "MULTI-USER ACCESS FRAMEWORK - PHASE 504",
            "Mode: multi-user access overview.",
            f"Users tracked: {len(users)}",
            f"Active users: {len(active)}",
            f"Role definitions: {len(roles)}",
            "Security rule: identity, session, role, and approval policy should travel together across every tool boundary.",
        ]
    )


def tenant_aware_ai_memory() -> str:
    tenants = _list_entries(COGNITION_DIR / "tenant_memory.json", "tenants")
    partitions = sum(int(item.get("memory_partitions", 0) or 0) for item in tenants if isinstance(item, dict))
    isolated = [item for item in tenants if isinstance(item, dict) and bool(item.get("isolated", False))]
    return "\n".join(
        [
            "TENANT-AWARE AI MEMORY - PHASE 505",
            "Mode: tenant memory isolation overview.",
            f"Tenants tracked: {len(tenants)}",
            f"Isolated tenants: {len(isolated)}",
            f"Memory partitions declared: {partitions}",
            "Isolation rule: retrieval, indexing, caching, and analytics should all respect tenant boundaries by default.",
        ]
    )
