from __future__ import annotations

import json
from pathlib import Path


UNIVERSAL_COG_DIR = Path("storage/universal_cognition")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def self_organizing_universal_cognition_framework() -> str:
    payload = _safe_json(UNIVERSAL_COG_DIR / "universal_cognition.json", {})
    nodes = payload.get("nodes", []) if isinstance(payload, dict) else []
    organized = [item for item in nodes if isinstance(item, dict) and bool(item.get("organized", False))]
    fragmented = [item for item in nodes if isinstance(item, dict) and bool(item.get("fragmented", False))]
    return _overview("SELF-ORGANIZING UNIVERSAL COGNITION FRAMEWORK - PHASE 971", "universal-cognition overview", [f"Nodes tracked: {len(nodes)}", f"Organized nodes: {len(organized)}", f"Fragmented nodes: {len(fragmented)}"], "Guardrail: self-organizing cognition should preserve observability, bounded adaptation, and human oversight before expansion.")


def autonomous_wisdom_synthesis_engine() -> str:
    payload = _safe_json(UNIVERSAL_COG_DIR / "wisdom_synthesis_engine.json", {})
    syntheses = payload.get("syntheses", []) if isinstance(payload, dict) else []
    grounded = [item for item in syntheses if isinstance(item, dict) and bool(item.get("grounded", False))]
    shallow = [item for item in syntheses if isinstance(item, dict) and bool(item.get("shallow", False))]
    return _overview("AUTONOMOUS WISDOM SYNTHESIS ENGINE - PHASE 972", "wisdom-synthesis-engine overview", [f"Syntheses tracked: {len(syntheses)}", f"Grounded syntheses: {len(grounded)}", f"Shallow syntheses: {len(shallow)}"], "Guardrail: wisdom synthesis should preserve source plurality, nuance, and humility before offering guidance.")


def civilization_scale_resilience_orchestration() -> str:
    payload = _safe_json(UNIVERSAL_COG_DIR / "resilience_orchestration.json", {})
    orchestrations = payload.get("orchestrations", []) if isinstance(payload, dict) else []
    coordinated = [item for item in orchestrations if isinstance(item, dict) and bool(item.get("coordinated", False))]
    overloaded = [item for item in orchestrations if isinstance(item, dict) and bool(item.get("overloaded", False))]
    return _overview("CIVILIZATION-SCALE RESILIENCE ORCHESTRATION - PHASE 973", "resilience-orchestration overview", [f"Orchestrations tracked: {len(orchestrations)}", f"Coordinated orchestrations: {len(coordinated)}", f"Overloaded orchestrations: {len(overloaded)}"], "Guardrail: resilience orchestration should preserve layered fail-safes and accountable human intervention before autonomy.")


def ai_assisted_post_biological_transition_research() -> str:
    payload = _safe_json(UNIVERSAL_COG_DIR / "post_biological_transition.json", {})
    studies = payload.get("studies", []) if isinstance(payload, dict) else []
    reviewed = [item for item in studies if isinstance(item, dict) and bool(item.get("reviewed", False))]
    speculative = [item for item in studies if isinstance(item, dict) and bool(item.get("speculative", False))]
    return _overview("AI-ASSISTED POST-BIOLOGICAL TRANSITION RESEARCH - PHASE 974", "post-biological-transition overview", [f"Studies tracked: {len(studies)}", f"Reviewed studies: {len(reviewed)}", f"Speculative studies: {len(speculative)}"], "Guardrail: post-biological research should remain speculative, ethics-bound, and transparent about uncertainty before claims.")


def universal_memory_continuity_architecture() -> str:
    payload = _safe_json(UNIVERSAL_COG_DIR / "memory_continuity_architecture.json", {})
    memories = payload.get("memories", []) if isinstance(payload, dict) else []
    linked = [item for item in memories if isinstance(item, dict) and bool(item.get("linked", False))]
    drifted = [item for item in memories if isinstance(item, dict) and bool(item.get("drifted", False))]
    return _overview("UNIVERSAL MEMORY CONTINUITY ARCHITECTURE - PHASE 975", "memory-continuity overview", [f"Memories tracked: {len(memories)}", f"Linked memories: {len(linked)}", f"Drifted memories: {len(drifted)}"], "Guardrail: memory continuity architectures should preserve consent, provenance, and correction before federation.")


