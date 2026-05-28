from __future__ import annotations

import json
from pathlib import Path


SPACE_CIV_DIR = Path("storage/space_civilization")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def planetary_coordination_framework() -> str:
    payload = _safe_json(SPACE_CIV_DIR / "planetary_coordination.json", {})
    councils = payload.get("councils", []) if isinstance(payload, dict) else []
    aligned = [item for item in councils if isinstance(item, dict) and bool(item.get("aligned", False))]
    urgent = [item for item in councils if isinstance(item, dict) and item.get("priority") == "urgent"]
    return _overview("PLANETARY COORDINATION FRAMEWORK - PHASE 801", "planetary-coordination overview", [f"Councils tracked: {len(councils)}", f"Aligned councils: {len(aligned)}", f"Urgent councils: {len(urgent)}"], "Guardrail: planetary coordination should remain participatory, transparent, and subordinate to legitimate human governance.")


def space_colonization_planning_ai() -> str:
    payload = _safe_json(SPACE_CIV_DIR / "space_colonization.json", {})
    missions = payload.get("missions", []) if isinstance(payload, dict) else []
    modeled = [item for item in missions if isinstance(item, dict) and bool(item.get("modeled", False))]
    constrained = [item for item in missions if isinstance(item, dict) and bool(item.get("constrained", False))]
    return _overview("SPACE COLONIZATION PLANNING AI - PHASE 802", "space-colonization overview", [f"Missions tracked: {len(missions)}", f"Modeled missions: {len(modeled)}", f"Constrained missions: {len(constrained)}"], "Guardrail: colonization planning should preserve ethics, planetary protection, and clear human oversight before recommendation.")


def autonomous_habitat_simulation() -> str:
    payload = _safe_json(SPACE_CIV_DIR / "habitat_simulation.json", {})
    habitats = payload.get("habitats", []) if isinstance(payload, dict) else []
    viable = [item for item in habitats if isinstance(item, dict) and bool(item.get("viable", False))]
    stressed = [item for item in habitats if isinstance(item, dict) and item.get("status") == "stressed"]
    return _overview("AUTONOMOUS HABITAT SIMULATION - PHASE 803", "habitat-simulation overview", [f"Habitats tracked: {len(habitats)}", f"Viable habitats: {len(viable)}", f"Stressed habitats: {len(stressed)}"], "Guardrail: habitat simulation should preserve safety margins, uncertainty, and engineering review before deployment.")


def interplanetary_logistics_engine() -> str:
    payload = _safe_json(SPACE_CIV_DIR / "interplanetary_logistics.json", {})
    routes = payload.get("routes", []) if isinstance(payload, dict) else []
    active = [item for item in routes if isinstance(item, dict) and item.get("status") == "active"]
    delayed = [item for item in routes if isinstance(item, dict) and bool(item.get("delayed", False))]
    return _overview("INTERPLANETARY LOGISTICS ENGINE - PHASE 804", "interplanetary-logistics overview", [f"Routes tracked: {len(routes)}", f"Active routes: {len(active)}", f"Delayed routes: {len(delayed)}"], "Guardrail: interplanetary logistics should preserve mission safety, redundancy, and explicit human approval for critical actions.")


def extraterrestrial_research_assistant() -> str:
    payload = _safe_json(SPACE_CIV_DIR / "extraterrestrial_research.json", {})
    studies = payload.get("studies", []) if isinstance(payload, dict) else []
    reviewed = [item for item in studies if isinstance(item, dict) and bool(item.get("reviewed", False))]
    sensitive = [item for item in studies if isinstance(item, dict) and bool(item.get("sensitive", False))]
    return _overview("EXTRATERRESTRIAL RESEARCH ASSISTANT - PHASE 805", "extraterrestrial-research overview", [f"Studies tracked: {len(studies)}", f"Reviewed studies: {len(reviewed)}", f"Sensitive studies: {len(sensitive)}"], "Guardrail: extraterrestrial research should preserve scientific rigor, contamination controls, and cautious interpretation.")


