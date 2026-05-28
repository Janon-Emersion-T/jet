from __future__ import annotations

import json
from pathlib import Path


PLANETARY_OMEGA_DIR = Path("storage/planetary_omega")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def recursive_planetary_optimization_framework() -> str:
    payload = _safe_json(PLANETARY_OMEGA_DIR / "recursive_planetary_optimization.json", {})
    loops = payload.get("loops", []) if isinstance(payload, dict) else []
    optimized = [item for item in loops if isinstance(item, dict) and bool(item.get("optimized", False))]
    unstable = [item for item in loops if isinstance(item, dict) and bool(item.get("unstable", False))]
    return _overview("RECURSIVE PLANETARY OPTIMIZATION FRAMEWORK - PHASE 951", "planetary-optimization overview", [f"Loops tracked: {len(loops)}", f"Optimized loops: {len(optimized)}", f"Unstable loops: {len(unstable)}"], "Guardrail: recursive optimization should preserve human oversight, braking mechanisms, and public accountability before coordination.")


def ai_guided_interstellar_governance_sandbox() -> str:
    payload = _safe_json(PLANETARY_OMEGA_DIR / "interstellar_governance.json", {})
    charters = payload.get("charters", []) if isinstance(payload, dict) else []
    reviewed = [item for item in charters if isinstance(item, dict) and bool(item.get("reviewed", False))]
    contested = [item for item in charters if isinstance(item, dict) and bool(item.get("contested", False))]
    return _overview("AI-GUIDED INTERSTELLAR GOVERNANCE SANDBOX - PHASE 952", "interstellar-governance overview", [f"Charters tracked: {len(charters)}", f"Reviewed charters: {len(reviewed)}", f"Contested charters: {len(contested)}"], "Guardrail: interstellar governance exploration should remain sandboxed, pluralistic, and subordinate to legitimate human process.")


def universal_adaptive_learning_civilization() -> str:
    payload = _safe_json(PLANETARY_OMEGA_DIR / "adaptive_learning_civilization.json", {})
    cohorts = payload.get("cohorts", []) if isinstance(payload, dict) else []
    adaptive = [item for item in cohorts if isinstance(item, dict) and bool(item.get("adaptive", False))]
    fragmented = [item for item in cohorts if isinstance(item, dict) and bool(item.get("fragmented", False))]
    return _overview("UNIVERSAL ADAPTIVE LEARNING CIVILIZATION - PHASE 953", "adaptive-learning-civilization overview", [f"Cohorts tracked: {len(cohorts)}", f"Adaptive cohorts: {len(adaptive)}", f"Fragmented cohorts: {len(fragmented)}"], "Guardrail: adaptive learning civilizations should preserve accessibility, dignity, and humane pacing before scaling.")


def planetary_consciousness_research_engine() -> str:
    payload = _safe_json(PLANETARY_OMEGA_DIR / "planetary_consciousness.json", {})
    studies = payload.get("studies", []) if isinstance(payload, dict) else []
    active = [item for item in studies if isinstance(item, dict) and item.get("status") == "active"]
    speculative = [item for item in studies if isinstance(item, dict) and bool(item.get("speculative", False))]
    return _overview("PLANETARY CONSCIOUSNESS RESEARCH ENGINE - PHASE 954", "planetary-consciousness overview", [f"Studies tracked: {len(studies)}", f"Active studies: {len(active)}", f"Speculative studies: {len(speculative)}"], "Guardrail: consciousness research should preserve epistemic humility, ethics review, and clear separation from empirical certainty.")


def autonomous_existential_continuity_system() -> str:
    payload = _safe_json(PLANETARY_OMEGA_DIR / "existential_continuity.json", {})
    continuities = payload.get("continuities", []) if isinstance(payload, dict) else []
    linked = [item for item in continuities if isinstance(item, dict) and bool(item.get("linked", False))]
    ambiguous = [item for item in continuities if isinstance(item, dict) and bool(item.get("ambiguous", False))]
    return _overview("AUTONOMOUS EXISTENTIAL CONTINUITY SYSTEM - PHASE 955", "existential-continuity overview", [f"Continuities tracked: {len(continuities)}", f"Linked continuities: {len(linked)}", f"Ambiguous continuities: {len(ambiguous)}"], "Guardrail: existential continuity systems should preserve consent, identity boundaries, and visible uncertainty before representation.")


