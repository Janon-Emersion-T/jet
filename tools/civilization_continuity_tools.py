from __future__ import annotations

import json
from pathlib import Path


CIV_CONT_DIR = Path("storage/civilization_continuity")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def human_potential_amplification_layer() -> str:
    payload = _safe_json(CIV_CONT_DIR / "human_potential.json", {})
    cohorts = payload.get("cohorts", []) if isinstance(payload, dict) else []
    amplified = [item for item in cohorts if isinstance(item, dict) and bool(item.get("amplified", False))]
    uneven = [item for item in cohorts if isinstance(item, dict) and bool(item.get("uneven", False))]
    return _overview("HUMAN POTENTIAL AMPLIFICATION LAYER - PHASE 891", "human-potential overview", [f"Cohorts tracked: {len(cohorts)}", f"Amplified cohorts: {len(amplified)}", f"Uneven cohorts: {len(uneven)}"], "Guardrail: potential amplification should preserve fairness, consent, and non-coercive access before rollout.")


def global_intelligence_collaboration_system() -> str:
    payload = _safe_json(CIV_CONT_DIR / "intelligence_collaboration.json", {})
    teams = payload.get("teams", []) if isinstance(payload, dict) else []
    linked = [item for item in teams if isinstance(item, dict) and bool(item.get("linked", False))]
    siloed = [item for item in teams if isinstance(item, dict) and bool(item.get("siloed", False))]
    return _overview("GLOBAL INTELLIGENCE COLLABORATION SYSTEM - PHASE 892", "intelligence-collaboration overview", [f"Teams tracked: {len(teams)}", f"Linked teams: {len(linked)}", f"Siloed teams: {len(siloed)}"], "Guardrail: collaboration systems should preserve attribution, boundaries, and secure sharing before federation.")


def recursive_innovation_engine() -> str:
    payload = _safe_json(CIV_CONT_DIR / "recursive_innovation.json", {})
    loops = payload.get("loops", []) if isinstance(payload, dict) else []
    compounding = [item for item in loops if isinstance(item, dict) and bool(item.get("compounding", False))]
    unstable = [item for item in loops if isinstance(item, dict) and bool(item.get("unstable", False))]
    return _overview("RECURSIVE INNOVATION ENGINE - PHASE 893", "recursive-innovation overview", [f"Loops tracked: {len(loops)}", f"Compounding loops: {len(compounding)}", f"Unstable loops: {len(unstable)}"], "Guardrail: recursive innovation should preserve test gates, ethics review, and rollback before acceleration.")


def self_expanding_scientific_frontier() -> str:
    payload = _safe_json(CIV_CONT_DIR / "scientific_frontier.json", {})
    programs = payload.get("programs", []) if isinstance(payload, dict) else []
    expanding = [item for item in programs if isinstance(item, dict) and bool(item.get("expanding", False))]
    speculative = [item for item in programs if isinstance(item, dict) and bool(item.get("speculative", False))]
    return _overview("SELF-EXPANDING SCIENTIFIC FRONTIER - PHASE 894", "scientific-frontier overview", [f"Programs tracked: {len(programs)}", f"Expanding programs: {len(expanding)}", f"Speculative programs: {len(speculative)}"], "Guardrail: scientific frontier growth should preserve replication, peer review, and clear epistemic boundaries before claims.")


def autonomous_civilization_mentor() -> str:
    payload = _safe_json(CIV_CONT_DIR / "civilization_mentor.json", {})
    mentors = payload.get("mentors", []) if isinstance(payload, dict) else []
    active = [item for item in mentors if isinstance(item, dict) and item.get("status") == "active"]
    overfit = [item for item in mentors if isinstance(item, dict) and bool(item.get("overfit", False))]
    return _overview("AUTONOMOUS CIVILIZATION MENTOR - PHASE 895", "civilization-mentor overview", [f"Mentors tracked: {len(mentors)}", f"Active mentors: {len(active)}", f"Overfit mentors: {len(overfit)}"], "Guardrail: civilization mentoring should remain advisory, plural, and subordinate to human deliberation before use.")


