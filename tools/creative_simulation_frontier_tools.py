from __future__ import annotations

import json
from pathlib import Path


CREATIVE_FRONTIER_DIR = Path("storage/creative_simulation_frontier")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def autonomous_creativity_engine() -> str:
    payload = _safe_json(CREATIVE_FRONTIER_DIR / "creativity_engine.json", {})
    concepts = payload.get("concepts", []) if isinstance(payload, dict) else []
    explored = [item for item in concepts if isinstance(item, dict) and bool(item.get("explored", False))]
    curated = [item for item in concepts if isinstance(item, dict) and bool(item.get("curated", False))]
    return _overview("AUTONOMOUS CREATIVITY ENGINE - PHASE 681", "creativity-engine overview", [f"Concepts tracked: {len(concepts)}", f"Explored concepts: {len(explored)}", f"Curated concepts: {len(curated)}"], "Guardrail: creative exploration should preserve authorship context, curation, and human taste rather than pretending objectivity.")


def narrative_intelligence_framework() -> str:
    payload = _safe_json(CREATIVE_FRONTIER_DIR / "narrative_intelligence.json", {})
    arcs = payload.get("arcs", []) if isinstance(payload, dict) else []
    coherent = [item for item in arcs if isinstance(item, dict) and bool(item.get("coherent", False))]
    branching = [item for item in arcs if isinstance(item, dict) and bool(item.get("branching", False))]
    return _overview("NARRATIVE INTELLIGENCE FRAMEWORK - PHASE 682", "narrative-intelligence overview", [f"Narrative arcs: {len(arcs)}", f"Coherent arcs: {len(coherent)}", f"Branching arcs: {len(branching)}"], "Guardrail: narrative systems should preserve coherence, authorship goals, and context rather than blindly maximizing novelty.")


def dynamic_storytelling_engine() -> str:
    payload = _safe_json(CREATIVE_FRONTIER_DIR / "dynamic_storytelling.json", {})
    scenes = payload.get("scenes", []) if isinstance(payload, dict) else []
    adaptive = [item for item in scenes if isinstance(item, dict) and bool(item.get("adaptive", False))]
    resolved = [item for item in scenes if isinstance(item, dict) and item.get("status") == "resolved"]
    return _overview("DYNAMIC STORYTELLING ENGINE - PHASE 683", "dynamic-storytelling overview", [f"Scenes tracked: {len(scenes)}", f"Adaptive scenes: {len(adaptive)}", f"Resolved scenes: {len(resolved)}"], "Guardrail: dynamic storytelling should remain coherent, audience-aware, and creator-controlled before adaptation.")


def procedural_world_generation() -> str:
    payload = _safe_json(CREATIVE_FRONTIER_DIR / "world_generation.json", {})
    worlds = payload.get("worlds", []) if isinstance(payload, dict) else []
    stable = [item for item in worlds if isinstance(item, dict) and bool(item.get("stable", False))]
    seeded = [item for item in worlds if isinstance(item, dict) and bool(item.get("seeded", False))]
    return _overview("PROCEDURAL WORLD GENERATION - PHASE 684", "world-generation overview", [f"Worlds tracked: {len(worlds)}", f"Stable worlds: {len(stable)}", f"Seeded worlds: {len(seeded)}"], "Guardrail: world generation should preserve reproducibility, safety boundaries, and creator control before publication.")


def ai_cinematic_director() -> str:
    payload = _safe_json(CREATIVE_FRONTIER_DIR / "cinematic_director.json", {})
    shots = payload.get("shots", []) if isinstance(payload, dict) else []
    composed = [item for item in shots if isinstance(item, dict) and bool(item.get("composed", False))]
    reviewed = [item for item in shots if isinstance(item, dict) and bool(item.get("reviewed", False))]
    return _overview("AI CINEMATIC DIRECTOR - PHASE 685", "cinematic-direction overview", [f"Shots tracked: {len(shots)}", f"Composed shots: {len(composed)}", f"Reviewed shots: {len(reviewed)}"], "Guardrail: cinematic direction should remain collaborator-friendly, source-aware, and creator-approved before release.")


