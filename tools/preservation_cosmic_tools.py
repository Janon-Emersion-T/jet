from __future__ import annotations

import json
from pathlib import Path


PRESERVATION_COSMIC_DIR = Path("storage/preservation_cosmic")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, pos: str, risk: str, key_label: str, pos_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(PRESERVATION_COSMIC_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(pos, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{pos_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_adaptive_optimization_framework() -> str:
    return _render("UNIVERSAL ADAPTIVE OPTIMIZATION FRAMEWORK - PHASE 1161", "adaptive-optimization overview", "adaptive_optimization.json", "loops", "optimized", "oscillating", "Loops tracked", "Optimized loops", "Oscillating loops", "Guardrail: adaptive optimization should preserve stability, explicit objectives, and rollback before deployment.")


def adaptive_entropy_stabilization_substrate() -> str:
    return _render("ADAPTIVE ENTROPY STABILIZATION SUBSTRATE - PHASE 1162", "entropy-stabilization overview", "entropy_stabilization.json", "substrates", "stabilized", "chaotic", "Substrates tracked", "Stabilized substrates", "Chaotic substrates", "Guardrail: entropy stabilization should preserve system boundaries, observability, and cautious intervention before tuning.")


def autonomous_resilience_amplification_ai() -> str:
    return _render("AUTONOMOUS RESILIENCE AMPLIFICATION AI - PHASE 1163", "resilience-amplification overview", "resilience_amplification.json", "networks", "amplified", "weakened", "Networks tracked", "Amplified networks", "Weakened networks", "Guardrail: resilience amplification should preserve redundancy, equity, and human supervision before scaling.")


def infinite_scale_continuity_planning_engine() -> str:
    return _render("INFINITE-SCALE CONTINUITY PLANNING ENGINE - PHASE 1164", "continuity-planning overview", "continuity_planning.json", "continuities", "planned", "gapped", "Continuities tracked", "Planned continuities", "Gapped continuities", "Guardrail: continuity planning should preserve lawful priorities, public communication, and fallback capacity before activation.")


def recursive_survival_strategy_framework() -> str:
    return _render("RECURSIVE SURVIVAL STRATEGY FRAMEWORK - PHASE 1165", "survival-strategy overview", "survival_strategy.json", "strategies", "viable", "fragile", "Strategies tracked", "Viable strategies", "Fragile strategies", "Guardrail: survival strategy work should preserve ethics, dignity, and anti-panic safeguards before recommendation.")


def universal_existential_preservation_network() -> str:
    return _render("UNIVERSAL EXISTENTIAL PRESERVATION NETWORK - PHASE 1166", "existential-preservation overview", "existential_preservation.json", "preservations", "protected", "at_risk", "Preservations tracked", "Protected preservations", "At-risk preservations", "Guardrail: existential preservation should preserve plural values, accountability, and transparent tradeoffs before coordination.")


def adaptive_species_continuity_ai() -> str:
    return _render("ADAPTIVE SPECIES CONTINUITY AI - PHASE 1167", "species-continuity overview", "species_continuity.json", "species", "supported", "declining", "Species tracked", "Supported species", "Declining species", "Guardrail: species continuity planning should preserve biodiversity, local stewardship, and non-invasive methods before intervention.")


def autonomous_interplanetary_migration_planner() -> str:
    return _render("AUTONOMOUS INTERPLANETARY MIGRATION PLANNER - PHASE 1168", "interplanetary-migration overview", "interplanetary_migration.json", "routes", "planned", "stranded", "Routes tracked", "Planned routes", "Stranded routes", "Guardrail: interplanetary migration planning should preserve consent, safety, and accountable governance before action.")


def infinite_scale_habitat_adaptation_engine() -> str:
    return _render("INFINITE-SCALE HABITAT ADAPTATION ENGINE - PHASE 1169", "habitat-adaptation overview", "habitat_adaptation.json", "habitats", "adapted", "unstable", "Habitats tracked", "Adapted habitats", "Unstable habitats", "Guardrail: habitat adaptation should preserve life-support safety, ecological limits, and human override before deployment.")


def recursive_terraforming_cognition_framework() -> str:
    return _render("RECURSIVE TERRAFORMING COGNITION FRAMEWORK - PHASE 1170", "terraforming-cognition overview", "terraforming_cognition.json", "transforms", "modeled", "irreversible", "Transforms tracked", "Modeled transforms", "Irreversible transforms", "Guardrail: terraforming cognition should preserve planetary protection, humility, and stringent review before recommendation.")