def ai_biosphere_management() -> str:
    payload = _safe_json(SPACE_CIV_DIR / "biosphere_management.json", {})
    systems = payload.get("systems", []) if isinstance(payload, dict) else []
    balanced = [item for item in systems if isinstance(item, dict) and bool(item.get("balanced", False))]
    fragile = [item for item in systems if isinstance(item, dict) and item.get("status") == "fragile"]
    return _overview("AI BIOSPHERE MANAGEMENT - PHASE 806", "biosphere-management overview", [f"Systems tracked: {len(systems)}", f"Balanced systems: {len(balanced)}", f"Fragile systems: {len(fragile)}"], "Guardrail: biosphere management should preserve ecological humility, fail-safes, and human stewardship before control loops expand.")


def long_duration_survival_intelligence() -> str:
    payload = _safe_json(SPACE_CIV_DIR / "long_duration_survival.json", {})
    plans = payload.get("plans", []) if isinstance(payload, dict) else []
    resilient = [item for item in plans if isinstance(item, dict) and bool(item.get("resilient", False))]
    scarce = [item for item in plans if isinstance(item, dict) and item.get("status") == "scarce"]
    return _overview("LONG-DURATION SURVIVAL INTELLIGENCE - PHASE 807", "long-duration-survival overview", [f"Plans tracked: {len(plans)}", f"Resilient plans: {len(resilient)}", f"Scarcity-flagged plans: {len(scarce)}"], "Guardrail: survival planning should preserve human welfare, redundancy, and direct oversight before execution.")


def autonomous_terraforming_simulation() -> str:
    payload = _safe_json(SPACE_CIV_DIR / "terraforming_simulation.json", {})
    scenarios = payload.get("scenarios", []) if isinstance(payload, dict) else []
    modeled = [item for item in scenarios if isinstance(item, dict) and bool(item.get("modeled", False))]
    risky = [item for item in scenarios if isinstance(item, dict) and item.get("risk") == "high"]
    return _overview("AUTONOMOUS TERRAFORMING SIMULATION - PHASE 808", "terraforming-simulation overview", [f"Scenarios tracked: {len(scenarios)}", f"Modeled scenarios: {len(modeled)}", f"High-risk scenarios: {len(risky)}"], "Guardrail: terraforming simulations should remain hypothetical, uncertainty-aware, and heavily constrained by ethical review.")


def cosmic_scale_data_analysis() -> str:
    payload = _safe_json(SPACE_CIV_DIR / "cosmic_data_analysis.json", {})
    datasets = payload.get("datasets", []) if isinstance(payload, dict) else []
    indexed = [item for item in datasets if isinstance(item, dict) and bool(item.get("indexed", False))]
    anomalous = [item for item in datasets if isinstance(item, dict) and bool(item.get("anomalous", False))]
    return _overview("COSMIC-SCALE DATA ANALYSIS - PHASE 809", "cosmic-data-analysis overview", [f"Datasets tracked: {len(datasets)}", f"Indexed datasets: {len(indexed)}", f"Anomalous datasets: {len(anomalous)}"], "Guardrail: large-scale scientific analysis should preserve provenance, reproducibility, and careful uncertainty handling before claims.")


def universal_scientific_archive_ai() -> str:
    payload = _safe_json(SPACE_CIV_DIR / "scientific_archive.json", {})
    archives = payload.get("archives", []) if isinstance(payload, dict) else []
    curated = [item for item in archives if isinstance(item, dict) and bool(item.get("curated", False))]
    incomplete = [item for item in archives if isinstance(item, dict) and bool(item.get("incomplete", False))]
    return _overview("UNIVERSAL SCIENTIFIC ARCHIVE AI - PHASE 810", "scientific-archive overview", [f"Archives tracked: {len(archives)}", f"Curated archives: {len(curated)}", f"Incomplete archives: {len(incomplete)}"], "Guardrail: scientific archiving should preserve attribution, accessibility, and correction mechanisms before universal indexing.")
