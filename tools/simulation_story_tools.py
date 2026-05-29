from __future__ import annotations

import json
from pathlib import Path


SIM_DIR = Path("storage/simulation")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _list_entries(path: Path, key: str):
    payload = _safe_json(path, {key: []})
    if isinstance(payload, dict) and isinstance(payload.get(key), list):
        return payload[key]
    if isinstance(payload, list):
        return payload
    return []


def creative_writing_engine() -> str:
    drafts = _list_entries(SIM_DIR / "writing.json", "drafts")
    genres = sorted(
        {
            str(item.get("genre", "unknown"))
            for item in drafts
            if isinstance(item, dict) and item.get("genre")
        }
    )
    return "\n".join(
        [
            "CREATIVE WRITING ENGINE - PHASE 477",
            "Mode: writing-project overview.",
            f"Drafts tracked: {len(drafts)}",
            f"Genres: {', '.join(genres) if genres else 'none'}",
            "Loop: premise, characters, conflict, scenes, revision passes, and voice consistency.",
        ]
    )


def game_ai_engine() -> str:
    prototypes = _list_entries(SIM_DIR / "game_ai.json", "prototypes")
    agents = sum(int(item.get("agent_count", 0) or 0) for item in prototypes if isinstance(item, dict))
    return "\n".join(
        [
            "GAME AI ENGINE - PHASE 478",
            "Mode: game-AI prototype overview.",
            f"Prototypes tracked: {len(prototypes)}",
            f"Total AI agents described: {agents}",
            "Focus: goal systems, utility scoring, navigation constraints, and player-facing clarity.",
        ]
    )


def npc_personality_framework() -> str:
    profiles = _list_entries(SIM_DIR / "npc_profiles.json", "profiles")
    factions = sorted(
        {
            str(item.get("faction", "independent"))
            for item in profiles
            if isinstance(item, dict) and item.get("faction")
        }
    )
    return "\n".join(
        [
            "NPC PERSONALITY FRAMEWORK - PHASE 479",
            "Mode: personality model overview.",
            f"NPC profiles: {len(profiles)}",
            f"Factions: {', '.join(factions) if factions else 'none'}",
            "Design axis: motives, memory, loyalties, stress responses, and dialogue style.",
        ]
    )


def simulation_environment_builder() -> str:
    scenarios = _list_entries(SIM_DIR / "scenarios.json", "scenarios")
    environments = sorted(
        {
            str(item.get("environment", "unknown"))
            for item in scenarios
            if isinstance(item, dict) and item.get("environment")
        }
    )
    return "\n".join(
        [
            "SIMULATION ENVIRONMENT BUILDER - PHASE 480",
            "Mode: scenario-environment overview.",
            f"Scenarios tracked: {len(scenarios)}",
            f"Environment types: {', '.join(environments) if environments else 'none'}",
            "Recommended ingredients: rules, actors, resources, success criteria, and logging before any autonomy claims grow larger.",
        ]
    )
