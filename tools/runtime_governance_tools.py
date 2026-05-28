from __future__ import annotations

import json
from pathlib import Path


RUNTIME_SECURITY_DIR = Path("storage/runtime_security")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def semantic_permission_layers() -> str:
    payload = _safe_json(RUNTIME_SECURITY_DIR / "semantic_permissions.json", {})
    layers = payload.get("layers", []) if isinstance(payload, dict) else []
    rules = payload.get("rules", []) if isinstance(payload, dict) else []
    privileged = [item for item in layers if isinstance(item, dict) and item.get("trust") == "privileged"]
    scoped = [item for item in rules if isinstance(item, dict) and bool(item.get("context_scoped", False))]
    return "\n".join(
        [
            "SEMANTIC PERMISSION LAYERS - PHASE 527",
            "Mode: permission-layer overview.",
            f"Permission layers: {len(layers)}",
            f"Privileged layers: {len(privileged)}",
            f"Semantic rules: {len(rules)}",
            f"Context-scoped rules: {len(scoped)}",
            "Guardrail: semantic permissions should stay explainable, least-privileged, and context-bound before any agent receives elevated access.",
        ]
    )


def ai_driven_identity_governance() -> str:
    payload = _safe_json(RUNTIME_SECURITY_DIR / "identity_governance.json", {})
    identities = payload.get("identities", []) if isinstance(payload, dict) else []
    policies = payload.get("policies", []) if isinstance(payload, dict) else []
    stale = [
        item for item in identities if isinstance(item, dict) and int(item.get("last_review_days", 0) or 0) > 90
    ]
    mfa = [item for item in identities if isinstance(item, dict) and bool(item.get("mfa_enforced", False))]
    return "\n".join(
        [
            "AI-DRIVEN IDENTITY GOVERNANCE - PHASE 528",
            "Mode: identity-governance overview.",
            f"Identities tracked: {len(identities)}",
            f"Policies tracked: {len(policies)}",
            f"Stale identities: {len(stale)}",
            f"MFA-enforced identities: {len(mfa)}",
            "Guardrail: identity governance should favor current ownership, strong authentication, and timely review before automating trust decisions.",
        ]
    )


def ai_policy_enforcement_engine() -> str:
    payload = _safe_json(RUNTIME_SECURITY_DIR / "policy_enforcement.json", {})
    events = payload.get("events", []) if isinstance(payload, dict) else []
    controls = payload.get("controls", []) if isinstance(payload, dict) else []
    blocked = [item for item in events if isinstance(item, dict) and item.get("decision") == "blocked"]
    remediating = [item for item in controls if isinstance(item, dict) and bool(item.get("auto_remediation", False))]
    return "\n".join(
        [
            "AI POLICY ENFORCEMENT ENGINE - PHASE 529",
            "Mode: policy-enforcement overview.",
            f"Policy events: {len(events)}",
            f"Blocked events: {len(blocked)}",
            f"Controls tracked: {len(controls)}",
            f"Auto-remediating controls: {len(remediating)}",
            "Guardrail: enforcement automation should preserve traceability, deterministic policy outcomes, and safe rollback paths before intervening.",
        ]
    )


def secure_execution_enclave() -> str:
    payload = _safe_json(RUNTIME_SECURITY_DIR / "execution_enclave.json", {})
    enclaves = payload.get("enclaves", []) if isinstance(payload, dict) else []
    attestations = payload.get("attestations", []) if isinstance(payload, dict) else []
    isolated = [item for item in enclaves if isinstance(item, dict) and bool(item.get("isolated", False))]
    valid = [item for item in attestations if isinstance(item, dict) and item.get("status") == "valid"]
    return "\n".join(
        [
            "SECURE EXECUTION ENCLAVE - PHASE 530",
            "Mode: enclave-readiness overview.",
            f"Enclaves tracked: {len(enclaves)}",
            f"Isolated enclaves: {len(isolated)}",
            f"Attestations tracked: {len(attestations)}",
            f"Valid attestations: {len(valid)}",
            "Guardrail: sensitive execution should prefer isolated runtimes, verifiable attestation, and narrow data exposure before code is promoted.",
        ]
    )