def real_time_character_dialogue_ai() -> str:
    payload = _safe_json(CREATIVE_FRONTIER_DIR / "character_dialogue.json", {})
    dialogues = payload.get("dialogues", []) if isinstance(payload, dict) else []
    live = [item for item in dialogues if isinstance(item, dict) and item.get("status") == "live"]
    constrained = [item for item in dialogues if isinstance(item, dict) and bool(item.get("constrained", False))]
    return _overview("REAL-TIME CHARACTER DIALOGUE AI - PHASE 686", "character-dialogue overview", [f"Dialogues tracked: {len(dialogues)}", f"Live dialogues: {len(live)}", f"Constrained dialogues: {len(constrained)}"], "Guardrail: live dialogue generation should preserve role consistency, safety constraints, and player-facing clarity before deployment.")


def interactive_simulation_universe() -> str:
    payload = _safe_json(CREATIVE_FRONTIER_DIR / "simulation_universe.json", {})
    systems = payload.get("systems", []) if isinstance(payload, dict) else []
    active = [item for item in systems if isinstance(item, dict) and item.get("status") == "active"]
    synchronized = [item for item in systems if isinstance(item, dict) and bool(item.get("synchronized", False))]
    return _overview("INTERACTIVE SIMULATION UNIVERSE - PHASE 687", "simulation-universe overview", [f"Systems tracked: {len(systems)}", f"Active systems: {len(active)}", f"Synchronized systems: {len(synchronized)}"], "Guardrail: interactive universes should preserve simulation integrity and participant safety before scaling complexity.")


def persistent_virtual_ecosystems() -> str:
    payload = _safe_json(CREATIVE_FRONTIER_DIR / "virtual_ecosystems.json", {})
    ecosystems = payload.get("ecosystems", []) if isinstance(payload, dict) else []
    persistent = [item for item in ecosystems if isinstance(item, dict) and bool(item.get("persistent", False))]
    unstable = [item for item in ecosystems if isinstance(item, dict) and item.get("status") == "unstable"]
    return _overview("PERSISTENT VIRTUAL ECOSYSTEMS - PHASE 688", "virtual-ecosystems overview", [f"Ecosystems tracked: {len(ecosystems)}", f"Persistent ecosystems: {len(persistent)}", f"Unstable ecosystems: {len(unstable)}"], "Guardrail: persistent ecosystems should maintain continuity, observability, and recovery paths rather than opaque drift.")


def ai_social_behavior_simulator() -> str:
    payload = _safe_json(CREATIVE_FRONTIER_DIR / "social_behavior.json", {})
    societies = payload.get("societies", []) if isinstance(payload, dict) else []
    emergent = [item for item in societies if isinstance(item, dict) and bool(item.get("emergent", False))]
    monitored = [item for item in societies if isinstance(item, dict) and bool(item.get("monitored", False))]
    return _overview("AI SOCIAL BEHAVIOR SIMULATOR - PHASE 689", "social-behavior overview", [f"Societies tracked: {len(societies)}", f"Emergent societies: {len(emergent)}", f"Monitored societies: {len(monitored)}"], "Guardrail: social simulation should remain ethically framed, observable, and non-deceptive before interpretation.")


def human_psychology_modeling() -> str:
    payload = _safe_json(CREATIVE_FRONTIER_DIR / "psychology_modeling.json", {})
    profiles = payload.get("profiles", []) if isinstance(payload, dict) else []
    reviewed = [item for item in profiles if isinstance(item, dict) and bool(item.get("reviewed", False))]
    sensitive = [item for item in profiles if isinstance(item, dict) and bool(item.get("sensitive", False))]
    return _overview("HUMAN PSYCHOLOGY MODELING - PHASE 690", "psychology-modeling overview", [f"Profiles tracked: {len(profiles)}", f"Reviewed profiles: {len(reviewed)}", f"Sensitive profiles: {len(sensitive)}"], "Guardrail: psychology modeling should remain consent-aware, non-manipulative, and tightly governed before use.")
