from __future__ import annotations

import json
from pathlib import Path


AUGMENTATION_DIR = Path("storage/augmentation_identity")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def hearing_enhancement_ai() -> str:
    payload = _safe_json(AUGMENTATION_DIR / "hearing_enhancement.json", {})
    profiles = payload.get("profiles", []) if isinstance(payload, dict) else []
    tuned = [item for item in profiles if isinstance(item, dict) and bool(item.get("tuned", False))]
    safe = [item for item in profiles if isinstance(item, dict) and bool(item.get("safe_levels", False))]
    return _overview("HEARING ENHANCEMENT AI - PHASE 721", "hearing-enhancement overview", [f"Profiles tracked: {len(profiles)}", f"Tuned profiles: {len(tuned)}", f"Safe-level profiles: {len(safe)}"], "Guardrail: hearing enhancement should preserve user comfort, audiology context, and safe levels before adaptation.")


def ai_mobility_assistant() -> str:
    payload = _safe_json(AUGMENTATION_DIR / "mobility_assistant.json", {})
    journeys = payload.get("journeys", []) if isinstance(payload, dict) else []
    assisted = [item for item in journeys if isinstance(item, dict) and bool(item.get("assisted", False))]
    accessible = [item for item in journeys if isinstance(item, dict) and bool(item.get("accessible", False))]
    return _overview("AI MOBILITY ASSISTANT - PHASE 722", "mobility-assistant overview", [f"Journeys tracked: {len(journeys)}", f"Assisted journeys: {len(assisted)}", f"Accessible journeys: {len(accessible)}"], "Guardrail: mobility assistance should prioritize safety, route reliability, and user consent before navigation guidance.")


def human_augmentation_interface() -> str:
    payload = _safe_json(AUGMENTATION_DIR / "human_augmentation.json", {})
    interfaces = payload.get("interfaces", []) if isinstance(payload, dict) else []
    calibrated = [item for item in interfaces if isinstance(item, dict) and bool(item.get("calibrated", False))]
    approved = [item for item in interfaces if isinstance(item, dict) and item.get("status") == "approved"]
    return _overview("HUMAN AUGMENTATION INTERFACE - PHASE 723", "human-augmentation overview", [f"Interfaces tracked: {len(interfaces)}", f"Calibrated interfaces: {len(calibrated)}", f"Approved interfaces: {len(approved)}"], "Guardrail: augmentation interfaces should remain safety-bounded, consent-driven, and medically/ethically reviewed before use.")


def cognitive_enhancement_layer() -> str:
    payload = _safe_json(AUGMENTATION_DIR / "cognitive_enhancement.json", {})
    programs = payload.get("programs", []) if isinstance(payload, dict) else []
    adaptive = [item for item in programs if isinstance(item, dict) and bool(item.get("adaptive", False))]
    reviewed = [item for item in programs if isinstance(item, dict) and bool(item.get("reviewed", False))]
    return _overview("COGNITIVE ENHANCEMENT LAYER - PHASE 724", "cognitive-enhancement overview", [f"Programs tracked: {len(programs)}", f"Adaptive programs: {len(adaptive)}", f"Reviewed programs: {len(reviewed)}"], "Guardrail: cognitive enhancement should remain non-coercive, evidence-aware, and human-supervised before personalization.")


def neural_memory_augmentation() -> str:
    payload = _safe_json(AUGMENTATION_DIR / "neural_memory.json", {})
    sessions = payload.get("sessions", []) if isinstance(payload, dict) else []
    encoded = [item for item in sessions if isinstance(item, dict) and bool(item.get("encoded", False))]
    consented = [item for item in sessions if isinstance(item, dict) and bool(item.get("consented", False))]
    return _overview("NEURAL MEMORY AUGMENTATION - PHASE 725", "neural-memory overview", [f"Sessions tracked: {len(sessions)}", f"Encoded sessions: {len(encoded)}", f"Consented sessions: {len(consented)}"], "Guardrail: neural memory systems should remain consent-heavy, reversible where possible, and explicit about limitations before use.")


