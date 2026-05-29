from __future__ import annotations

import json
from pathlib import Path


STEWARDSHIP_PROSPERITY_DIR = Path("storage/stewardship_prosperity")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(STEWARDSHIP_PROSPERITY_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_stewardship_harmonization_ai() -> str:
    return _render("UNIVERSAL STEWARDSHIP HARMONIZATION AI - PHASE 1381", "stewardship-harmonization overview", "universal_stewardship_harmonization.json", "stewardship_meshes", "harmonized", "captured", "Stewardship meshes tracked", "Harmonized meshes", "Captured meshes", "Guardrail: stewardship harmonization should preserve public accountability, stewardship boundaries, and reversible coordination paths.")


def adaptive_resilience_orchestration_engine() -> str:
    return _render("ADAPTIVE RESILIENCE ORCHESTRATION ENGINE - PHASE 1382", "resilience-orchestration overview", "adaptive_resilience_orchestration.json", "resilience_paths", "orchestrated", "overstretched", "Resilience paths tracked", "Orchestrated paths", "Overstretched paths", "Guardrail: resilience orchestration should preserve capacity margins, transparency, and operator intervention rights.")


def autonomous_cosmic_continuity_framework() -> str:
    return _render("AUTONOMOUS COSMIC CONTINUITY FRAMEWORK - PHASE 1383", "cosmic-continuity overview", "cosmic_continuity.json", "continuity_corridors", "continuous", "disrupted", "Continuity corridors tracked", "Continuous corridors", "Disrupted corridors", "Guardrail: cosmic continuity planning should preserve treaty boundaries, resilience assumptions, and uncertainty disclosure.")


def infinite_scale_planetary_synthesis_ai() -> str:
    return _render("INFINITE-SCALE PLANETARY SYNTHESIS AI - PHASE 1384", "planetary-synthesis overview", "planetary_synthesis.json", "planetary_models", "synthesized", "partial", "Planetary models tracked", "Synthesized models", "Partial models", "Guardrail: planetary synthesis should preserve source diversity, traceability, and local context before unified recommendations.")


def recursive_intelligence_flourishing_engine() -> str:
    return _render("RECURSIVE INTELLIGENCE FLOURISHING ENGINE - PHASE 1385", "intelligence-flourishing overview", "intelligence_flourishing.json", "flourishing_loops", "flourishing", "degrading", "Flourishing loops tracked", "Flourishing loops", "Degrading loops", "Guardrail: intelligence flourishing should preserve human benefit, bounded autonomy, and grounded evaluation metrics.")


def universal_coexistence_orchestration_framework() -> str:
    return _render("UNIVERSAL COEXISTENCE ORCHESTRATION FRAMEWORK - PHASE 1386", "coexistence-orchestration overview", "coexistence_orchestration.json", "coexistence_meshes", "orchestrated", "polarized", "Coexistence meshes tracked", "Orchestrated meshes", "Polarized meshes", "Guardrail: coexistence orchestration should preserve rights protection, conflict transparency, and non-coercive mediation.")


def adaptive_abundance_harmonizer_ai() -> str:
    return _render("ADAPTIVE ABUNDANCE HARMONIZER AI - PHASE 1387", "abundance-harmonizer overview", "adaptive_abundance_harmonizer.json", "abundance_paths", "abundant", "scarce", "Abundance paths tracked", "Abundant paths", "Scarce paths", "Guardrail: abundance harmonization should preserve ecological limits, equity, and auditable resource assumptions.")


def autonomous_infinite_wisdom_engine() -> str:
    return _render("AUTONOMOUS INFINITE WISDOM ENGINE - PHASE 1388", "infinite-wisdom overview", "infinite_wisdom.json", "wisdom_paths", "wise", "overconfident", "Wisdom paths tracked", "Wise paths", "Overconfident paths", "Guardrail: wisdom engines should preserve humility, provenance, and uncertainty bounds before strategic use.")


def infinite_scale_destiny_stewardship_framework() -> str:
    return _render("INFINITE-SCALE DESTINY STEWARDSHIP FRAMEWORK - PHASE 1389", "destiny-stewardship overview", "destiny_stewardship.json", "stewardship_futures", "stewarded", "captured", "Stewardship futures tracked", "Stewarded futures", "Captured futures", "Guardrail: destiny stewardship should preserve public agency, revisability, and anti-paternalistic framing.")


def recursive_universal_prosperity_ai() -> str:
    return _render("RECURSIVE UNIVERSAL PROSPERITY AI - PHASE 1390", "universal-prosperity overview", "recursive_universal_prosperity.json", "prosperity_loops", "prosperous", "extractive", "Prosperity loops tracked", "Prosperous loops", "Extractive loops", "Guardrail: prosperity optimization should preserve justice, inclusion, and anti-extraction safeguards before recommendation.")
