from __future__ import annotations

import json
from pathlib import Path


HUMAN_SUPPORT_DIR = Path("storage/human_support_accessibility")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def archaeological_simulation_assistant() -> str:
    payload = _safe_json(HUMAN_SUPPORT_DIR / "archaeology.json", {})
    sites = payload.get("sites", []) if isinstance(payload, dict) else []
    modeled = [item for item in sites if isinstance(item, dict) and bool(item.get("modeled", False))]
    fragile = [item for item in sites if isinstance(item, dict) and item.get("risk") == "fragile"]
    return _overview("ARCHAEOLOGICAL SIMULATION ASSISTANT - PHASE 711", "archaeology-simulation overview", [f"Sites tracked: {len(sites)}", f"Modeled sites: {len(modeled)}", f"Fragile sites: {len(fragile)}"], "Guardrail: archaeology simulations should preserve evidentiary humility, stewardship, and site protection before public claims.")


def language_revival_framework() -> str:
    payload = _safe_json(HUMAN_SUPPORT_DIR / "language_revival.json", {})
    languages = payload.get("languages", []) if isinstance(payload, dict) else []
    active = [item for item in languages if isinstance(item, dict) and item.get("status") == "active"]
    community = [item for item in languages if isinstance(item, dict) and bool(item.get("community_led", False))]
    return _overview("LANGUAGE REVIVAL FRAMEWORK - PHASE 712", "language-revival overview", [f"Languages tracked: {len(languages)}", f"Active language programs: {len(active)}", f"Community-led programs: {len(community)}"], "Guardrail: language revival should remain community-led, consent-aware, and culturally grounded before automation scales.")


def autonomous_education_civilization_model() -> str:
    payload = _safe_json(HUMAN_SUPPORT_DIR / "education_civilization.json", {})
    systems = payload.get("systems", []) if isinstance(payload, dict) else []
    adaptive = [item for item in systems if isinstance(item, dict) and bool(item.get("adaptive", False))]
    equitable = [item for item in systems if isinstance(item, dict) and bool(item.get("equitable", False))]
    return _overview("AUTONOMOUS EDUCATION CIVILIZATION MODEL - PHASE 713", "education-civilization overview", [f"Systems tracked: {len(systems)}", f"Adaptive systems: {len(adaptive)}", f"Equity-aware systems: {len(equitable)}"], "Guardrail: civilization-scale education models should prioritize equity, developmental fit, and educator oversight before prescription.")


def personalized_lifelong_learning_ai() -> str:
    payload = _safe_json(HUMAN_SUPPORT_DIR / "lifelong_learning.json", {})
    learners = payload.get("learners", []) if isinstance(payload, dict) else []
    active = [item for item in learners if isinstance(item, dict) and item.get("status") == "active"]
    personalized = [item for item in learners if isinstance(item, dict) and bool(item.get("personalized", False))]
    return _overview("PERSONALIZED LIFELONG LEARNING AI - PHASE 714", "lifelong-learning overview", [f"Learners tracked: {len(learners)}", f"Active learners: {len(active)}", f"Personalized paths: {len(personalized)}"], "Guardrail: lifelong learning personalization should remain transparent, learner-controlled, and supportive rather than coercive.")


def ai_guided_childhood_education() -> str:
    payload = _safe_json(HUMAN_SUPPORT_DIR / "childhood_education.json", {})
    cohorts = payload.get("cohorts", []) if isinstance(payload, dict) else []
    supervised = [item for item in cohorts if isinstance(item, dict) and bool(item.get("supervised", False))]
    age_fit = [item for item in cohorts if isinstance(item, dict) and bool(item.get("age_appropriate", False))]
    return _overview("AI-GUIDED CHILDHOOD EDUCATION - PHASE 715", "childhood-education overview", [f"Cohorts tracked: {len(cohorts)}", f"Supervised cohorts: {len(supervised)}", f"Age-appropriate cohorts: {len(age_fit)}"], "Guardrail: childhood education systems should remain adult-supervised, age-appropriate, and child-safety-first before adaptation.")