def personalized_reasoning_assistant() -> str:
    payload = _safe_json(AUGMENTATION_DIR / "personal_reasoning.json", {})
    sessions = payload.get("sessions", []) if isinstance(payload, dict) else []
    tailored = [item for item in sessions if isinstance(item, dict) and bool(item.get("tailored", False))]
    reviewed = [item for item in sessions if isinstance(item, dict) and bool(item.get("reviewed", False))]
    return _overview("PERSONALIZED REASONING ASSISTANT - PHASE 726", "personal-reasoning overview", [f"Sessions tracked: {len(sessions)}", f"Tailored sessions: {len(tailored)}", f"Reviewed sessions: {len(reviewed)}"], "Guardrail: reasoning personalization should preserve autonomy, transparency, and non-manipulative support before adapting advice.")


def ai_creativity_amplifier() -> str:
    payload = _safe_json(AUGMENTATION_DIR / "creativity_amplifier.json", {})
    projects = payload.get("projects", []) if isinstance(payload, dict) else []
    amplified = [item for item in projects if isinstance(item, dict) and bool(item.get("amplified", False))]
    attributed = [item for item in projects if isinstance(item, dict) and bool(item.get("attributed", False))]
    return _overview("AI CREATIVITY AMPLIFIER - PHASE 727", "creativity-amplifier overview", [f"Projects tracked: {len(projects)}", f"Amplified projects: {len(amplified)}", f"Attributed projects: {len(attributed)}"], "Guardrail: creative amplification should preserve authorship, attribution, and user agency rather than substituting authorship.")


def dream_simulation_sandbox() -> str:
    payload = _safe_json(AUGMENTATION_DIR / "dream_simulation.json", {})
    simulations = payload.get("simulations", []) if isinstance(payload, dict) else []
    vivid = [item for item in simulations if isinstance(item, dict) and bool(item.get("vivid", False))]
    bounded = [item for item in simulations if isinstance(item, dict) and bool(item.get("bounded", False))]
    return _overview("DREAM SIMULATION SANDBOX - PHASE 728", "dream-simulation overview", [f"Simulations tracked: {len(simulations)}", f"Vivid simulations: {len(vivid)}", f"Bounded simulations: {len(bounded)}"], "Guardrail: dream simulation should remain clearly fictional, psychologically careful, and user-controlled before immersive use.")


def consciousness_research_framework() -> str:
    payload = _safe_json(AUGMENTATION_DIR / "consciousness_research.json", {})
    studies = payload.get("studies", []) if isinstance(payload, dict) else []
    active = [item for item in studies if isinstance(item, dict) and item.get("status") == "active"]
    controversial = [item for item in studies if isinstance(item, dict) and bool(item.get("controversial", False))]
    return _overview("CONSCIOUSNESS RESEARCH FRAMEWORK - PHASE 729", "consciousness-research overview", [f"Studies tracked: {len(studies)}", f"Active studies: {len(active)}", f"Controversial studies: {len(controversial)}"], "Guardrail: consciousness research should preserve epistemic humility, ethical review, and clear boundaries between hypothesis and claim.")


def ai_introspection_engine() -> str:
    payload = _safe_json(AUGMENTATION_DIR / "introspection_engine.json", {})
    traces = payload.get("traces", []) if isinstance(payload, dict) else []
    explainable = [item for item in traces if isinstance(item, dict) and bool(item.get("explainable", False))]
    uncertain = [item for item in traces if isinstance(item, dict) and bool(item.get("uncertain", False))]
    return _overview("AI INTROSPECTION ENGINE - PHASE 730", "introspection overview", [f"Traces tracked: {len(traces)}", f"Explainable traces: {len(explainable)}", f"Uncertain traces: {len(uncertain)}"], "Guardrail: introspection should surface uncertainty and limits instead of pretending access to hidden certainty.")
