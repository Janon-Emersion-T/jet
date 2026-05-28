from __future__ import annotations

import json
from pathlib import Path


COMPLIANCE_DIR = Path("storage/compliance_governance")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def _readiness(path_name: str, phase: int, title: str) -> str:
    payload = _safe_json(COMPLIANCE_DIR / path_name, {})
    controls = payload.get("controls", []) if isinstance(payload, dict) else []
    gaps = [item for item in controls if isinstance(item, dict) and item.get("status") == "gap"]
    ready = [item for item in controls if isinstance(item, dict) and item.get("status") == "ready"]
    return _overview(
        f"{title} - PHASE {phase}",
        "compliance-readiness overview",
        [
            f"Controls tracked: {len(controls)}",
            f"Ready controls: {len(ready)}",
            f"Gap controls: {len(gaps)}",
        ],
        "Guardrail: readiness reporting should distinguish verified evidence from planned work before claiming conformance.",
    )


def gdpr_readiness_analyzer() -> str:
    return _readiness("gdpr.json", 544, "GDPR READINESS ANALYZER")


def iso_compliance_assistant() -> str:
    return _readiness("iso.json", 545, "ISO COMPLIANCE ASSISTANT")


def pci_dss_readiness_engine() -> str:
    return _readiness("pci_dss.json", 546, "PCI-DSS READINESS ENGINE")


def hipaa_compliance_sandbox() -> str:
    return _readiness("hipaa.json", 547, "HIPAA COMPLIANCE SANDBOX")


def enterprise_governance_framework() -> str:
    payload = _safe_json(COMPLIANCE_DIR / "governance.json", {})
    councils = payload.get("councils", []) if isinstance(payload, dict) else []
    policies = payload.get("policies", []) if isinstance(payload, dict) else []
    active = [item for item in councils if isinstance(item, dict) and item.get("status") == "active"]
    approved = [item for item in policies if isinstance(item, dict) and item.get("status") == "approved"]
    return _overview(
        "ENTERPRISE GOVERNANCE FRAMEWORK - PHASE 548",
        "enterprise-governance overview",
        [
            f"Governance councils: {len(councils)}",
            f"Active councils: {len(active)}",
            f"Policies tracked: {len(policies)}",
            f"Approved policies: {len(approved)}",
        ],
        "Guardrail: governance summaries should reflect accountable ownership, approved policy state, and review cadence before expanding decision power.",
    )


def ai_legal_reasoning_layer() -> str:
    payload = _safe_json(COMPLIANCE_DIR / "legal_reasoning.json", {})
    briefs = payload.get("briefs", []) if isinstance(payload, dict) else []
    reviewed = [item for item in briefs if isinstance(item, dict) and bool(item.get("human_reviewed", False))]
    high_risk = [item for item in briefs if isinstance(item, dict) and item.get("risk") == "high"]
    return _overview(
        "AI LEGAL REASONING LAYER - PHASE 549",
        "legal-reasoning overview",
        [
            f"Legal briefs: {len(briefs)}",
            f"Human-reviewed briefs: {len(reviewed)}",
            f"High-risk briefs: {len(high_risk)}",
        ],
        "Guardrail: legal reasoning should remain advisory, source-grounded, and lawyer-reviewable before it influences obligations.",
    )


def ai_policy_drafting_engine() -> str:
    payload = _safe_json(COMPLIANCE_DIR / "policy_drafting.json", {})
    drafts = payload.get("drafts", []) if isinstance(payload, dict) else []
    approved = [item for item in drafts if isinstance(item, dict) and item.get("status") == "approved"]
    awaiting = [item for item in drafts if isinstance(item, dict) and item.get("status") == "review"]
    return _overview(
        "AI POLICY DRAFTING ENGINE - PHASE 550",
        "policy-drafting overview",
        [
            f"Drafts tracked: {len(drafts)}",
            f"Approved drafts: {len(approved)}",
            f"Drafts awaiting review: {len(awaiting)}",
        ],
        "Guardrail: policy drafting should preserve version clarity, accountable approval, and legal review before publication.",
    )