def cognitive_development_assistant() -> str:
    payload = _safe_json(HUMAN_SUPPORT_DIR / "cognitive_development.json", {})
    profiles = payload.get("profiles", []) if isinstance(payload, dict) else []
    supported = [item for item in profiles if isinstance(item, dict) and bool(item.get("supported", False))]
    reviewed = [item for item in profiles if isinstance(item, dict) and bool(item.get("reviewed", False))]
    return _overview("COGNITIVE DEVELOPMENT ASSISTANT - PHASE 716", "cognitive-development overview", [f"Profiles tracked: {len(profiles)}", f"Supported profiles: {len(supported)}", f"Reviewed profiles: {len(reviewed)}"], "Guardrail: cognitive development support should remain caregiver-aware, non-diagnostic, and careful with sensitive developmental inferences.")


def elderly_care_ai_ecosystem() -> str:
    payload = _safe_json(HUMAN_SUPPORT_DIR / "elderly_care.json", {})
    care_plans = payload.get("care_plans", []) if isinstance(payload, dict) else []
    assisted = [item for item in care_plans if isinstance(item, dict) and bool(item.get("assisted", False))]
    urgent = [item for item in care_plans if isinstance(item, dict) and item.get("priority") == "urgent"]
    return _overview("ELDERLY CARE AI ECOSYSTEM - PHASE 717", "elderly-care overview", [f"Care plans tracked: {len(care_plans)}", f"Assisted care plans: {len(assisted)}", f"Urgent care plans: {len(urgent)}"], "Guardrail: elderly care automation should center dignity, consent, and human support before intervention.")


def accessibility_first_ai_framework() -> str:
    payload = _safe_json(HUMAN_SUPPORT_DIR / "accessibility_framework.json", {})
    services = payload.get("services", []) if isinstance(payload, dict) else []
    compliant = [item for item in services if isinstance(item, dict) and bool(item.get("accessible", False))]
    gaps = [item for item in services if isinstance(item, dict) and bool(item.get("gap", False))]
    return _overview("ACCESSIBILITY-FIRST AI FRAMEWORK - PHASE 718", "accessibility-framework overview", [f"Services tracked: {len(services)}", f"Accessible services: {len(compliant)}", f"Accessibility gaps: {len(gaps)}"], "Guardrail: accessibility-first systems should privilege universal access, user testing, and fallback support before release.")


def ai_sign_language_interpreter() -> str:
    payload = _safe_json(HUMAN_SUPPORT_DIR / "sign_language.json", {})
    sessions = payload.get("sessions", []) if isinstance(payload, dict) else []
    translated = [item for item in sessions if isinstance(item, dict) and bool(item.get("translated", False))]
    reviewed = [item for item in sessions if isinstance(item, dict) and bool(item.get("reviewed", False))]
    return _overview("AI SIGN-LANGUAGE INTERPRETER - PHASE 719", "sign-language overview", [f"Sessions tracked: {len(sessions)}", f"Translated sessions: {len(translated)}", f"Reviewed sessions: {len(reviewed)}"], "Guardrail: sign-language systems should preserve signer nuance, consent, and human review for sensitive communication.")


def visual_impairment_assistant() -> str:
    payload = _safe_json(HUMAN_SUPPORT_DIR / "visual_impairment.json", {})
    supports = payload.get("supports", []) if isinstance(payload, dict) else []
    active = [item for item in supports if isinstance(item, dict) and item.get("status") == "active"]
    high_conf = [item for item in supports if isinstance(item, dict) and bool(item.get("high_confidence", False))]
    return _overview("VISUAL IMPAIRMENT ASSISTANT - PHASE 720", "visual-support overview", [f"Support sessions: {len(supports)}", f"Active sessions: {len(active)}", f"High-confidence sessions: {len(high_conf)}"], "Guardrail: visual assistance should prioritize safety, confidence disclosure, and user control before guidance.")
