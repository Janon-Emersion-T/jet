from __future__ import annotations

import json
from pathlib import Path


PLANETARY_HUMANITARIAN_DIR = Path("storage/planetary_humanitarian")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def synthetic_society_simulation() -> str:
    payload = _safe_json(PLANETARY_HUMANITARIAN_DIR / "synthetic_society.json", {})
    populations = payload.get("populations", []) if isinstance(payload, dict) else []
    modeled = [item for item in populations if isinstance(item, dict) and bool(item.get("modeled", False))]
    diverse = [item for item in populations if isinstance(item, dict) and bool(item.get("diverse", False))]
    return _overview("SYNTHETIC SOCIETY SIMULATION - PHASE 771", "synthetic-society overview", [f"Populations tracked: {len(populations)}", f"Modeled populations: {len(modeled)}", f"Diverse populations: {len(diverse)}"], "Guardrail: society simulations should preserve representation limits, uncertainty, and non-deterministic framing.")


def ai_assisted_civilization_planning() -> str:
    payload = _safe_json(PLANETARY_HUMANITARIAN_DIR / "civilization_planning.json", {})
    plans = payload.get("plans", []) if isinstance(payload, dict) else []
    reviewed = [item for item in plans if isinstance(item, dict) and bool(item.get("reviewed", False))]
    equitable = [item for item in plans if isinstance(item, dict) and bool(item.get("equitable", False))]
    return _overview("AI-ASSISTED CIVILIZATION PLANNING - PHASE 772", "civilization-planning overview", [f"Plans tracked: {len(plans)}", f"Reviewed plans: {len(reviewed)}", f"Equitable plans: {len(equitable)}"], "Guardrail: civilization planning should remain pluralistic, revisable, and grounded in human consent before recommendation.")


def planetary_scale_optimization_ai() -> str:
    payload = _safe_json(PLANETARY_HUMANITARIAN_DIR / "planetary_optimization.json", {})
    systems = payload.get("systems", []) if isinstance(payload, dict) else []
    optimized = [item for item in systems if isinstance(item, dict) and bool(item.get("optimized", False))]
    constrained = [item for item in systems if isinstance(item, dict) and bool(item.get("constrained", False))]
    return _overview("PLANETARY-SCALE OPTIMIZATION AI - PHASE 773", "planetary-optimization overview", [f"Systems tracked: {len(systems)}", f"Optimized systems: {len(optimized)}", f"Constrained systems: {len(constrained)}"], "Guardrail: planetary optimization should preserve democratic legitimacy, ecological caution, and reversible pathways before coordination.")


def sustainable_resource_balancing_engine() -> str:
    payload = _safe_json(PLANETARY_HUMANITARIAN_DIR / "resource_balancing.json", {})
    resources = payload.get("resources", []) if isinstance(payload, dict) else []
    balanced = [item for item in resources if isinstance(item, dict) and bool(item.get("balanced", False))]
    stressed = [item for item in resources if isinstance(item, dict) and item.get("status") == "stressed"]
    return _overview("SUSTAINABLE RESOURCE BALANCING ENGINE - PHASE 774", "resource-balancing overview", [f"Resources tracked: {len(resources)}", f"Balanced resources: {len(balanced)}", f"Stressed resources: {len(stressed)}"], "Guardrail: resource balancing should preserve justice, ecological regeneration, and transparent tradeoffs before policy use.")


def climate_intervention_simulation() -> str:
    payload = _safe_json(PLANETARY_HUMANITARIAN_DIR / "climate_intervention.json", {})
    interventions = payload.get("interventions", []) if isinstance(payload, dict) else []
    modeled = [item for item in interventions if isinstance(item, dict) and bool(item.get("modeled", False))]
    high_risk = [item for item in interventions if isinstance(item, dict) and item.get("risk") == "high"]
    return _overview("CLIMATE INTERVENTION SIMULATION - PHASE 775", "climate-intervention overview", [f"Interventions tracked: {len(interventions)}", f"Modeled interventions: {len(modeled)}", f"High-risk interventions: {len(high_risk)}"], "Guardrail: climate intervention simulations should preserve precaution, externality review, and global governance context before use.")