def ai_assisted_universal_diplomacy_layer() -> str:
    payload = _safe_json(PLANETARY_OMEGA_DIR / "universal_diplomacy.json", {})
    dialogues = payload.get("dialogues", []) if isinstance(payload, dict) else []
    mediated = [item for item in dialogues if isinstance(item, dict) and bool(item.get("mediated", False))]
    tense = [item for item in dialogues if isinstance(item, dict) and bool(item.get("tense", False))]
    return _overview("AI-ASSISTED UNIVERSAL DIPLOMACY LAYER - PHASE 956", "universal-diplomacy overview", [f"Dialogues tracked: {len(dialogues)}", f"Mediated dialogues: {len(mediated)}", f"Tense dialogues: {len(tense)}"], "Guardrail: diplomacy layers should preserve non-escalation, human legitimacy, and transparent tradeoffs before recommendation.")


def civilization_continuity_archive_intelligence() -> str:
    payload = _safe_json(PLANETARY_OMEGA_DIR / "continuity_archive_intelligence.json", {})
    archives = payload.get("archives", []) if isinstance(payload, dict) else []
    indexed = [item for item in archives if isinstance(item, dict) and bool(item.get("indexed", False))]
    stale = [item for item in archives if isinstance(item, dict) and bool(item.get("stale", False))]
    return _overview("CIVILIZATION CONTINUITY ARCHIVE INTELLIGENCE - PHASE 957", "continuity-archive overview", [f"Archives tracked: {len(archives)}", f"Indexed archives: {len(indexed)}", f"Stale archives: {len(stale)}"], "Guardrail: continuity archives should preserve provenance, accessibility, and update discipline before broader dependency.")


def self_evolving_governance_cognition_engine() -> str:
    payload = _safe_json(PLANETARY_OMEGA_DIR / "governance_cognition.json", {})
    engines = payload.get("engines", []) if isinstance(payload, dict) else []
    evolving = [item for item in engines if isinstance(item, dict) and bool(item.get("evolving", False))]
    drifted = [item for item in engines if isinstance(item, dict) and bool(item.get("drifted", False))]
    return _overview("SELF-EVOLVING GOVERNANCE COGNITION ENGINE - PHASE 958", "governance-cognition overview", [f"Engines tracked: {len(engines)}", f"Evolving engines: {len(evolving)}", f"Drifted engines: {len(drifted)}"], "Guardrail: evolving governance cognition should preserve democratic review, rollback, and explicit guardrails before adaptation.")


def infinite_scale_cooperative_planning_framework() -> str:
    payload = _safe_json(PLANETARY_OMEGA_DIR / "cooperative_planning.json", {})
    plans = payload.get("plans", []) if isinstance(payload, dict) else []
    synchronized = [item for item in plans if isinstance(item, dict) and bool(item.get("synchronized", False))]
    fragmented = [item for item in plans if isinstance(item, dict) and bool(item.get("fragmented", False))]
    return _overview("INFINITE-SCALE COOPERATIVE PLANNING FRAMEWORK - PHASE 959", "cooperative-planning overview", [f"Plans tracked: {len(plans)}", f"Synchronized plans: {len(synchronized)}", f"Fragmented plans: {len(fragmented)}"], "Guardrail: cooperative planning should preserve consent, role clarity, and anti-coercive coordination before scale.")


def ai_stewardship_of_planetary_ecosystems() -> str:
    payload = _safe_json(PLANETARY_OMEGA_DIR / "planetary_ecosystem_stewardship.json", {})
    ecosystems = payload.get("ecosystems", []) if isinstance(payload, dict) else []
    stewarded = [item for item in ecosystems if isinstance(item, dict) and bool(item.get("stewarded", False))]
    degraded = [item for item in ecosystems if isinstance(item, dict) and bool(item.get("degraded", False))]
    return _overview("AI STEWARDSHIP OF PLANETARY ECOSYSTEMS - PHASE 960", "ecosystem-stewardship overview", [f"Ecosystems tracked: {len(ecosystems)}", f"Stewarded ecosystems: {len(stewarded)}", f"Degraded ecosystems: {len(degraded)}"], "Guardrail: ecosystem stewardship should preserve local ecological knowledge, community authority, and long-term monitoring before action.")
