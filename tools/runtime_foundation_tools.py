from __future__ import annotations

import json
from pathlib import Path


RUNTIME_FOUNDATION_DIR = Path("storage/runtime_foundation")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(RUNTIME_FOUNDATION_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def recursive_autonomous_systems_kernel() -> str:
    return _render("RECURSIVE AUTONOMOUS SYSTEMS KERNEL - PHASE 1501", "autonomous-systems-kernel overview", "autonomous_systems_kernel.json", "kernel_loops", "stable", "runaway", "Kernel loops tracked", "Stable loops", "Runaway loops", "Guardrail: autonomous systems kernels should preserve bounded recursion, emergency shutdown, and operator visibility into state.")


def universal_agent_runtime_foundation() -> str:
    return _render("UNIVERSAL AGENT RUNTIME FOUNDATION - PHASE 1502", "agent-runtime-foundation overview", "agent_runtime_foundation.json", "runtime_layers", "ready", "coupled", "Runtime layers tracked", "Ready layers", "Coupled layers", "Guardrail: runtime foundations should preserve isolation, explicit contracts, and graceful degradation between layers.")


def infinite_context_memory_compression_engine() -> str:
    return _render("INFINITE-CONTEXT MEMORY COMPRESSION ENGINE - PHASE 1503", "memory-compression overview", "memory_compression_engine.json", "compression_policies", "loss-aware", "distorted", "Compression policies tracked", "Loss-aware policies", "Distorted policies", "Guardrail: memory compression should preserve provenance, recoverability, and visible uncertainty after summarization.")


def distributed_cognition_operating_layer() -> str:
    return _render("DISTRIBUTED COGNITION OPERATING LAYER - PHASE 1504", "distributed-cognition overview", "distributed_cognition_layer.json", "cognition_nodes", "coordinated", "desynced", "Cognition nodes tracked", "Coordinated nodes", "Desynced nodes", "Guardrail: distributed cognition should preserve synchronization boundaries, auditable state transfer, and bounded blast radius.")


def autonomous_self_maintenance_core() -> str:
    return _render("AUTONOMOUS SELF-MAINTENANCE CORE - PHASE 1505", "self-maintenance overview", "self_maintenance_core.json", "maintenance_loops", "healthy", "drifting", "Maintenance loops tracked", "Healthy loops", "Drifting loops", "Guardrail: self-maintenance should preserve explicit approvals for invasive action, rollback plans, and audit visibility.")


def cross_environment_execution_framework() -> str:
    return _render("CROSS-ENVIRONMENT EXECUTION FRAMEWORK - PHASE 1506", "cross-environment-execution overview", "cross_environment_execution.json", "execution_paths", "portable", "environment-bound", "Execution paths tracked", "Portable paths", "Environment-bound paths", "Guardrail: cross-environment execution should preserve compatibility checks, secret isolation, and environment-specific safety rails.")


def local_cloud_hybrid_intelligence_bridge() -> str:
    return _render("LOCAL-CLOUD HYBRID INTELLIGENCE BRIDGE - PHASE 1507", "local-cloud-hybrid overview", "local_cloud_hybrid_bridge.json", "bridge_links", "bridged", "leaky", "Bridge links tracked", "Bridged links", "Leaky links", "Guardrail: local-cloud bridges should preserve data minimization, explicit routing, and user-controlled fallback to local-only mode.")


def multi_device_personal_ai_fabric() -> str:
    return _render("MULTI-DEVICE PERSONAL AI FABRIC - PHASE 1508", "multi-device-ai-fabric overview", "personal_ai_fabric.json", "device_meshes", "synchronized", "fragmented", "Device meshes tracked", "Synchronized meshes", "Fragmented meshes", "Guardrail: multi-device fabrics should preserve encryption, conflict visibility, and device-specific trust boundaries.")


def ai_identity_continuity_protocol() -> str:
    return _render("AI IDENTITY CONTINUITY PROTOCOL - PHASE 1509", "identity-continuity overview", "identity_continuity_protocol.json", "identity_paths", "continuous", "spoofable", "Identity paths tracked", "Continuous paths", "Spoofable paths", "Guardrail: identity continuity should preserve user consent, provenance, and strong anti-impersonation controls.")


def sovereign_user_data_control_system() -> str:
    return _render("SOVEREIGN USER DATA CONTROL SYSTEM - PHASE 1510", "user-data-control overview", "user_data_control_system.json", "control_policies", "user-sovereign", "opaque", "Control policies tracked", "User-sovereign policies", "Opaque policies", "Guardrail: user data control should preserve exportability, deletion rights, and transparent data routing before retention.")
