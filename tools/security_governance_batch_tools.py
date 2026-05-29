from __future__ import annotations

import json
from pathlib import Path


SECURITY_GOVERNANCE_BATCH_DIR = Path("storage/security_governance_batch")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(SECURITY_GOVERNANCE_BATCH_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def ai_security_review_board() -> str:
    return _render("AI SECURITY REVIEW BOARD - PHASE 1681", "security-review overview", "ai_security_review_board.json", "review_items", "reviewed", "escalated", "Review items tracked", "Reviewed items", "Escalated items", "Guardrail: AI security review should preserve human accountability and avoid auto-approving high-risk changes from heuristic scoring alone.")


def dependency_license_auditor() -> str:
    return _render("DEPENDENCY LICENSE AUDITOR - PHASE 1682", "dependency-license overview", "dependency_license_auditor.json", "license_checks", "clear", "conflicting", "License checks tracked", "Clear checks", "Conflicting checks", "Guardrail: license auditing should preserve exact package/version evidence and avoid legal conclusions without counsel review.")


def open_source_risk_scorer() -> str:
    return _render("OPEN-SOURCE RISK SCORER - PHASE 1683", "open-source-risk overview", "open_source_risk_scorer.json", "package_profiles", "low-risk", "high-risk", "Package profiles tracked", "Low-risk packages", "High-risk packages", "Guardrail: open-source risk scoring should preserve explainability and separate maintenance signals from exploit evidence.")


def package_update_strategy_engine() -> str:
    return _render("PACKAGE UPDATE STRATEGY ENGINE - PHASE 1684", "package-update-strategy overview", "package_update_strategy.json", "update_paths", "safe", "disruptive", "Update paths tracked", "Safe paths", "Disruptive paths", "Guardrail: update strategy should preserve compatibility context, rollback planning, and explicit distinction between patch and breaking upgrades.")


def cve_impact_mapper() -> str:
    return _render("CVE IMPACT MAPPER - PHASE 1685", "cve-impact overview", "cve_impact_mapper.json", "cve_matches", "contextualized", "exposed", "CVE matches tracked", "Contextualized matches", "Exposed matches", "Guardrail: CVE mapping should preserve affected-version evidence and avoid implying exploitability without environment-specific confirmation.")


def secret_rotation_planner() -> str:
    return _render("SECRET ROTATION PLANNER - PHASE 1686", "secret-rotation overview", "secret_rotation_planner.json", "rotation_paths", "planned", "stale", "Rotation paths tracked", "Planned paths", "Stale paths", "Guardrail: secret rotation planning should preserve service dependencies, staged cutovers, and prevent disclosure of secret values in reports.")


def credential_hygiene_assistant() -> str:
    return _render("CREDENTIAL HYGIENE ASSISTANT - PHASE 1687", "credential-hygiene overview", "credential_hygiene_assistant.json", "credential_profiles", "healthy", "risky", "Credential profiles tracked", "Healthy profiles", "Risky profiles", "Guardrail: credential hygiene analysis should preserve privacy and never display or infer actual credentials in outputs.")


def ssh_key_inventory_manager() -> str:
    return _render("SSH-KEY INVENTORY MANAGER - PHASE 1688", "ssh-key-inventory overview", "ssh_key_inventory_manager.json", "ssh_keys", "tracked", "unknown", "SSH keys tracked", "Tracked keys", "Unknown keys", "Guardrail: SSH-key inventory should preserve public/private separation and avoid presenting orphan detection as revocation authority.")


def firewall_policy_analyzer() -> str:
    return _render("FIREWALL POLICY ANALYZER - PHASE 1689", "firewall-policy overview", "firewall_policy_analyzer.json", "firewall_rules", "restricted", "permissive", "Firewall rules tracked", "Restricted rules", "Permissive rules", "Guardrail: firewall analysis should preserve exact port/protocol context and avoid broad hardening advice without service-dependency review.")


def server_exposure_mapper() -> str:
    return _render("SERVER EXPOSURE MAPPER - PHASE 1690", "server-exposure overview", "server_exposure_mapper.json", "exposure_paths", "contained", "exposed", "Exposure paths tracked", "Contained paths", "Exposed paths", "Guardrail: exposure mapping should preserve scope boundaries and avoid implying internet reachability from incomplete local evidence.")