def ai_guided_planetary_evolution() -> str:
    payload = _safe_json(CIV_CONT_DIR / "planetary_evolution.json", {})
    pathways = payload.get("pathways", []) if isinstance(payload, dict) else []
    guided = [item for item in pathways if isinstance(item, dict) and bool(item.get("guided", False))]
    controversial = [item for item in pathways if isinstance(item, dict) and bool(item.get("controversial", False))]
    return _overview("AI-GUIDED PLANETARY EVOLUTION - PHASE 896", "planetary-evolution overview", [f"Pathways tracked: {len(pathways)}", f"Guided pathways: {len(guided)}", f"Controversial pathways: {len(controversial)}"], "Guardrail: planetary evolution scenarios should preserve humility, human legitimacy, and visible disagreement before planning.")


def universal_discovery_engine() -> str:
    payload = _safe_json(CIV_CONT_DIR / "universal_discovery.json", {})
    discoveries = payload.get("discoveries", []) if isinstance(payload, dict) else []
    surfaced = [item for item in discoveries if isinstance(item, dict) and bool(item.get("surfaced", False))]
    tentative = [item for item in discoveries if isinstance(item, dict) and bool(item.get("tentative", False))]
    return _overview("UNIVERSAL DISCOVERY ENGINE - PHASE 897", "universal-discovery overview", [f"Discoveries tracked: {len(discoveries)}", f"Surfaced discoveries: {len(surfaced)}", f"Tentative discoveries: {len(tentative)}"], "Guardrail: discovery engines should preserve falsifiability, provenance, and human review before announcement.")


def infinite_scale_cooperative_intelligence() -> str:
    payload = _safe_json(CIV_CONT_DIR / "cooperative_intelligence.json", {})
    cooperatives = payload.get("cooperatives", []) if isinstance(payload, dict) else []
    synchronized = [item for item in cooperatives if isinstance(item, dict) and bool(item.get("synchronized", False))]
    fragmented = [item for item in cooperatives if isinstance(item, dict) and bool(item.get("fragmented", False))]
    return _overview("INFINITE-SCALE COOPERATIVE INTELLIGENCE - PHASE 898", "cooperative-intelligence overview", [f"Cooperatives tracked: {len(cooperatives)}", f"Synchronized cooperatives: {len(synchronized)}", f"Fragmented cooperatives: {len(fragmented)}"], "Guardrail: cooperative intelligence should preserve autonomy, fairness, and anti-concentration safeguards before scale.")


def autonomous_interstellar_preparation_ai() -> str:
    payload = _safe_json(CIV_CONT_DIR / "interstellar_preparation.json", {})
    preparations = payload.get("preparations", []) if isinstance(payload, dict) else []
    staged = [item for item in preparations if isinstance(item, dict) and bool(item.get("staged", False))]
    premature = [item for item in preparations if isinstance(item, dict) and bool(item.get("premature", False))]
    return _overview("AUTONOMOUS INTERSTELLAR PREPARATION AI - PHASE 899", "interstellar-preparation overview", [f"Preparations tracked: {len(preparations)}", f"Staged preparations: {len(staged)}", f"Premature preparations: {len(premature)}"], "Guardrail: interstellar preparation should preserve realism, safety, and public accountability before mobilization.")


def species_continuity_intelligence() -> str:
    payload = _safe_json(CIV_CONT_DIR / "species_continuity.json", {})
    plans = payload.get("plans", []) if isinstance(payload, dict) else []
    durable = [item for item in plans if isinstance(item, dict) and bool(item.get("durable", False))]
    exposed = [item for item in plans if isinstance(item, dict) and bool(item.get("exposed", False))]
    return _overview("SPECIES CONTINUITY INTELLIGENCE - PHASE 900", "species-continuity overview", [f"Plans tracked: {len(plans)}", f"Durable plans: {len(durable)}", f"Exposed plans: {len(exposed)}"], "Guardrail: species continuity planning should preserve ethics, diversity, and resilience over narrow optimization.")
