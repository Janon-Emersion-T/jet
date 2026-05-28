from __future__ import annotations

import json
from pathlib import Path


CULTURE_GOVERNANCE_DIR = Path("storage/culture_governance")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_key: str, risk_key: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(CULTURE_GOVERNANCE_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_key, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_key, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_conflict_resolution_cognition_layer() -> str:
    return _render("UNIVERSAL CONFLICT RESOLUTION COGNITION LAYER - PHASE 1038", "conflict-resolution overview", "conflict_resolution.json", "cases", "resolved", "stalled", "Cases tracked", "Resolved cases", "Stalled cases", "Guardrail: conflict-resolution systems should preserve due process, non-coercion, and human review before mediation.")


def adaptive_peace_negotiation_intelligence() -> str:
    return _render("ADAPTIVE PEACE NEGOTIATION INTELLIGENCE - PHASE 1039", "peace-negotiation overview", "peace_negotiation.json", "negotiations", "bridged", "tense", "Negotiations tracked", "Bridged negotiations", "Tense negotiations", "Guardrail: peace negotiation intelligence should preserve non-escalation, legitimacy, and transparent tradeoffs before advice.")


def recursive_educational_civilization_engine() -> str:
    return _render("RECURSIVE EDUCATIONAL CIVILIZATION ENGINE - PHASE 1040", "educational-civilization overview", "educational_civilization.json", "pathways", "adaptive", "excluded", "Pathways tracked", "Adaptive pathways", "Excluded pathways", "Guardrail: educational engines should preserve accessibility, plural pedagogy, and humane pacing before rollout.")


def infinite_context_historical_reasoning_framework() -> str:
    return _render("INFINITE-CONTEXT HISTORICAL REASONING FRAMEWORK - PHASE 1041", "historical-reasoning overview", "historical_reasoning.json", "records", "contextualized", "distorted", "Records tracked", "Contextualized records", "Distorted records", "Guardrail: historical reasoning should preserve provenance, historiographic debate, and explicit limits before conclusions.")


def autonomous_cultural_continuity_system() -> str:
    return _render("AUTONOMOUS CULTURAL CONTINUITY SYSTEM - PHASE 1042", "cultural-continuity overview", "cultural_continuity.json", "traditions", "sustained", "eroding", "Traditions tracked", "Sustained traditions", "Eroding traditions", "Guardrail: cultural continuity should preserve community authority, consent, and living diversity before intervention.")


def planetary_wisdom_preservation_archive() -> str:
    return _render("PLANETARY WISDOM PRESERVATION ARCHIVE - PHASE 1043", "wisdom-preservation overview", "wisdom_preservation.json", "archives", "preserved", "stale", "Archives tracked", "Preserved archives", "Stale archives", "Guardrail: wisdom preservation should preserve provenance, access rights, and plural traditions before standardization.")


def recursive_language_evolution_intelligence() -> str:
    return _render("RECURSIVE LANGUAGE EVOLUTION INTELLIGENCE - PHASE 1044", "language-evolution overview", "language_evolution.json", "languages", "evolving", "drifting", "Languages tracked", "Evolving languages", "Drifting languages", "Guardrail: language-evolution intelligence should preserve minority languages, speaker agency, and interpretive nuance before harmonization.")


def universal_symbolic_reasoning_network() -> str:
    return _render("UNIVERSAL SYMBOLIC REASONING NETWORK - PHASE 1045", "symbolic-reasoning overview", "symbolic_reasoning.json", "graphs", "linked", "ambiguous", "Graphs tracked", "Linked graphs", "Ambiguous graphs", "Guardrail: symbolic reasoning should preserve interpretability, provenance, and challenge paths before decision support.")


def adaptive_societal_equilibrium_engine() -> str:
    return _render("ADAPTIVE SOCIETAL EQUILIBRIUM ENGINE - PHASE 1046", "societal-equilibrium overview", "societal_equilibrium.json", "equilibriums", "stable", "fragile", "Equilibriums tracked", "Stable equilibriums", "Fragile equilibriums", "Guardrail: equilibrium optimization should preserve rights, pluralism, and caution against suppression before adjustment.")


def autonomous_decentralized_governance_mesh() -> str:
    return _render("AUTONOMOUS DECENTRALIZED GOVERNANCE MESH - PHASE 1047", "decentralized-governance overview", "decentralized_governance.json", "nodes", "coordinated", "captured", "Nodes tracked", "Coordinated nodes", "Captured nodes", "Guardrail: decentralized governance should preserve transparency, revocability, and legitimate human authority before delegation.")