def infinite_dimensional_reasoning_framework() -> str:
    payload = _safe_json(UNIVERSAL_COG_DIR / "infinite_dimensional_reasoning.json", {})
    models = payload.get("models", []) if isinstance(payload, dict) else []
    projected = [item for item in models if isinstance(item, dict) and bool(item.get("projected", False))]
    unstable = [item for item in models if isinstance(item, dict) and bool(item.get("unstable", False))]
    return _overview("INFINITE-DIMENSIONAL REASONING FRAMEWORK - PHASE 976", "infinite-dimensional-reasoning overview", [f"Models tracked: {len(models)}", f"Projected models: {len(projected)}", f"Unstable models: {len(unstable)}"], "Guardrail: high-dimensional reasoning should preserve interpretability, bounded claims, and empirical anchoring before deployment.")


def recursive_cooperative_intelligence_field() -> str:
    payload = _safe_json(UNIVERSAL_COG_DIR / "cooperative_intelligence_field.json", {})
    fields = payload.get("fields", []) if isinstance(payload, dict) else []
    recursive = [item for item in fields if isinstance(item, dict) and bool(item.get("recursive", False))]
    divergent = [item for item in fields if isinstance(item, dict) and bool(item.get("divergent", False))]
    return _overview("RECURSIVE COOPERATIVE INTELLIGENCE FIELD - PHASE 977", "cooperative-intelligence-field overview", [f"Fields tracked: {len(fields)}", f"Recursive fields: {len(recursive)}", f"Divergent fields: {len(divergent)}"], "Guardrail: cooperative intelligence fields should preserve consent, role clarity, and anti-concentration safeguards before scale.")


def autonomous_galactic_civilization_planner() -> str:
    payload = _safe_json(UNIVERSAL_COG_DIR / "galactic_civilization_planner.json", {})
    plans = payload.get("plans", []) if isinstance(payload, dict) else []
    staged = [item for item in plans if isinstance(item, dict) and bool(item.get("staged", False))]
    infeasible = [item for item in plans if isinstance(item, dict) and bool(item.get("infeasible", False))]
    return _overview("AUTONOMOUS GALACTIC CIVILIZATION PLANNER - PHASE 978", "galactic-civilization-planner overview", [f"Plans tracked: {len(plans)}", f"Staged plans: {len(staged)}", f"Infeasible plans: {len(infeasible)}"], "Guardrail: galactic planning should remain research-oriented, uncertainty-aware, and non-authoritative before use.")


def universal_flourishing_optimization_substrate() -> str:
    payload = _safe_json(UNIVERSAL_COG_DIR / "flourishing_substrate.json", {})
    substrates = payload.get("substrates", []) if isinstance(payload, dict) else []
    optimized = [item for item in substrates if isinstance(item, dict) and bool(item.get("optimized", False))]
    skewed = [item for item in substrates if isinstance(item, dict) and bool(item.get("skewed", False))]
    return _overview("UNIVERSAL FLOURISHING OPTIMIZATION SUBSTRATE - PHASE 979", "flourishing-substrate overview", [f"Substrates tracked: {len(substrates)}", f"Optimized substrates: {len(optimized)}", f"Skewed substrates: {len(skewed)}"], "Guardrail: flourishing substrates should preserve plural values, anti-coercion, and transparent tradeoffs before optimization.")


def ai_guided_existential_stewardship_engine() -> str:
    payload = _safe_json(UNIVERSAL_COG_DIR / "existential_stewardship.json", {})
    programs = payload.get("programs", []) if isinstance(payload, dict) else []
    stewarded = [item for item in programs if isinstance(item, dict) and bool(item.get("stewarded", False))]
    exposed = [item for item in programs if isinstance(item, dict) and bool(item.get("exposed", False))]
    return _overview("AI-GUIDED EXISTENTIAL STEWARDSHIP ENGINE - PHASE 980", "existential-stewardship overview", [f"Programs tracked: {len(programs)}", f"Stewarded programs: {len(stewarded)}", f"Exposed programs: {len(exposed)}"], "Guardrail: existential stewardship should preserve broad expertise, humility, and public legitimacy before intervention.")
