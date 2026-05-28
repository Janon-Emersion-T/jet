from __future__ import annotations

import json
from pathlib import Path


COSMIC_CIV_DIR = Path("storage/cosmic_civilization")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def recursive_cosmic_exploration_intelligence() -> str:
    payload = _safe_json(COSMIC_CIV_DIR / "cosmic_exploration.json", {})
    expeditions = payload.get("expeditions", []) if isinstance(payload, dict) else []
    recursive = [item for item in expeditions if isinstance(item, dict) and bool(item.get("recursive", False))]
    delayed = [item for item in expeditions if isinstance(item, dict) and bool(item.get("delayed", False))]
    return _overview("RECURSIVE COSMIC EXPLORATION INTELLIGENCE - PHASE 961", "cosmic-exploration overview", [f"Expeditions tracked: {len(expeditions)}", f"Recursive expeditions: {len(recursive)}", f"Delayed expeditions: {len(delayed)}"], "Guardrail: cosmic exploration intelligence should preserve safety, scientific integrity, and human oversight before mission recommendations.")


def autonomous_civilization_expansion_simulator() -> str:
    payload = _safe_json(COSMIC_CIV_DIR / "civilization_expansion.json", {})
    expansions = payload.get("expansions", []) if isinstance(payload, dict) else []
    simulated = [item for item in expansions if isinstance(item, dict) and bool(item.get("simulated", False))]
    unstable = [item for item in expansions if isinstance(item, dict) and bool(item.get("unstable", False))]
    return _overview("AUTONOMOUS CIVILIZATION EXPANSION SIMULATOR - PHASE 962", "civilization-expansion overview", [f"Expansions tracked: {len(expansions)}", f"Simulated expansions: {len(simulated)}", f"Unstable expansions: {len(unstable)}"], "Guardrail: civilization expansion simulations should remain exploratory, non-deterministic, and ethically bounded before use.")


def universal_ethical_adaptation_framework() -> str:
    payload = _safe_json(COSMIC_CIV_DIR / "ethical_adaptation.json", {})
    frameworks = payload.get("frameworks", []) if isinstance(payload, dict) else []
    adapted = [item for item in frameworks if isinstance(item, dict) and bool(item.get("adapted", False))]
    conflicted = [item for item in frameworks if isinstance(item, dict) and bool(item.get("conflicted", False))]
    return _overview("UNIVERSAL ETHICAL ADAPTATION FRAMEWORK - PHASE 963", "ethical-adaptation overview", [f"Frameworks tracked: {len(frameworks)}", f"Adapted frameworks: {len(adapted)}", f"Conflicted frameworks: {len(conflicted)}"], "Guardrail: ethical adaptation should preserve plural values, public scrutiny, and appeal before rollout.")


def ai_assisted_reality_interpretation_engine() -> str:
    payload = _safe_json(COSMIC_CIV_DIR / "reality_interpretation.json", {})
    models = payload.get("models", []) if isinstance(payload, dict) else []
    interpreted = [item for item in models if isinstance(item, dict) and bool(item.get("interpreted", False))]
    noisy = [item for item in models if isinstance(item, dict) and bool(item.get("noisy", False))]
    return _overview("AI-ASSISTED REALITY INTERPRETATION ENGINE - PHASE 964", "reality-interpretation overview", [f"Models tracked: {len(models)}", f"Interpreted models: {len(interpreted)}", f"Noisy models: {len(noisy)}"], "Guardrail: reality interpretation should preserve empirical grounding, uncertainty, and resistance to self-confirming narratives.")


def cross_civilization_memory_federation() -> str:
    payload = _safe_json(COSMIC_CIV_DIR / "memory_federation.json", {})
    federations = payload.get("federations", []) if isinstance(payload, dict) else []
    linked = [item for item in federations if isinstance(item, dict) and bool(item.get("linked", False))]
    incompatible = [item for item in federations if isinstance(item, dict) and bool(item.get("incompatible", False))]
    return _overview("CROSS-CIVILIZATION MEMORY FEDERATION - PHASE 965", "memory-federation overview", [f"Federations tracked: {len(federations)}", f"Linked federations: {len(linked)}", f"Incompatible federations: {len(incompatible)}"], "Guardrail: memory federation should preserve consent, access control, and provenance before interoperability expands.")


