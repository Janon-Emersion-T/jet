from __future__ import annotations

import json
from pathlib import Path


TRUST_OBSERVABILITY_DIR = Path("storage/trust_observability")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(TRUST_OBSERVABILITY_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def encrypted_agent_memory_vault() -> str:
    return _render("ENCRYPTED AGENT MEMORY VAULT - PHASE 1511", "agent-memory-vault overview", "agent_memory_vault.json", "vault_segments", "encrypted", "exposed", "Vault segments tracked", "Encrypted segments", "Exposed segments", "Guardrail: encrypted memory vaults should preserve key separation, revocation pathways, and least-privilege read access.")


def personal_knowledge_constitution() -> str:
    return _render("PERSONAL KNOWLEDGE CONSTITUTION - PHASE 1512", "knowledge-constitution overview", "knowledge_constitution.json", "knowledge_charters", "codified", "inconsistent", "Knowledge charters tracked", "Codified charters", "Inconsistent charters", "Guardrail: knowledge constitutions should preserve user ownership, amendment visibility, and conflict-resolution rules.")


def autonomous_trust_boundary_manager() -> str:
    return _render("AUTONOMOUS TRUST BOUNDARY MANAGER - PHASE 1513", "trust-boundary overview", "trust_boundary_manager.json", "trust_boundaries", "isolated", "porous", "Trust boundaries tracked", "Isolated boundaries", "Porous boundaries", "Guardrail: trust boundaries should preserve compartmentalization, explicit escalation paths, and auditable crossing events.")


def dynamic_permission_negotiation_engine() -> str:
    return _render("DYNAMIC PERMISSION NEGOTIATION ENGINE - PHASE 1514", "permission-negotiation overview", "permission_negotiation_engine.json", "permission_requests", "justified", "overbroad", "Permission requests tracked", "Justified requests", "Overbroad requests", "Guardrail: permission negotiation should preserve least privilege, user clarity, and revocation after task completion.")


def runtime_risk_containment_layer() -> str:
    return _render("RUNTIME RISK CONTAINMENT LAYER - PHASE 1515", "risk-containment overview", "risk_containment_layer.json", "containment_rules", "contained", "leaking", "Containment rules tracked", "Contained rules", "Leaking rules", "Guardrail: runtime containment should preserve deterministic failure handling, auditability, and human-visible escalation on breach.")


def agent_action_insurance_framework() -> str:
    return _render("AGENT ACTION INSURANCE FRAMEWORK - PHASE 1516", "action-insurance overview", "action_insurance_framework.json", "insurance_policies", "covered", "uninsured", "Insurance policies tracked", "Covered policies", "Uninsured policies", "Guardrail: action insurance should preserve precondition checks, compensation logic, and accountable attribution of failures.")


def reversible_automation_architecture() -> str:
    return _render("REVERSIBLE AUTOMATION ARCHITECTURE - PHASE 1517", "reversible-automation overview", "reversible_automation_architecture.json", "automation_paths", "reversible", "irreversible", "Automation paths tracked", "Reversible paths", "Irreversible paths", "Guardrail: automation architecture should preserve rollback capability, state snapshots, and user-approved irreversible boundaries.")


def system_wide_rollback_intelligence() -> str:
    return _render("SYSTEM-WIDE ROLLBACK INTELLIGENCE - PHASE 1518", "rollback-intelligence overview", "rollback_intelligence.json", "rollback_strategies", "ready", "partial", "Rollback strategies tracked", "Ready strategies", "Partial strategies", "Guardrail: rollback intelligence should preserve dependency awareness, recovery ordering, and human confirmation for destructive restores.")


def autonomous_audit_trail_explainer() -> str:
    return _render("AUTONOMOUS AUDIT TRAIL EXPLAINER - PHASE 1519", "audit-trail-explainer overview", "audit_trail_explainer.json", "audit_entries", "explained", "opaque", "Audit entries tracked", "Explained entries", "Opaque entries", "Guardrail: audit explanations should preserve provenance, non-repudiation, and faithful representation of underlying events.")


def full_stack_observability_brain() -> str:
    return _render("FULL-STACK OBSERVABILITY BRAIN - PHASE 1520", "full-stack-observability overview", "observability_brain.json", "observability_surfaces", "visible", "blind", "Observability surfaces tracked", "Visible surfaces", "Blind surfaces", "Guardrail: observability should preserve least-privilege telemetry access, redaction of secrets, and clear signal provenance.")
