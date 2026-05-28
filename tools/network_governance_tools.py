from __future__ import annotations

import json
from pathlib import Path


NETWORK_DIR = Path("storage/network_governance")


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


def ai_accountability_tracker() -> str:
    records = _list_entries(NETWORK_DIR / "accountability.json", "records")
    owned = [item for item in records if isinstance(item, dict) and item.get("owner")]
    reviewed = [item for item in records if isinstance(item, dict) and bool(item.get("reviewed", False))]
    return "\n".join(
        [
            "AI ACCOUNTABILITY TRACKER - PHASE 516",
            "Mode: accountability record overview.",
            f"Records tracked: {len(records)}",
            f"Records with owners: {len(owned)}",
            f"Reviewed records: {len(reviewed)}",
            "Rule: every autonomous action path should map back to an owner, a policy, and a review state.",
        ]
    )


def autonomous_infrastructure_diagnostics() -> str:
    checks = _list_entries(NETWORK_DIR / "diagnostics.json", "checks")
    failing = [item for item in checks if isinstance(item, dict) and item.get("status") == "failing"]
    degraded = [item for item in checks if isinstance(item, dict) and item.get("status") == "degraded"]
    return "\n".join(
        [
            "AUTONOMOUS INFRASTRUCTURE DIAGNOSTICS - PHASE 517",
            "Mode: infrastructure diagnostics overview.",
            f"Checks tracked: {len(checks)}",
            f"Degraded checks: {len(degraded)}",
            f"Failing checks: {len(failing)}",
            "Pattern: observe, classify, isolate, and escalate before invoking any automatic repair routine.",
        ]
    )


def live_topology_visualization() -> str:
    nodes = _list_entries(NETWORK_DIR / "topology.json", "nodes")
    edges = _list_entries(NETWORK_DIR / "topology.json", "edges")
    zones = sorted(
        {
            str(item.get("zone", "default"))
            for item in nodes
            if isinstance(item, dict) and item.get("zone")
        }
    )
    return "\n".join(
        [
            "LIVE TOPOLOGY VISUALIZATION - PHASE 518",
            "Mode: topology model overview.",
            f"Nodes tracked: {len(nodes)}",
            f"Edges tracked: {len(edges)}",
            f"Zones: {', '.join(zones) if zones else 'none'}",
            "Goal: keep runtime relationships visible enough that failures and trust boundaries are obvious at a glance.",
        ]
    )


def ai_network_optimization() -> str:
    links = _list_entries(NETWORK_DIR / "optimization.json", "links")
    congested = [item for item in links if isinstance(item, dict) and float(item.get("utilization", 0) or 0) >= 80]
    tuned = [item for item in links if isinstance(item, dict) and bool(item.get("optimized", False))]
    return "\n".join(
        [
            "AI NETWORK OPTIMIZATION - PHASE 519",
            "Mode: network optimization overview.",
            f"Links tracked: {len(links)}",
            f"Congested links: {len(congested)}",
            f"Already tuned links: {len(tuned)}",
            "Constraint: optimize for latency, resilience, and cost without hiding risky tradeoffs from operators.",
        ]
    )


def autonomous_vpn_management() -> str:
    tunnels = _list_entries(NETWORK_DIR / "vpn.json", "tunnels")
    active = [item for item in tunnels if isinstance(item, dict) and bool(item.get("active", False))]
    expiring = [item for item in tunnels if isinstance(item, dict) and int(item.get("days_to_expiry", 999) or 999) <= 14]
    return "\n".join(
        [
            "AUTONOMOUS VPN MANAGEMENT - PHASE 520",
            "Mode: VPN fleet overview.",
            f"Tunnels tracked: {len(tunnels)}",
            f"Active tunnels: {len(active)}",
            f"Tunnels nearing expiry: {len(expiring)}",
            "Safety: certificate rotation, route updates, and policy changes should stay approval-aware even when monitoring is automatic.",
        ]
    )
