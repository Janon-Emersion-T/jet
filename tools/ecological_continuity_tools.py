from __future__ import annotations

import json
from pathlib import Path


ECOLOGICAL_CONTINUITY_DIR = Path("storage/ecological_continuity")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def autonomous_multi_species_cooperation_engine() -> str:
    payload = _safe_json(ECOLOGICAL_CONTINUITY_DIR / "multi_species_cooperation.json", {})
    coalitions = payload.get("coalitions", []) if isinstance(payload, dict) else []
    aligned = [item for item in coalitions if isinstance(item, dict) and bool(item.get("aligned", False))]
    strained = [item for item in coalitions if isinstance(item, dict) and bool(item.get("strained", False))]
    return _overview(
        "AUTONOMOUS MULTI-SPECIES COOPERATION ENGINE - PHASE 1021",
        "multi-species-cooperation overview",
        [
            f"Coalitions tracked: {len(coalitions)}",
            f"Aligned coalitions: {len(aligned)}",
            f"Strained coalitions: {len(strained)}",
        ],
        "Guardrail: multi-species cooperation planning should preserve welfare, consent proxies, and ecological humility before intervention.",
    )


def universal_ecological_stewardship_intelligence() -> str:
    payload = _safe_json(ECOLOGICAL_CONTINUITY_DIR / "ecological_stewardship.json", {})
    habitats = payload.get("habitats", []) if isinstance(payload, dict) else []
    stewarded = [item for item in habitats if isinstance(item, dict) and bool(item.get("stewarded", False))]
    degraded = [item for item in habitats if isinstance(item, dict) and bool(item.get("degraded", False))]
    return _overview(
        "UNIVERSAL ECOLOGICAL STEWARDSHIP INTELLIGENCE - PHASE 1022",
        "ecological-stewardship overview",
        [
            f"Habitats tracked: {len(habitats)}",
            f"Stewarded habitats: {len(stewarded)}",
            f"Degraded habitats: {len(degraded)}",
        ],
        "Guardrail: ecological stewardship should preserve biodiversity, local knowledge, and long-horizon regeneration before recommendation.",
    )


def self_healing_civilization_memory_archive() -> str:
    payload = _safe_json(ECOLOGICAL_CONTINUITY_DIR / "civilization_memory_archive.json", {})
    archives = payload.get("archives", []) if isinstance(payload, dict) else []
    healed = [item for item in archives if isinstance(item, dict) and bool(item.get("healed", False))]
    fractured = [item for item in archives if isinstance(item, dict) and bool(item.get("fractured", False))]
    return _overview(
        "SELF-HEALING CIVILIZATION MEMORY ARCHIVE - PHASE 1023",
        "civilization-memory-archive overview",
        [
            f"Archives tracked: {len(archives)}",
            f"Healed archives: {len(healed)}",
            f"Fractured archives: {len(fractured)}",
        ],
        "Guardrail: memory repair should preserve provenance, plural memory, and reversible restoration before archival updates.",
    )


def planetary_semantic_continuity_system() -> str:
    payload = _safe_json(ECOLOGICAL_CONTINUITY_DIR / "semantic_continuity.json", {})
    vocabularies = payload.get("vocabularies", []) if isinstance(payload, dict) else []
    synchronized = [item for item in vocabularies if isinstance(item, dict) and bool(item.get("synchronized", False))]
    drifting = [item for item in vocabularies if isinstance(item, dict) and bool(item.get("drifting", False))]
    return _overview(
        "PLANETARY SEMANTIC CONTINUITY SYSTEM - PHASE 1024",
        "semantic-continuity overview",
        [
            f"Vocabularies tracked: {len(vocabularies)}",
            f"Synchronized vocabularies: {len(synchronized)}",
            f"Drifting vocabularies: {len(drifting)}",
        ],
        "Guardrail: semantic continuity should preserve translation nuance, minority languages, and explicit disagreement before harmonization.",
    )


def recursive_planetary_logistics_optimizer() -> str:
    payload = _safe_json(ECOLOGICAL_CONTINUITY_DIR / "planetary_logistics_optimizer.json", {})
    routes = payload.get("routes", []) if isinstance(payload, dict) else []
    optimized = [item for item in routes if isinstance(item, dict) and bool(item.get("optimized", False))]
    fragile = [item for item in routes if isinstance(item, dict) and bool(item.get("fragile", False))]
    return _overview(
        "RECURSIVE PLANETARY LOGISTICS OPTIMIZER - PHASE 1025",
        "planetary-logistics overview",
        [
            f"Routes tracked: {len(routes)}",
            f"Optimized routes: {len(optimized)}",
            f"Fragile routes: {len(fragile)}",
        ],
        "Guardrail: logistics optimization should preserve resilience, equitable access, and human override before deployment.",
    )
