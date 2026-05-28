from __future__ import annotations

import json
from pathlib import Path


CREATIVE_VIRTUALIZATION_DIR = Path("storage/creative_virtualization")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_key: str, risk_key: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(CREATIVE_VIRTUALIZATION_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_key, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_key, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def autonomous_collaborative_creativity_network() -> str:
    return _render("AUTONOMOUS COLLABORATIVE CREATIVITY NETWORK - PHASE 1088", "collaborative-creativity overview", "collaborative_creativity.json", "collectives", "collaborating", "blocked", "Collectives tracked", "Collaborating collectives", "Blocked collectives", "Guardrail: collaborative creativity should preserve attribution, consent, and human editorial choice before publication.")


def infinite_scale_artistic_synthesis_engine() -> str:
    return _render("INFINITE-SCALE ARTISTIC SYNTHESIS ENGINE - PHASE 1089", "artistic-synthesis overview", "artistic_synthesis.json", "works", "synthesized", "derivative", "Works tracked", "Synthesized works", "Derivative works", "Guardrail: artistic synthesis should preserve authorship clarity, licensing, and human curation before release.")


def recursive_cinematic_intelligence_runtime() -> str:
    return _render("RECURSIVE CINEMATIC INTELLIGENCE RUNTIME - PHASE 1090", "cinematic-intelligence overview", "cinematic_intelligence.json", "productions", "orchestrated", "disjointed", "Productions tracked", "Orchestrated productions", "Disjointed productions", "Guardrail: cinematic intelligence should preserve safety, authorship, and editorial accountability before production use.")


def universal_narrative_evolution_framework() -> str:
    return _render("UNIVERSAL NARRATIVE EVOLUTION FRAMEWORK - PHASE 1091", "narrative-evolution overview", "narrative_evolution.json", "narratives", "evolving", "stalled", "Narratives tracked", "Evolving narratives", "Stalled narratives", "Guardrail: narrative evolution should preserve cultural context, authorship, and revision transparency before adaptation.")


def adaptive_mythology_generation_engine() -> str:
    return _render("ADAPTIVE MYTHOLOGY GENERATION ENGINE - PHASE 1092", "mythology-generation overview", "mythology_generation.json", "myths", "generated", "appropriative", "Myths tracked", "Generated myths", "Appropriative myths", "Guardrail: mythology generation should preserve cultural respect, provenance, and human stewardship before circulation.")


def autonomous_symbolic_culture_simulator() -> str:
    return _render("AUTONOMOUS SYMBOLIC CULTURE SIMULATOR - PHASE 1093", "symbolic-culture overview", "symbolic_culture.json", "cultures", "simulated", "flattened", "Cultures tracked", "Simulated cultures", "Flattened cultures", "Guardrail: culture simulation should preserve nuance, community authority, and anti-stereotyping safeguards before use.")


def infinite_scale_storytelling_cognition_layer() -> str:
    return _render("INFINITE-SCALE STORYTELLING COGNITION LAYER - PHASE 1094", "storytelling-cognition overview", "storytelling_cognition.json", "storyworlds", "coherent", "fragmented", "Storyworlds tracked", "Coherent storyworlds", "Fragmented storyworlds", "Guardrail: storytelling cognition should preserve coherence, authorship, and audience safety before publication.")


def recursive_virtual_civilization_framework() -> str:
    return _render("RECURSIVE VIRTUAL CIVILIZATION FRAMEWORK - PHASE 1095", "virtual-civilization overview", "virtual_civilization.json", "civilizations", "running", "unstable", "Civilizations tracked", "Running civilizations", "Unstable civilizations", "Guardrail: virtual civilization modeling should preserve sandbox boundaries, observability, and non-transfer assumptions before inference.")


def universal_simulation_interoperability_mesh() -> str:
    return _render("UNIVERSAL SIMULATION INTEROPERABILITY MESH - PHASE 1096", "simulation-interoperability overview", "simulation_interoperability.json", "simulations", "interoperable", "isolated", "Simulations tracked", "Interoperable simulations", "Isolated simulations", "Guardrail: simulation interoperability should preserve schema clarity, provenance, and compatibility review before exchange.")


def adaptive_reality_construction_engine() -> str:
    return _render("ADAPTIVE REALITY CONSTRUCTION ENGINE - PHASE 1097", "reality-construction overview", "reality_construction.json", "worlds", "constructed", "incoherent", "Worlds tracked", "Constructed worlds", "Incoherent worlds", "Guardrail: reality construction should preserve user consent, psychological safety, and explicit framing before immersion.")
