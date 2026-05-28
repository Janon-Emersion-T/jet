from __future__ import annotations

import json
from pathlib import Path


DISCOVERY_REASONING_DIR = Path("storage/discovery_reasoning")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_key: str, risk_key: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(DISCOVERY_REASONING_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_key, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_key, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_mentorship_cognition_engine() -> str:
    return _render("UNIVERSAL MENTORSHIP COGNITION ENGINE - PHASE 1121", "mentorship-cognition overview", "mentorship_cognition.json", "mentorships", "supported", "orphaned", "Mentorships tracked", "Supported mentorships", "Orphaned mentorships", "Guardrail: mentorship cognition should preserve human agency, boundary clarity, and development consent before guidance.")


def adaptive_lifelong_development_substrate() -> str:
    return _render("ADAPTIVE LIFELONG DEVELOPMENT SUBSTRATE - PHASE 1122", "lifelong-development overview", "lifelong_development.json", "journeys", "adaptive", "fragmented", "Journeys tracked", "Adaptive journeys", "Fragmented journeys", "Guardrail: lifelong development systems should preserve accessibility, autonomy, and reflective pacing before intervention.")


def autonomous_curiosity_amplification_system() -> str:
    return _render("AUTONOMOUS CURIOSITY AMPLIFICATION SYSTEM - PHASE 1123", "curiosity-amplification overview", "curiosity_amplification.json", "explorations", "amplified", "distracted", "Explorations tracked", "Amplified explorations", "Distracted explorations", "Guardrail: curiosity amplification should preserve attention health, user intent, and non-manipulation before personalization.")


def infinite_scale_exploration_intelligence() -> str:
    return _render("INFINITE-SCALE EXPLORATION INTELLIGENCE - PHASE 1124", "exploration-intelligence overview", "exploration_intelligence.json", "missions", "scouted", "blind", "Missions tracked", "Scouted missions", "Blind missions", "Guardrail: exploration intelligence should preserve safety, scientific rigor, and accountable priorities before dispatch.")


def recursive_knowledge_frontier_simulator() -> str:
    return _render("RECURSIVE KNOWLEDGE FRONTIER SIMULATOR - PHASE 1125", "knowledge-frontier overview", "knowledge_frontier.json", "frontiers", "modeled", "uncertain", "Frontiers tracked", "Modeled frontiers", "Uncertain frontiers", "Guardrail: frontier simulation should preserve humility, evidence traceability, and exploratory diversity before ranking.")


def universal_discovery_optimization_engine() -> str:
    return _render("UNIVERSAL DISCOVERY OPTIMIZATION ENGINE - PHASE 1126", "discovery-optimization overview", "discovery_optimization.json", "pipelines", "optimized", "biased", "Pipelines tracked", "Optimized pipelines", "Biased pipelines", "Guardrail: discovery optimization should preserve scientific openness, replication, and anti-bias checks before automation.")


def adaptive_scientific_collaboration_ai() -> str:
    return _render("ADAPTIVE SCIENTIFIC COLLABORATION AI - PHASE 1127", "scientific-collaboration overview", "scientific_collaboration.json", "collaborations", "paired", "blocked", "Collaborations tracked", "Paired collaborations", "Blocked collaborations", "Guardrail: scientific collaboration systems should preserve attribution, inclusion, and transparent matchmaking before recommendation.")


def autonomous_theorem_generation_framework() -> str:
    return _render("AUTONOMOUS THEOREM GENERATION FRAMEWORK - PHASE 1128", "theorem-generation overview", "theorem_generation.json", "theorems", "generated", "unproved", "Theorems tracked", "Generated theorems", "Unproved theorems", "Guardrail: theorem generation should preserve proof verification, formal rigor, and explicit uncertainty before publication.")


def infinite_scale_mathematical_cognition_substrate() -> str:
    return _render("INFINITE-SCALE MATHEMATICAL COGNITION SUBSTRATE - PHASE 1129", "mathematical-cognition overview", "mathematical_cognition.json", "models", "reasoning", "inconsistent", "Models tracked", "Reasoning models", "Inconsistent models", "Guardrail: mathematical cognition should preserve verifiability, abstraction clarity, and challenge paths before integration.")


def recursive_abstraction_synthesis_engine() -> str:
    return _render("RECURSIVE ABSTRACTION SYNTHESIS ENGINE - PHASE 1130", "abstraction-synthesis overview", "abstraction_synthesis.json", "abstractions", "synthesized", "leaky", "Abstractions tracked", "Synthesized abstractions", "Leaky abstractions", "Guardrail: abstraction synthesis should preserve interpretability, grounding, and reviewable assumptions before reuse.")
