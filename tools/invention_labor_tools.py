from __future__ import annotations

import json
from pathlib import Path


INVENTION_LABOR_DIR = Path("storage/invention_labor")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_key: str, risk_key: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(INVENTION_LABOR_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_key, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_key, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_intellectual_property_harmonizer() -> str:
    return _render("UNIVERSAL INTELLECTUAL PROPERTY HARMONIZER - PHASE 1111", "ip-harmonization overview", "intellectual_property.json", "claims", "harmonized", "contested", "Claims tracked", "Harmonized claims", "Contested claims", "Guardrail: IP harmonization should preserve creator rights, public-interest exceptions, and appeals before enforcement.")


def adaptive_invention_validation_framework() -> str:
    return _render("ADAPTIVE INVENTION VALIDATION FRAMEWORK - PHASE 1112", "invention-validation overview", "invention_validation.json", "inventions", "validated", "unverified", "Inventions tracked", "Validated inventions", "Unverified inventions", "Guardrail: invention validation should preserve replication, safety checks, and documented evidence before approval.")


def autonomous_prototype_generation_engine() -> str:
    return _render("AUTONOMOUS PROTOTYPE GENERATION ENGINE - PHASE 1113", "prototype-generation overview", "prototype_generation.json", "prototypes", "generated", "unsafe", "Prototypes tracked", "Generated prototypes", "Unsafe prototypes", "Guardrail: prototype generation should preserve sandboxing, review gates, and manufacturing safety before execution.")


def infinite_scale_manufacturing_coordination_ai() -> str:
    return _render("INFINITE-SCALE MANUFACTURING COORDINATION AI - PHASE 1114", "manufacturing-coordination overview", "manufacturing_coordination.json", "plants", "coordinated", "backlogged", "Plants tracked", "Coordinated plants", "Backlogged plants", "Guardrail: manufacturing coordination should preserve labor safety, quality controls, and accountable override before dispatch.")


def recursive_robotics_deployment_framework() -> str:
    return _render("RECURSIVE ROBOTICS DEPLOYMENT FRAMEWORK - PHASE 1115", "robotics-deployment overview", "robotics_deployment.json", "fleets", "deployed", "faulty", "Fleets tracked", "Deployed fleets", "Faulty fleets", "Guardrail: robotics deployment should preserve kill switches, observability, and human supervision before rollout.")


def universal_autonomous_labor_substrate() -> str:
    return _render("UNIVERSAL AUTONOMOUS LABOR SUBSTRATE - PHASE 1116", "autonomous-labor overview", "autonomous_labor.json", "roles", "automated", "displaced", "Roles tracked", "Automated roles", "Displaced roles", "Guardrail: autonomous labor systems should preserve worker dignity, transition planning, and human accountability before replacement.")


def adaptive_workforce_transition_engine() -> str:
    return _render("ADAPTIVE WORKFORCE TRANSITION ENGINE - PHASE 1117", "workforce-transition overview", "workforce_transition.json", "cohorts", "reskilled", "at_risk", "Cohorts tracked", "Reskilled cohorts", "At-risk cohorts", "Guardrail: workforce transitions should preserve support equity, informed participation, and humane pacing before restructuring.")


def autonomous_skill_redistribution_ai() -> str:
    return _render("AUTONOMOUS SKILL REDISTRIBUTION AI - PHASE 1118", "skill-redistribution overview", "skill_redistribution.json", "pathways", "redistributed", "mismatched", "Pathways tracked", "Redistributed pathways", "Mismatched pathways", "Guardrail: skill redistribution should preserve agency, fair access, and transparent matching before assignment.")


def infinite_scale_education_harmonization_layer() -> str:
    return _render("INFINITE-SCALE EDUCATION HARMONIZATION LAYER - PHASE 1119", "education-harmonization overview", "education_harmonization.json", "systems", "harmonized", "uneven", "Systems tracked", "Harmonized systems", "Uneven systems", "Guardrail: education harmonization should preserve local pedagogy, accessibility, and plural curricula before standardization.")


def recursive_personalized_mastery_framework() -> str:
    return _render("RECURSIVE PERSONALIZED MASTERY FRAMEWORK - PHASE 1120", "personalized-mastery overview", "personalized_mastery.json", "learners", "advancing", "stalled", "Learners tracked", "Advancing learners", "Stalled learners", "Guardrail: mastery frameworks should preserve learner autonomy, wellbeing, and non-coercive pacing before optimization.")
