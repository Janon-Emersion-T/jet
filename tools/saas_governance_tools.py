from __future__ import annotations

import json
from pathlib import Path


SAAS_GOVERNANCE_DIR = Path("storage/saas_governance")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(SAAS_GOVERNANCE_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def database_migration_planner() -> str:
    return _render("DATABASE MIGRATION PLANNER - PHASE 1621", "database-migration overview", "database_migration_planner.json", "migration_paths", "planned", "risky", "Migration paths tracked", "Planned paths", "Risky paths", "Guardrail: migration planning should preserve rollback steps, data integrity concerns, and ordering dependencies.")


def data_seeding_strategist() -> str:
    return _render("DATA SEEDING STRATEGIST - PHASE 1622", "data-seeding overview", "data_seeding_strategist.json", "seeding_plans", "coherent", "unsafe", "Seeding plans tracked", "Coherent plans", "Unsafe plans", "Guardrail: seeding guidance should preserve environment separation and avoid overwriting sensitive or production data assumptions.")


def tenant_isolation_auditor() -> str:
    return _render("TENANT ISOLATION AUDITOR - PHASE 1623", "tenant-isolation overview", "tenant_isolation_auditor.json", "tenant_boundaries", "isolated", "leaky", "Tenant boundaries tracked", "Isolated boundaries", "Leaky boundaries", "Guardrail: tenant isolation analysis should preserve evidence, least privilege, and explicit blast-radius discussion for shared resources.")


def saas_module_marketplace_engine() -> str:
    return _render("SAAS MODULE MARKETPLACE ENGINE - PHASE 1624", "saas-marketplace overview", "saas_module_marketplace.json", "module_listings", "coherent", "scattered", "Module listings tracked", "Coherent listings", "Scattered listings", "Guardrail: marketplace planning should preserve module compatibility, permission boundaries, and billing clarity.")


def subscription_enforcement_auditor() -> str:
    return _render("SUBSCRIPTION ENFORCEMENT AUDITOR - PHASE 1625", "subscription-enforcement overview", "subscription_enforcement_auditor.json", "enforcement_checks", "consistent", "bypassed", "Enforcement checks tracked", "Consistent checks", "Bypassed checks", "Guardrail: subscription auditing should preserve entitlement traceability and avoid cutting access without contract-status evidence.")


def trial_period_automation() -> str:
    return _render("TRIAL-PERIOD AUTOMATION - PHASE 1626", "trial-period overview", "trial_period_automation.json", "trial_flows", "fair", "confusing", "Trial flows tracked", "Fair flows", "Confusing flows", "Guardrail: trial automation should preserve user clarity, explicit consent for billing transitions, and local legal/compliance review.")


def user_role_drift_detector() -> str:
    return _render("USER-ROLE DRIFT DETECTOR - PHASE 1627", "role-drift overview", "user_role_drift_detector.json", "role_assignments", "expected", "drifting", "Role assignments tracked", "Expected assignments", "Drifting assignments", "Guardrail: role-drift detection should preserve approval history, least privilege, and avoid treating legitimate exceptions as incidents without evidence.")


def permission_matrix_visualizer() -> str:
    return _render("PERMISSION MATRIX VISUALIZER - PHASE 1628", "permission-matrix overview", "permission_matrix_visualizer.json", "permission_matrices", "clear", "opaque", "Permission matrices tracked", "Clear matrices", "Opaque matrices", "Guardrail: permission visualization should preserve exact policy provenance and distinguish inferred access from verified rules.")


def audit_log_intelligence() -> str:
    return _render("AUDIT-LOG INTELLIGENCE - PHASE 1629", "audit-log-intelligence overview", "audit_log_intelligence.json", "audit_signals", "explained", "suspicious", "Audit signals tracked", "Explained signals", "Suspicious signals", "Guardrail: audit analysis should preserve chronology, actor provenance, and avoid claiming intent from log patterns alone.")


def immutable_ledger_checker() -> str:
    return _render("IMMUTABLE LEDGER CHECKER - PHASE 1630", "immutable-ledger overview", "immutable_ledger_checker.json", "ledger_entries", "consistent", "tampered", "Ledger entries tracked", "Consistent entries", "Tampered entries", "Guardrail: ledger checking should preserve evidence chains and treat integrity anomalies as flags for review, not final proof.")
