from __future__ import annotations

import json
from pathlib import Path


COLLECTIVE_COEXISTENCE_DIR = Path("storage/collective_coexistence")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, pos: str, risk: str, key_label: str, pos_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(COLLECTIVE_COEXISTENCE_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(pos, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{pos_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_collaborative_flourishing_engine() -> str:
    return _render("UNIVERSAL COLLABORATIVE FLOURISHING ENGINE - PHASE 1331", "collaborative-flourishing overview", "collaborative_flourishing.json", "flourishing_meshes", "flourishing", "uneven", "Flourishing meshes tracked", "Flourishing meshes", "Uneven meshes", "Guardrail: collaborative flourishing should preserve equity, shared agency, and non-coercive support before optimization.")


def adaptive_planetary_enlightenment_ai() -> str:
    return _render("ADAPTIVE PLANETARY ENLIGHTENMENT AI - PHASE 1332", "planetary-enlightenment overview", "adaptive_planetary_enlightenment.json", "enlightenment_loops", "illuminated", "dogmatic", "Enlightenment loops tracked", "Illuminated loops", "Dogmatic loops", "Guardrail: planetary enlightenment should preserve plural wisdom and anti-dogmatic safeguards before guidance.")


def autonomous_infinite_context_coordination_framework() -> str:
    return _render("AUTONOMOUS INFINITE-CONTEXT COORDINATION FRAMEWORK - PHASE 1333", "infinite-context-coordination overview", "infinite_context_coordination.json", "coordination_contexts", "coordinated", "overwhelmed", "Coordination contexts tracked", "Coordinated contexts", "Overwhelmed contexts", "Guardrail: infinite-context coordination should preserve legibility, bounded execution, and accountable escalation before orchestration.")


def infinite_scale_prosperity_harmonizer() -> str:
    return _render("INFINITE-SCALE PROSPERITY HARMONIZER - PHASE 1334", "prosperity-harmonization overview", "prosperity_harmonization.json", "prosperity_networks", "harmonized", "skewed", "Prosperity networks tracked", "Harmonized networks", "Skewed networks", "Guardrail: prosperity harmonization should preserve justice, local autonomy, and measurable accountability before optimization.")


def recursive_collective_wisdom_ai() -> str:
    return _render("RECURSIVE COLLECTIVE WISDOM AI - PHASE 1335", "collective-wisdom overview", "collective_wisdom.json", "wisdom_collectives", "wise", "misled", "Wisdom collectives tracked", "Wise collectives", "Misled collectives", "Guardrail: collective wisdom systems should preserve dissent, provenance, and challenge rights before recommendation.")


def universal_continuity_intelligence_substrate() -> str:
    return _render("UNIVERSAL CONTINUITY INTELLIGENCE SUBSTRATE - PHASE 1336", "continuity-intelligence overview", "continuity_intelligence.json", "continuity_networks", "intelligent", "drifting", "Continuity networks tracked", "Intelligent networks", "Drifting networks", "Guardrail: continuity intelligence should preserve auditability, local context, and explicit uncertainty before action.")


def adaptive_planetary_empathy_framework() -> str:
    return _render("ADAPTIVE PLANETARY EMPATHY FRAMEWORK - PHASE 1337", "planetary-empathy overview", "planetary_empathy.json", "empathy_paths", "empathetic", "manipulative", "Empathy paths tracked", "Empathetic paths", "Manipulative paths", "Guardrail: empathy frameworks should preserve boundaries, authenticity, and non-coercion before recommendation.")


def autonomous_interstellar_flourishing_ai() -> str:
    return _render("AUTONOMOUS INTERSTELLAR FLOURISHING AI - PHASE 1338", "interstellar-flourishing overview", "interstellar_flourishing.json", "flourishing_systems", "thriving", "deprived", "Flourishing systems tracked", "Thriving systems", "Deprived systems", "Guardrail: interstellar flourishing systems should preserve equity, sovereignty, and long-horizon stewardship before optimization.")


def infinite_scale_coexistence_engine() -> str:
    return _render("INFINITE-SCALE COEXISTENCE ENGINE - PHASE 1339", "coexistence-engine overview", "coexistence_engine.json", "coexistence_networks", "stable", "fractured", "Coexistence networks tracked", "Stable networks", "Fractured networks", "Guardrail: coexistence engines should preserve pluralism, negotiated boundaries, and anti-domination safeguards before alignment.")


def recursive_civilization_symbiosis_framework() -> str:
    return _render("RECURSIVE CIVILIZATION SYMBIOSIS FRAMEWORK - PHASE 1340", "civilization-symbiosis overview", "civilization_symbiosis.json", "symbiosis_paths", "symbiotic", "parasitic", "Symbiosis paths tracked", "Symbiotic paths", "Parasitic paths", "Guardrail: civilization symbiosis should preserve reciprocity, fairness, and transparent tradeoffs before optimization.")
