from __future__ import annotations

import json
from pathlib import Path


SYNCHRONIZATION_GOVERNANCE_DIR = Path("storage/synchronization_governance")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, pos: str, risk: str, key_label: str, pos_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(SYNCHRONIZATION_GOVERNANCE_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(pos, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{pos_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_intelligence_synchronization_framework() -> str:
    return _render("UNIVERSAL INTELLIGENCE SYNCHRONIZATION FRAMEWORK - PHASE 1321", "intelligence-synchronization overview", "intelligence_synchronization.json", "intelligence_meshes", "synchronized", "divergent", "Intelligence meshes tracked", "Synchronized meshes", "Divergent meshes", "Guardrail: intelligence synchronization should preserve autonomy, privacy, and disagreement visibility before alignment.")


def adaptive_omnidisciplinary_cognition_engine() -> str:
    return _render("ADAPTIVE OMNIDISCIPLINARY COGNITION ENGINE - PHASE 1322", "omnidisciplinary-cognition overview", "omnidisciplinary_cognition.json", "cognition_spans", "integrated", "shallow", "Cognition spans tracked", "Integrated spans", "Shallow spans", "Guardrail: omnidisciplinary cognition should preserve rigor, provenance, and challenge paths before synthesis.")


def autonomous_universal_systems_synthesis_ai() -> str:
    return _render("AUTONOMOUS UNIVERSAL SYSTEMS SYNTHESIS AI - PHASE 1323", "systems-synthesis overview", "universal_systems_synthesis.json", "system_models", "synthesized", "entangled", "System models tracked", "Synthesized models", "Entangled models", "Guardrail: systems synthesis should preserve interpretability, modularity, and reviewability before orchestration.")


def infinite_scale_adaptive_orchestration_substrate() -> str:
    return _render("INFINITE-SCALE ADAPTIVE ORCHESTRATION SUBSTRATE - PHASE 1324", "adaptive-orchestration overview", "adaptive_orchestration.json", "orchestration_meshes", "adaptive", "overloaded", "Orchestration meshes tracked", "Adaptive meshes", "Overloaded meshes", "Guardrail: adaptive orchestration should preserve visibility, fail-safes, and human override before deployment.")


def recursive_galactic_resilience_framework() -> str:
    return _render("RECURSIVE GALACTIC RESILIENCE FRAMEWORK - PHASE 1325", "galactic-resilience overview", "galactic_resilience.json", "resilience_grids", "resilient", "brittle", "Resilience grids tracked", "Resilient grids", "Brittle grids", "Guardrail: galactic resilience planning should preserve redundancy, fairness, and anti-fragility review before optimization.")


def universal_exploratory_cognition_ai() -> str:
    return _render("UNIVERSAL EXPLORATORY COGNITION AI - PHASE 1326", "exploratory-cognition overview", "exploratory_cognition.json", "exploration_models", "curious", "stagnant", "Exploration models tracked", "Curious models", "Stagnant models", "Guardrail: exploratory cognition should preserve safety, openness, and user agency before amplification.")


def adaptive_existential_harmonization_engine() -> str:
    return _render("ADAPTIVE EXISTENTIAL HARMONIZATION ENGINE - PHASE 1327", "existential-harmonization overview", "existential_harmonization.json", "existential_paths", "harmonized", "fractured", "Existential paths tracked", "Harmonized paths", "Fractured paths", "Guardrail: existential harmonization should preserve autonomy, plurality, and psychological safety before guidance.")


def autonomous_continuity_civilization_framework() -> str:
    return _render("AUTONOMOUS CONTINUITY CIVILIZATION FRAMEWORK - PHASE 1328", "continuity-civilization overview", "continuity_civilization.json", "civilization_continuities", "continuous", "broken", "Civilization continuities tracked", "Continuous continuities", "Broken continuities", "Guardrail: continuity civilization planning should preserve memory, legitimacy, and accountable stewardship before intervention.")


def infinite_scale_cooperative_destiny_ai() -> str:
    return _render("INFINITE-SCALE COOPERATIVE DESTINY AI - PHASE 1329", "cooperative-destiny overview", "cooperative_destiny.json", "destiny_meshes", "cooperative", "coercive", "Destiny meshes tracked", "Cooperative meshes", "Coercive meshes", "Guardrail: cooperative destiny systems should preserve consent, anti-domination safeguards, and plural future rights before coordination.")


def recursive_universal_governance_substrate() -> str:
    return _render("RECURSIVE UNIVERSAL GOVERNANCE SUBSTRATE - PHASE 1330", "universal-governance overview", "universal_governance.json", "governance_layers", "governed", "captured", "Governance layers tracked", "Governed layers", "Captured layers", "Guardrail: universal governance should preserve subsidiarity, accountability, and appeals before delegation.")
