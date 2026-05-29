from __future__ import annotations

import json
from pathlib import Path


RESILIENCE_PRIVACY_DIR = Path("storage/resilience_privacy")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(RESILIENCE_PRIVACY_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def login_anomaly_detector() -> str:
    return _render("LOGIN ANOMALY DETECTOR - PHASE 1691", "login-anomaly overview", "login_anomaly_detector.json", "login_events", "routine", "anomalous", "Login events tracked", "Routine events", "Anomalous events", "Guardrail: anomaly detection should preserve explainability and avoid turning sparse signals into account-compromise claims without corroboration.")


def fail2ban_intelligence() -> str:
    return _render("FAIL2BAN INTELLIGENCE - PHASE 1692", "fail2ban-intelligence overview", "fail2ban_intelligence.json", "ban_profiles", "effective", "weak", "Ban profiles tracked", "Effective profiles", "Weak profiles", "Guardrail: Fail2ban analysis should preserve config provenance and avoid recommending bans that could lock out legitimate operators without review.")


def malware_scan_orchestrator() -> str:
    return _render("MALWARE SCAN ORCHESTRATOR - PHASE 1693", "malware-scan overview", "malware_scan_orchestrator.json", "scan_runs", "clean", "flagged", "Scan runs tracked", "Clean runs", "Flagged runs", "Guardrail: malware orchestration should preserve non-destructive scanning and clearly label signatures or heuristics as unconfirmed until reviewed.")


def backup_integrity_tester() -> str:
    return _render("BACKUP INTEGRITY TESTER - PHASE 1694", "backup-integrity overview", "backup_integrity_tester.json", "backup_checks", "restorable", "broken", "Backup checks tracked", "Restorable checks", "Broken checks", "Guardrail: backup integrity testing should preserve environment isolation and distinguish metadata success from tested restore viability.")


def disaster_recovery_simulator() -> str:
    return _render("DISASTER RECOVERY SIMULATOR - PHASE 1695", "disaster-recovery overview", "disaster_recovery_simulator.json", "recovery_paths", "rehearsed", "fragile", "Recovery paths tracked", "Rehearsed paths", "Fragile paths", "Guardrail: DR simulation should preserve tabletop-vs-live distinctions and avoid implying recovery certainty without actual drills.")


def ransomware_resilience_planner() -> str:
    return _render("RANSOMWARE RESILIENCE PLANNER - PHASE 1696", "ransomware-resilience overview", "ransomware_resilience_planner.json", "resilience_layers", "layered", "thin", "Resilience layers tracked", "Layered defenses", "Thin defenses", "Guardrail: ransomware planning should preserve backup immutability nuance and avoid claiming immunity from any single control.")


def privacy_impact_assessor() -> str:
    return _render("PRIVACY-IMPACT ASSESSOR - PHASE 1697", "privacy-impact overview", "privacy_impact_assessor.json", "processing_activities", "assessed", "sensitive", "Processing activities tracked", "Assessed activities", "Sensitive activities", "Guardrail: privacy impact analysis should preserve data-category context and avoid legal conclusions without jurisdiction-specific review.")


def data_retention_governor() -> str:
    return _render("DATA RETENTION GOVERNOR - PHASE 1698", "data-retention overview", "data_retention_governor.json", "retention_policies", "defined", "overretained", "Retention policies tracked", "Defined policies", "Overretained policies", "Guardrail: retention guidance should preserve legal-hold exceptions, backup nuance, and explicit confirmation before deletion workflows.")


def compliance_evidence_collector() -> str:
    return _render("COMPLIANCE EVIDENCE COLLECTOR - PHASE 1699", "compliance-evidence overview", "compliance_evidence_collector.json", "evidence_items", "collected", "missing", "Evidence items tracked", "Collected items", "Missing items", "Guardrail: evidence collection should preserve chain-of-custody context and clearly distinguish gathered artifacts from validated compliance.")


def security_command_authority_layer() -> str:
    return _render("SECURITY COMMAND AUTHORITY LAYER - PHASE 1700", "security-authority overview", "security_command_authority.json", "authority_checks", "authorized", "overreaching", "Authority checks tracked", "Authorized checks", "Overreaching checks", "Guardrail: authority-layer analysis should preserve least privilege and clear separation between advisory detection and enforcement power.")
