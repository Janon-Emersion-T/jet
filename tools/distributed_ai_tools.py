from __future__ import annotations

import json
import os
from pathlib import Path


DISTRIBUTED_DIR = Path("storage/distributed_ai")


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


def autonomous_infrastructure_scaling() -> str:
    nodes = _list_entries(DISTRIBUTED_DIR / "scaling.json", "nodes")
    autoscale = [item for item in nodes if isinstance(item, dict) and bool(item.get("autoscale", False))]
    return "\n".join(
        [
            "AUTONOMOUS INFRASTRUCTURE SCALING - PHASE 486",
            "Mode: scaling-plan overview.",
            f"Nodes tracked: {len(nodes)}",
            f"Autoscale-capable nodes: {len(autoscale)}",
            "Safety: recommendation only; no infrastructure scale event was triggered.",
        ]
    )


def federated_local_ai_network() -> str:
    peers = _list_entries(DISTRIBUTED_DIR / "federation.json", "peers")
    trusted = [item for item in peers if isinstance(item, dict) and bool(item.get("trusted", False))]
    return "\n".join(
        [
            "FEDERATED LOCAL AI NETWORK - PHASE 487",
            "Mode: federation topology review.",
            f"Peers tracked: {len(peers)}",
            f"Trusted peers: {len(trusted)}",
            "Pattern: local-first inference with explicit trust boundaries and model/data locality preserved.",
        ]
    )


def distributed_memory_system() -> str:
    stores = _list_entries(DISTRIBUTED_DIR / "memory_shards.json", "stores")
    replicas = sum(int(item.get("replicas", 0) or 0) for item in stores if isinstance(item, dict))
    return "\n".join(
        [
            "DISTRIBUTED MEMORY SYSTEM - PHASE 488",
            "Mode: memory-cluster overview.",
            f"Stores tracked: {len(stores)}",
            f"Replica count: {replicas}",
            "Design note: reconcile freshness, conflict handling, access policy, and recovery before scaling memory writes horizontally.",
        ]
    )


def distributed_agent_clusters() -> str:
    clusters = _list_entries(DISTRIBUTED_DIR / "agent_clusters.json", "clusters")
    agents = sum(int(item.get("agents", 0) or 0) for item in clusters if isinstance(item, dict))
    return "\n".join(
        [
            "DISTRIBUTED AGENT CLUSTERS - PHASE 489",
            "Mode: agent-cluster overview.",
            f"Clusters tracked: {len(clusters)}",
            f"Total agents described: {agents}",
            "Goal: place planning, execution, monitoring, and recovery roles on explicit cluster boundaries.",
        ]
    )


def edge_ai_deployment_engine() -> str:
    devices = _list_entries(DISTRIBUTED_DIR / "edge_devices.json", "devices")
    offline_ready = [item for item in devices if isinstance(item, dict) and bool(item.get("offline_ready", False))]
    return "\n".join(
        [
            "EDGE AI DEPLOYMENT ENGINE - PHASE 490",
            "Mode: edge deployment readiness review.",
            f"Devices tracked: {len(devices)}",
            f"Offline-ready devices: {len(offline_ready)}",
            "Constraint set: model size, thermals, storage, latency, update policy, and fallback behavior.",
        ]
    )


def offline_enterprise_ai_appliance() -> str:
    appliance = _safe_json(DISTRIBUTED_DIR / "enterprise_appliance.json", {})
    racks = int(appliance.get("racks", 0) or 0) if isinstance(appliance, dict) else 0
    models = int(appliance.get("models", 0) or 0) if isinstance(appliance, dict) else 0
    return "\n".join(
        [
            "OFFLINE ENTERPRISE AI APPLIANCE - PHASE 491",
            "Mode: appliance architecture summary.",
            f"Rack units planned: {racks}",
            f"Model families planned: {models}",
            "Goal: deliver a sealed local AI stack with offline inference, managed updates, and explicit support boundaries.",
        ]
    )


def sovereign_ai_workstation() -> str:
    profile = _safe_json(DISTRIBUTED_DIR / "workstation.json", {})
    gpus = int(profile.get("gpus", 0) or 0) if isinstance(profile, dict) else 0
    ram = int(profile.get("ram_gb", 0) or 0) if isinstance(profile, dict) else 0
    secure_boot = bool(profile.get("secure_boot", False)) if isinstance(profile, dict) else False
    return "\n".join(
        [
            "SOVEREIGN AI WORKSTATION - PHASE 492",
            "Mode: workstation sovereignty profile.",
            f"GPUs: {gpus}",
            f"RAM (GB): {ram}",
            f"Secure boot enabled: {'YES' if secure_boot else 'NO'}",
            "Principle: local ownership of compute, data, models, updates, and backup/restore capability.",
        ]
    )
