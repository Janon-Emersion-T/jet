from __future__ import annotations

import json
from pathlib import Path


GOVERNANCE_OPERATIONS_DIR = Path("storage/governance_operations")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, pos: str, risk: str, key_label: str, pos_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(GOVERNANCE_OPERATIONS_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(pos, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{pos_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_accountability_framework() -> str:
    return _render("UNIVERSAL ACCOUNTABILITY FRAMEWORK - PHASE 1151", "accountability overview", "accountability.json", "controls", "accountable", "opaque", "Controls tracked", "Accountable controls", "Opaque controls", "Guardrail: accountability systems should preserve traceability, appeals, and human responsibility before enforcement.")


def adaptive_transparency_optimization_engine() -> str:
    return _render("ADAPTIVE TRANSPARENCY OPTIMIZATION ENGINE - PHASE 1152", "transparency overview", "transparency_optimization.json", "disclosures", "optimized", "withheld", "Disclosures tracked", "Optimized disclosures", "Withheld disclosures", "Guardrail: transparency optimization should preserve privacy, public-interest disclosure, and non-deceptive framing before rollout.")


def autonomous_corruption_detection_ai() -> str:
    return _render("AUTONOMOUS CORRUPTION DETECTION AI - PHASE 1153", "corruption-detection overview", "corruption_detection.json", "signals", "flagged", "missed", "Signals tracked", "Flagged signals", "Missed signals", "Guardrail: corruption detection should preserve due process, evidence review, and anti-bias checks before escalation.")


def infinite_scale_institutional_resilience_framework() -> str:
    return _render("INFINITE-SCALE INSTITUTIONAL RESILIENCE FRAMEWORK - PHASE 1154", "institutional-resilience overview", "institutional_resilience.json", "institutions", "resilient", "fragile", "Institutions tracked", "Resilient institutions", "Fragile institutions", "Guardrail: institutional resilience planning should preserve legitimacy, continuity safeguards, and public oversight before intervention.")


def recursive_governance_continuity_engine() -> str:
    return _render("RECURSIVE GOVERNANCE CONTINUITY ENGINE - PHASE 1155", "governance-continuity overview", "governance_continuity.json", "plans", "continuous", "disrupted", "Plans tracked", "Continuous plans", "Disrupted plans", "Guardrail: governance continuity should preserve lawful succession, checks and balances, and human review before activation.")


def universal_civilization_audit_substrate() -> str:
    return _render("UNIVERSAL CIVILIZATION AUDIT SUBSTRATE - PHASE 1156", "civilization-audit overview", "civilization_audit.json", "audits", "audited", "blind", "Audits tracked", "Audited systems", "Blind systems", "Guardrail: civilization audits should preserve proportionality, transparency, and verifiable evidence before scoring.")


def adaptive_planetary_operations_intelligence() -> str:
    return _render("ADAPTIVE PLANETARY OPERATIONS INTELLIGENCE - PHASE 1157", "planetary-operations overview", "planetary_operations.json", "operations", "coordinated", "delayed", "Operations tracked", "Coordinated operations", "Delayed operations", "Guardrail: planetary operations intelligence should preserve locality, accountability, and fallback paths before orchestration.")


def autonomous_infrastructure_harmonizer() -> str:
    return _render("AUTONOMOUS INFRASTRUCTURE HARMONIZER - PHASE 1158", "infrastructure-harmonization overview", "infrastructure_harmonizer.json", "infrastructures", "harmonized", "misaligned", "Infrastructures tracked", "Harmonized infrastructures", "Misaligned infrastructures", "Guardrail: infrastructure harmonization should preserve safety, interoperability review, and human override before changes.")


def infinite_scale_systems_orchestration_ai() -> str:
    return _render("INFINITE-SCALE SYSTEMS ORCHESTRATION AI - PHASE 1159", "systems-orchestration overview", "systems_orchestration.json", "systems", "orchestrated", "overloaded", "Systems tracked", "Orchestrated systems", "Overloaded systems", "Guardrail: systems orchestration should preserve observability, layered control, and braking mechanisms before automation.")


def recursive_complexity_management_engine() -> str:
    return _render("RECURSIVE COMPLEXITY MANAGEMENT ENGINE - PHASE 1160", "complexity-management overview", "complexity_management.json", "models", "managed", "entangled", "Models tracked", "Managed models", "Entangled models", "Guardrail: complexity management should preserve interpretability, decomposition, and reviewable abstractions before optimization.")
