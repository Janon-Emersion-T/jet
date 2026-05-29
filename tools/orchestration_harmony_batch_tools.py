from __future__ import annotations

import json
from pathlib import Path


ORCHESTRATION_HARMONY_BATCH_DIR = Path("storage/orchestration_harmony_batch")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(ORCHESTRATION_HARMONY_BATCH_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def adaptive_intelligence_orchestration_engine() -> str:
    return _render("ADAPTIVE INTELLIGENCE ORCHESTRATION ENGINE - PHASE 1451", "intelligence-orchestration overview", "intelligence_orchestration.json", "orchestration_paths", "adaptive", "stalled", "Orchestration paths tracked", "Adaptive paths", "Stalled paths", "Guardrail: intelligence orchestration should preserve observability, bounded autonomy, and rollback paths before adaptation.")


def autonomous_cosmic_harmony_framework() -> str:
    return _render("AUTONOMOUS COSMIC HARMONY FRAMEWORK - PHASE 1452", "cosmic-harmony overview", "cosmic_harmony.json", "harmony_frameworks", "harmonized", "suppressed", "Harmony frameworks tracked", "Harmonized frameworks", "Suppressed frameworks", "Guardrail: cosmic harmony should preserve plural values, dissent visibility, and non-coercive alignment before synthesis.")


def infinite_scale_ethical_synthesis_ai() -> str:
    return _render("INFINITE-SCALE ETHICAL SYNTHESIS AI - PHASE 1453", "ethical-synthesis overview", "ethical_synthesis_ai.json", "ethical_syntheses", "coherent", "contradictory", "Ethical syntheses tracked", "Coherent syntheses", "Contradictory syntheses", "Guardrail: ethical synthesis should preserve contestability, rights floors, and explicit uncertainty where norms conflict.")


def recursive_destiny_stewardship_engine() -> str:
    return _render("RECURSIVE DESTINY STEWARDSHIP ENGINE - PHASE 1454", "destiny-stewardship overview", "destiny_stewardship_engine.json", "stewardship_loops", "stewarded", "captured", "Stewardship loops tracked", "Stewarded loops", "Captured loops", "Guardrail: destiny stewardship should preserve revisability, public agency, and anti-paternalistic framing before guidance.")


def universal_prosperity_continuity_framework() -> str:
    return _render("UNIVERSAL PROSPERITY CONTINUITY FRAMEWORK - PHASE 1455", "prosperity-continuity overview", "prosperity_continuity.json", "continuity_paths", "continuous", "extractive", "Continuity paths tracked", "Continuous paths", "Extractive paths", "Guardrail: prosperity continuity should preserve equity, ecological realism, and transparent maintenance assumptions.")


def adaptive_coexistence_harmonization_ai() -> str:
    return _render("ADAPTIVE COEXISTENCE HARMONIZATION AI - PHASE 1456", "coexistence-harmonization overview", "coexistence_harmonization.json", "coexistence_meshes", "harmonized", "polarized", "Coexistence meshes tracked", "Harmonized meshes", "Polarized meshes", "Guardrail: coexistence harmonization should preserve rights, plural norms, and transparent conflict mediation before convergence.")


def autonomous_flourishing_orchestration_engine() -> str:
    return _render("AUTONOMOUS FLOURISHING ORCHESTRATION ENGINE - PHASE 1457", "flourishing-orchestration overview", "flourishing_orchestration_engine.json", "flourishing_routes", "orchestrated", "excluded", "Flourishing routes tracked", "Orchestrated routes", "Excluded routes", "Guardrail: flourishing orchestration should preserve dignity, inclusion, and visible tradeoffs before optimization.")


def infinite_scale_planetary_continuity_framework() -> str:
    return _render("INFINITE-SCALE PLANETARY CONTINUITY FRAMEWORK - PHASE 1458", "planetary-continuity overview", "planetary_continuity_framework.json", "continuity_models", "continuous", "brittle", "Continuity models tracked", "Continuous models", "Brittle models", "Guardrail: planetary continuity should preserve resilience, democratic legitimacy, and fallback capacity before coordination.")


def recursive_collaborative_wisdom_ai() -> str:
    return _render("RECURSIVE COLLABORATIVE WISDOM AI - PHASE 1459", "collaborative-wisdom overview", "collaborative_wisdom.json", "wisdom_clusters", "wise", "overconfident", "Wisdom clusters tracked", "Wise clusters", "Overconfident clusters", "Guardrail: collaborative wisdom should preserve source traceability, humility, and shared interpretive accountability.")


def universal_stewardship_synthesis_engine() -> str:
    return _render("UNIVERSAL STEWARDSHIP SYNTHESIS ENGINE - PHASE 1460", "stewardship-synthesis overview", "stewardship_synthesis_engine.json", "stewardship_syntheses", "coherent", "captured", "Stewardship syntheses tracked", "Coherent syntheses", "Captured syntheses", "Guardrail: stewardship synthesis should preserve accountability chains, local agency, and anti-capture review before alignment.")
