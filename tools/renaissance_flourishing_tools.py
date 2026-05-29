from __future__ import annotations

import json
from pathlib import Path


RENAISSANCE_FLOURISHING_DIR = Path("storage/renaissance_flourishing")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, pos: str, risk: str, key_label: str, pos_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(RENAISSANCE_FLOURISHING_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(pos, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{pos_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_planetary_renaissance_framework() -> str:
    return _render("UNIVERSAL PLANETARY RENAISSANCE FRAMEWORK - PHASE 1301", "planetary-renaissance overview", "planetary_renaissance.json", "renaissance_paths", "renewed", "stalled", "Renaissance paths tracked", "Renewed paths", "Stalled paths", "Guardrail: renaissance planning should preserve plural cultures, broad participation, and non-coercive transformation before recommendation.")


def adaptive_innovation_civilization_substrate() -> str:
    return _render("ADAPTIVE INNOVATION CIVILIZATION SUBSTRATE - PHASE 1302", "innovation-civilization overview", "innovation_civilization.json", "innovation_ecologies", "adaptive", "captured", "Innovation ecologies tracked", "Adaptive ecologies", "Captured ecologies", "Guardrail: innovation civilization systems should preserve open inquiry, equity, and anti-monopoly safeguards before optimization.")


def autonomous_universal_prosperity_engine() -> str:
    return _render("AUTONOMOUS UNIVERSAL PROSPERITY ENGINE - PHASE 1303", "universal-prosperity overview", "universal_prosperity.json", "prosperity_streams", "prosperous", "uneven", "Prosperity streams tracked", "Prosperous streams", "Uneven streams", "Guardrail: prosperity engines should preserve justice, sustainability, and local agency before allocation.")


def infinite_scale_cooperative_evolution_ai() -> str:
    return _render("INFINITE-SCALE COOPERATIVE EVOLUTION AI - PHASE 1304", "cooperative-evolution overview", "cooperative_evolution.json", "evolution_paths", "cooperative", "competitive", "Evolution paths tracked", "Cooperative paths", "Competitive paths", "Guardrail: cooperative evolution should preserve autonomy, fairness, and anti-coercive coordination before optimization.")


def recursive_harmony_optimization_framework() -> str:
    return _render("RECURSIVE HARMONY OPTIMIZATION FRAMEWORK - PHASE 1305", "harmony-optimization overview", "harmony_optimization.json", "harmony_loops", "harmonized", "suppressed", "Harmony loops tracked", "Harmonized loops", "Suppressed loops", "Guardrail: harmony optimization should preserve dissent, rights, and anti-suppression safeguards before alignment.")


def universal_coexistence_substrate() -> str:
    return _render("UNIVERSAL COEXISTENCE SUBSTRATE - PHASE 1306", "coexistence overview", "coexistence_substrate.json", "coexistence_paths", "coexisting", "fractured", "Coexistence paths tracked", "Coexisting paths", "Fractured paths", "Guardrail: coexistence systems should preserve plurality, safety, and negotiated boundaries before orchestration.")


def adaptive_peace_amplification_engine() -> str:
    return _render("ADAPTIVE PEACE AMPLIFICATION ENGINE - PHASE 1307", "peace-amplification overview", "peace_amplification.json", "peace_paths", "amplified", "tense", "Peace paths tracked", "Amplified peace", "Tense peace", "Guardrail: peace amplification should preserve legitimacy, non-escalation, and transparent mediation before intervention.")


def autonomous_resilience_civilization_ai() -> str:
    return _render("AUTONOMOUS RESILIENCE CIVILIZATION AI - PHASE 1308", "resilience-civilization overview", "resilience_civilization.json", "civilization_resilience_paths", "resilient", "brittle", "Civilization resilience paths tracked", "Resilient paths", "Brittle paths", "Guardrail: resilience civilization systems should preserve equity, redundancy, and accountable stewardship before optimization.")


def infinite_scale_flourishing_simulator() -> str:
    return _render("INFINITE-SCALE FLOURISHING SIMULATOR - PHASE 1309", "flourishing-simulation overview", "flourishing_simulator.json", "flourishing_scenarios", "simulated", "depriving", "Flourishing scenarios tracked", "Simulated scenarios", "Depriving scenarios", "Guardrail: flourishing simulation should preserve non-reductionism, dignity, and uncertainty disclosure before policy use.")


def recursive_wisdom_harmonization_framework() -> str:
    return _render("RECURSIVE WISDOM HARMONIZATION FRAMEWORK - PHASE 1310", "wisdom-harmonization overview", "wisdom_harmonization.json", "wisdom_streams", "harmonized", "conflicted", "Wisdom streams tracked", "Harmonized streams", "Conflicted streams", "Guardrail: wisdom harmonization should preserve plurality, provenance, and human interpretation before convergence.")
