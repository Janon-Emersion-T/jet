from __future__ import annotations

import json
from pathlib import Path


WELLBEING_EQUITY_DIR = Path("storage/wellbeing_equity")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, pos: str, risk: str, key_label: str, pos_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(WELLBEING_EQUITY_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(pos, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{pos_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_abundance_distribution_substrate() -> str:
    return _render("UNIVERSAL ABUNDANCE DISTRIBUTION SUBSTRATE - PHASE 1231", "abundance-distribution overview", "abundance_distribution.json", "distribution_channels", "abundant", "scarce", "Distribution channels tracked", "Abundant channels", "Scarce channels", "Guardrail: abundance distribution should preserve fairness, dignity, and transparent allocation before deployment.")


def adaptive_anti_scarcity_ai() -> str:
    return _render("ADAPTIVE ANTI-SCARCITY AI - PHASE 1232", "anti-scarcity overview", "anti_scarcity.json", "scarcity_loops", "reduced", "persistent", "Scarcity loops tracked", "Reduced loops", "Persistent loops", "Guardrail: anti-scarcity systems should preserve ecological realism, human agency, and justice before optimization.")


def autonomous_poverty_elimination_framework() -> str:
    return _render("AUTONOMOUS POVERTY ELIMINATION FRAMEWORK - PHASE 1233", "poverty-elimination overview", "poverty_elimination.json", "poverty_programs", "uplifting", "excluded", "Poverty programs tracked", "Uplifting programs", "Excluded populations", "Guardrail: poverty elimination should preserve dignity, local voice, and measurable accountability before intervention.")


def infinite_scale_human_development_engine() -> str:
    return _render("INFINITE-SCALE HUMAN DEVELOPMENT ENGINE - PHASE 1234", "human-development overview", "human_development.json", "development_paths", "advancing", "blocked", "Development paths tracked", "Advancing paths", "Blocked paths", "Guardrail: human development systems should preserve autonomy, plural life paths, and supportive pacing before optimization.")


def recursive_educational_upliftment_ai() -> str:
    return _render("RECURSIVE EDUCATIONAL UPLIFTMENT AI - PHASE 1235", "educational-upliftment overview", "educational_upliftment.json", "upliftment_programs", "uplifting", "lagging", "Upliftment programs tracked", "Uplifting programs", "Lagging programs", "Guardrail: educational upliftment should preserve accessibility, cultural context, and learner dignity before intervention.")


def universal_health_equity_substrate() -> str:
    return _render("UNIVERSAL HEALTH EQUITY SUBSTRATE - PHASE 1236", "health-equity overview", "health_equity.json", "care_networks", "equitable", "disparate", "Care networks tracked", "Equitable networks", "Disparate networks", "Guardrail: health equity systems should preserve patient dignity, fairness, and accountable clinical oversight before optimization.")


def adaptive_nutrition_balancing_framework() -> str:
    return _render("ADAPTIVE NUTRITION BALANCING FRAMEWORK - PHASE 1237", "nutrition-balancing overview", "nutrition_balancing.json", "nutrition_programs", "balanced", "deficient", "Nutrition programs tracked", "Balanced programs", "Deficient programs", "Guardrail: nutrition balancing should preserve cultural food contexts, consent, and public-health review before recommendation.")


def autonomous_wellness_harmonizer() -> str:
    return _render("AUTONOMOUS WELLNESS HARMONIZER - PHASE 1238", "wellness-harmonization overview", "wellness_harmonizer.json", "wellness_plans", "harmonized", "stressful", "Wellness plans tracked", "Harmonized plans", "Stressful plans", "Guardrail: wellness harmonization should preserve autonomy, privacy, and non-coercive guidance before intervention.")


def infinite_scale_happiness_optimization_ai() -> str:
    return _render("INFINITE-SCALE HAPPINESS OPTIMIZATION AI - PHASE 1239", "happiness-optimization overview", "happiness_optimization.json", "happiness_models", "improving", "flattening", "Happiness models tracked", "Improving models", "Flattening models", "Guardrail: happiness optimization should preserve emotional nuance, autonomy, and anti-manipulation safeguards before use.")


def recursive_emotional_resilience_engine() -> str:
    return _render("RECURSIVE EMOTIONAL RESILIENCE ENGINE - PHASE 1240", "emotional-resilience overview", "emotional_resilience.json", "resilience_programs", "stabilizing", "fragile", "Resilience programs tracked", "Stabilizing programs", "Fragile programs", "Guardrail: emotional resilience systems should preserve psychological safety, consent, and supportive framing before intervention.")