def planetary_semantic_synchronization_layer() -> str:
    payload = _safe_json(COSMIC_CIV_DIR / "semantic_synchronization.json", {})
    layers = payload.get("layers", []) if isinstance(payload, dict) else []
    synchronized = [item for item in layers if isinstance(item, dict) and bool(item.get("synchronized", False))]
    drifted = [item for item in layers if isinstance(item, dict) and bool(item.get("drifted", False))]
    return _overview("PLANETARY SEMANTIC SYNCHRONIZATION LAYER - PHASE 966", "semantic-synchronization overview", [f"Layers tracked: {len(layers)}", f"Synchronized layers: {len(synchronized)}", f"Drifted layers: {len(drifted)}"], "Guardrail: semantic synchronization should preserve provenance, ambiguity visibility, and human correction before convergence.")


def autonomous_universal_research_orchestration() -> str:
    payload = _safe_json(COSMIC_CIV_DIR / "research_orchestration.json", {})
    programs = payload.get("programs", []) if isinstance(payload, dict) else []
    orchestrated = [item for item in programs if isinstance(item, dict) and bool(item.get("orchestrated", False))]
    blocked = [item for item in programs if isinstance(item, dict) and bool(item.get("blocked", False))]
    return _overview("AUTONOMOUS UNIVERSAL RESEARCH ORCHESTRATION - PHASE 967", "research-orchestration overview", [f"Programs tracked: {len(programs)}", f"Orchestrated programs: {len(orchestrated)}", f"Blocked programs: {len(blocked)}"], "Guardrail: research orchestration should preserve scientific method, peer review, and explicit approvals before execution.")


def human_machine_civilization_fusion_stack() -> str:
    payload = _safe_json(COSMIC_CIV_DIR / "civilization_fusion.json", {})
    stacks = payload.get("stacks", []) if isinstance(payload, dict) else []
    fused = [item for item in stacks if isinstance(item, dict) and bool(item.get("fused", False))]
    unstable = [item for item in stacks if isinstance(item, dict) and bool(item.get("unstable", False))]
    return _overview("HUMAN-MACHINE CIVILIZATION FUSION STACK - PHASE 968", "civilization-fusion overview", [f"Stacks tracked: {len(stacks)}", f"Fused stacks: {len(fused)}", f"Unstable stacks: {len(unstable)}"], "Guardrail: fusion stacks should preserve human agency, reversibility, and clear oversight before integration.")


def ai_guided_future_species_simulator() -> str:
    payload = _safe_json(COSMIC_CIV_DIR / "future_species.json", {})
    species = payload.get("species", []) if isinstance(payload, dict) else []
    simulated = [item for item in species if isinstance(item, dict) and bool(item.get("simulated", False))]
    contested = [item for item in species if isinstance(item, dict) and bool(item.get("contested", False))]
    return _overview("AI-GUIDED FUTURE SPECIES SIMULATOR - PHASE 969", "future-species overview", [f"Species tracked: {len(species)}", f"Simulated species: {len(simulated)}", f"Contested species: {len(contested)}"], "Guardrail: future species modeling should remain speculative, ethics-bound, and non-prescriptive before interpretation.")


def infinite_recursion_intelligence_sandbox() -> str:
    payload = _safe_json(COSMIC_CIV_DIR / "infinite_recursion.json", {})
    loops = payload.get("loops", []) if isinstance(payload, dict) else []
    sandboxed = [item for item in loops if isinstance(item, dict) and bool(item.get("sandboxed", False))]
    runaway = [item for item in loops if isinstance(item, dict) and bool(item.get("runaway", False))]
    return _overview("INFINITE RECURSION INTELLIGENCE SANDBOX - PHASE 970", "infinite-recursion overview", [f"Loops tracked: {len(loops)}", f"Sandboxed loops: {len(sandboxed)}", f"Runaway loops: {len(runaway)}"], "Guardrail: recursion sandboxes should preserve containment, observability, and kill-switches before experimentation.")