def ocean_monitoring_intelligence() -> str:
    payload = _safe_json(PLANETARY_HUMANITARIAN_DIR / "ocean_monitoring.json", {})
    zones = payload.get("zones", []) if isinstance(payload, dict) else []
    monitored = [item for item in zones if isinstance(item, dict) and bool(item.get("monitored", False))]
    degraded = [item for item in zones if isinstance(item, dict) and item.get("status") == "degraded"]
    return _overview("OCEAN MONITORING INTELLIGENCE - PHASE 776", "ocean-monitoring overview", [f"Zones tracked: {len(zones)}", f"Monitored zones: {len(monitored)}", f"Degraded zones: {len(degraded)}"], "Guardrail: ocean monitoring should preserve open science, ecological humility, and verification before intervention.")


def wildlife_preservation_ai() -> str:
    payload = _safe_json(PLANETARY_HUMANITARIAN_DIR / "wildlife_preservation.json", {})
    habitats = payload.get("habitats", []) if isinstance(payload, dict) else []
    protected = [item for item in habitats if isinstance(item, dict) and bool(item.get("protected", False))]
    threatened = [item for item in habitats if isinstance(item, dict) and item.get("risk") == "threatened"]
    return _overview("WILDLIFE PRESERVATION AI - PHASE 777", "wildlife-preservation overview", [f"Habitats tracked: {len(habitats)}", f"Protected habitats: {len(protected)}", f"Threatened habitats: {len(threatened)}"], "Guardrail: wildlife preservation should preserve biodiversity priorities and avoid extractive optimization logic.")


def biodiversity_prediction_system() -> str:
    payload = _safe_json(PLANETARY_HUMANITARIAN_DIR / "biodiversity_prediction.json", {})
    forecasts = payload.get("forecasts", []) if isinstance(payload, dict) else []
    calibrated = [item for item in forecasts if isinstance(item, dict) and bool(item.get("calibrated", False))]
    declining = [item for item in forecasts if isinstance(item, dict) and item.get("trend") == "declining"]
    return _overview("BIODIVERSITY PREDICTION SYSTEM - PHASE 778", "biodiversity-prediction overview", [f"Forecasts tracked: {len(forecasts)}", f"Calibrated forecasts: {len(calibrated)}", f"Declining forecasts: {len(declining)}"], "Guardrail: biodiversity forecasts should preserve uncertainty and direct field validation before prescriptive use.")


def ecosystem_recovery_planner() -> str:
    payload = _safe_json(PLANETARY_HUMANITARIAN_DIR / "ecosystem_recovery.json", {})
    programs = payload.get("programs", []) if isinstance(payload, dict) else []
    active = [item for item in programs if isinstance(item, dict) and item.get("status") == "active"]
    restored = [item for item in programs if isinstance(item, dict) and bool(item.get("restored", False))]
    return _overview("ECOSYSTEM RECOVERY PLANNER - PHASE 779", "ecosystem-recovery overview", [f"Programs tracked: {len(programs)}", f"Active programs: {len(active)}", f"Restored programs: {len(restored)}"], "Guardrail: recovery planning should preserve local stewardship, ecological fit, and long-term monitoring before execution.")


def ai_humanitarian_operations_layer() -> str:
    payload = _safe_json(PLANETARY_HUMANITARIAN_DIR / "humanitarian_operations.json", {})
    operations = payload.get("operations", []) if isinstance(payload, dict) else []
    coordinated = [item for item in operations if isinstance(item, dict) and bool(item.get("coordinated", False))]
    urgent = [item for item in operations if isinstance(item, dict) and item.get("priority") == "urgent"]
    return _overview("AI HUMANITARIAN OPERATIONS LAYER - PHASE 780", "humanitarian-operations overview", [f"Operations tracked: {len(operations)}", f"Coordinated operations: {len(coordinated)}", f"Urgent operations: {len(urgent)}"], "Guardrail: humanitarian operations should preserve neutrality, dignity, and human-led accountability before deployment.")
