from __future__ import annotations

import json
from pathlib import Path


TALENT_FUTURE_DIR = Path("storage/talent_future")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, pos: str, risk: str, key_label: str, pos_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(TALENT_FUTURE_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(pos, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{pos_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_inspiration_network() -> str:
    return _render("UNIVERSAL INSPIRATION NETWORK - PHASE 1291", "inspiration-network overview", "inspiration_network.json", "inspiration_nodes", "inspired", "blocked", "Inspiration nodes tracked", "Inspired nodes", "Blocked nodes", "Guardrail: inspiration networks should preserve autonomy, attribution, and non-manipulative support before use.")


def adaptive_genius_cultivation_framework() -> str:
    return _render("ADAPTIVE GENIUS CULTIVATION FRAMEWORK - PHASE 1292", "genius-cultivation overview", "genius_cultivation.json", "cultivation_paths", "cultivated", "excluded", "Cultivation paths tracked", "Cultivated paths", "Excluded paths", "Guardrail: genius cultivation should preserve equity, wellbeing, and diverse definitions of excellence before optimization.")


def autonomous_talent_emergence_engine() -> str:
    return _render("AUTONOMOUS TALENT EMERGENCE ENGINE - PHASE 1293", "talent-emergence overview", "talent_emergence.json", "talent_signals", "emerged", "suppressed", "Talent signals tracked", "Emerged talent", "Suppressed talent", "Guardrail: talent emergence should preserve fairness, anti-bias review, and supportive opportunities before ranking.")


def infinite_scale_human_potential_ai() -> str:
    return _render("INFINITE-SCALE HUMAN POTENTIAL AI - PHASE 1294", "human-potential overview", "human_potential.json", "potential_paths", "expanded", "underrealized", "Potential paths tracked", "Expanded paths", "Underrealized paths", "Guardrail: human potential systems should preserve autonomy, dignity, and non-reductive guidance before optimization.")


def recursive_capability_expansion_framework() -> str:
    return _render("RECURSIVE CAPABILITY EXPANSION FRAMEWORK - PHASE 1295", "capability-expansion overview", "capability_expansion.json", "capabilities", "expanded", "misapplied", "Capabilities tracked", "Expanded capabilities", "Misapplied capabilities", "Guardrail: capability expansion should preserve safety, consent, and human goals before acceleration.")


def universal_empowerment_substrate() -> str:
    return _render("UNIVERSAL EMPOWERMENT SUBSTRATE - PHASE 1296", "empowerment overview", "empowerment_substrate.json", "empowerment_paths", "empowered", "disempowered", "Empowerment paths tracked", "Empowered paths", "Disempowered paths", "Guardrail: empowerment systems should preserve agency, inclusion, and accountability before intervention.")


def adaptive_aspiration_harmonizer() -> str:
    return _render("ADAPTIVE ASPIRATION HARMONIZER - PHASE 1297", "aspiration-harmonization overview", "aspiration_harmonization.json", "aspirations", "aligned", "suppressed", "Aspirations tracked", "Aligned aspirations", "Suppressed aspirations", "Guardrail: aspiration harmonization should preserve self-determination, plural life goals, and revision rights before guidance.")


def autonomous_achievement_optimization_engine() -> str:
    return _render("AUTONOMOUS ACHIEVEMENT OPTIMIZATION ENGINE - PHASE 1298", "achievement-optimization overview", "achievement_optimization.json", "achievement_paths", "optimized", "burned_out", "Achievement paths tracked", "Optimized paths", "Burned-out paths", "Guardrail: achievement optimization should preserve wellbeing, ethics, and non-coercive pacing before recommendation.")


def infinite_scale_possibility_simulator() -> str:
    return _render("INFINITE-SCALE POSSIBILITY SIMULATOR - PHASE 1299", "possibility-simulation overview", "possibility_simulation.json", "possibility_branches", "simulated", "collapsed", "Possibility branches tracked", "Simulated branches", "Collapsed branches", "Guardrail: possibility simulation should preserve openness, uncertainty, and human interpretation before narrowing options.")


def recursive_future_civilization_ai() -> str:
    return _render("RECURSIVE FUTURE CIVILIZATION AI - PHASE 1300", "future-civilization overview", "future_civilization.json", "civilization_futures", "modeled", "regressing", "Civilization futures tracked", "Modeled futures", "Regressing futures", "Guardrail: future civilization modeling should preserve plural possibilities, humility, and transparent assumptions before recommendation.")
