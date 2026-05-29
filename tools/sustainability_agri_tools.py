from __future__ import annotations

import json
from pathlib import Path


SUSTAINABILITY_DIR = Path("storage/sustainability_agri")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def autonomous_energy_optimization() -> str:
    payload = _safe_json(SUSTAINABILITY_DIR / "energy_optimization.json", {})
    sites = payload.get("sites", []) if isinstance(payload, dict) else []
    optimized = [item for item in sites if isinstance(item, dict) and bool(item.get("optimized", False))]
    peaks = [item for item in sites if isinstance(item, dict) and item.get("status") == "peak"]
    return _overview("AUTONOMOUS ENERGY OPTIMIZATION - PHASE 621", "energy-optimization overview", [f"Sites tracked: {len(sites)}", f"Optimized sites: {len(optimized)}", f"Peak-load sites: {len(peaks)}"], "Guardrail: energy optimization should respect operational constraints, resilience, and cost visibility before shifting loads.")


def smart_grid_management_ai() -> str:
    payload = _safe_json(SUSTAINABILITY_DIR / "smart_grid.json", {})
    nodes = payload.get("nodes", []) if isinstance(payload, dict) else []
    balanced = [item for item in nodes if isinstance(item, dict) and bool(item.get("balanced", False))]
    unstable = [item for item in nodes if isinstance(item, dict) and item.get("status") == "unstable"]
    return _overview("SMART GRID MANAGEMENT AI - PHASE 622", "smart-grid overview", [f"Grid nodes: {len(nodes)}", f"Balanced nodes: {len(balanced)}", f"Unstable nodes: {len(unstable)}"], "Guardrail: grid intelligence should privilege stability, safety margins, and operator control before automated balancing.")


def environmental_monitoring_intelligence() -> str:
    payload = _safe_json(SUSTAINABILITY_DIR / "environmental_monitoring.json", {})
    sensors = payload.get("sensors", []) if isinstance(payload, dict) else []
    alerts = [item for item in sensors if isinstance(item, dict) and bool(item.get("alert", False))]
    healthy = [item for item in sensors if isinstance(item, dict) and item.get("status") == "healthy"]
    return _overview("ENVIRONMENTAL MONITORING INTELLIGENCE - PHASE 623", "environmental-monitoring overview", [f"Sensors tracked: {len(sensors)}", f"Alerting sensors: {len(alerts)}", f"Healthy sensors: {len(healthy)}"], "Guardrail: environmental monitoring should highlight data quality, thresholds, and intervention context before escalation.")


def climate_simulation_assistant() -> str:
    payload = _safe_json(SUSTAINABILITY_DIR / "climate_simulation.json", {})
    runs = payload.get("runs", []) if isinstance(payload, dict) else []
    completed = [item for item in runs if isinstance(item, dict) and item.get("status") == "completed"]
    uncertain = [item for item in runs if isinstance(item, dict) and bool(item.get("uncertain", False))]
    return _overview("CLIMATE SIMULATION ASSISTANT - PHASE 624", "climate-simulation overview", [f"Simulation runs: {len(runs)}", f"Completed runs: {len(completed)}", f"Uncertain runs: {len(uncertain)}"], "Guardrail: climate simulations should preserve assumptions, uncertainty, and scenario context before policy recommendations.")


def agricultural_ai_orchestration() -> str:
    payload = _safe_json(SUSTAINABILITY_DIR / "agri_orchestration.json", {})
    farms = payload.get("farms", []) if isinstance(payload, dict) else []
    coordinated = [item for item in farms if isinstance(item, dict) and bool(item.get("coordinated", False))]
    stressed = [item for item in farms if isinstance(item, dict) and item.get("status") == "stressed"]
    return _overview("AGRICULTURAL AI ORCHESTRATION - PHASE 625", "agriculture-orchestration overview", [f"Farms tracked: {len(farms)}", f"Coordinated farms: {len(coordinated)}", f"Stressed farms: {len(stressed)}"], "Guardrail: agricultural orchestration should respect local conditions, farmer control, and seasonal uncertainty before automation.")


def precision_farming_engine() -> str:
    payload = _safe_json(SUSTAINABILITY_DIR / "precision_farming.json", {})
    plots = payload.get("plots", []) if isinstance(payload, dict) else []
    targeted = [item for item in plots if isinstance(item, dict) and bool(item.get("targeted", False))]
    low_yield = [item for item in plots if isinstance(item, dict) and item.get("yield") == "low"]
    return _overview("PRECISION FARMING ENGINE - PHASE 626", "precision-farming overview", [f"Plots tracked: {len(plots)}", f"Targeted plots: {len(targeted)}", f"Low-yield plots: {len(low_yield)}"], "Guardrail: precision farming should preserve agronomic context, input limits, and environmental impact before changing treatment.")


def smart_irrigation_optimizer() -> str:
    payload = _safe_json(SUSTAINABILITY_DIR / "irrigation.json", {})
    zones = payload.get("zones", []) if isinstance(payload, dict) else []
    optimized = [item for item in zones if isinstance(item, dict) and bool(item.get("optimized", False))]
    dry = [item for item in zones if isinstance(item, dict) and item.get("status") == "dry"]
    return _overview("SMART IRRIGATION OPTIMIZER - PHASE 627", "irrigation-optimization overview", [f"Zones tracked: {len(zones)}", f"Optimized zones: {len(optimized)}", f"Dry zones: {len(dry)}"], "Guardrail: irrigation optimization should balance crop health, water conservation, and local constraints before changing schedules.")


def livestock_monitoring_ai() -> str:
    payload = _safe_json(SUSTAINABILITY_DIR / "livestock_monitoring.json", {})
    herds = payload.get("herds", []) if isinstance(payload, dict) else []
    monitored = [item for item in herds if isinstance(item, dict) and bool(item.get("monitored", False))]
    at_risk = [item for item in herds if isinstance(item, dict) and item.get("risk") == "high"]
    return _overview("LIVESTOCK MONITORING AI - PHASE 628", "livestock-monitoring overview", [f"Herds tracked: {len(herds)}", f"Monitored herds: {len(monitored)}", f"High-risk herds: {len(at_risk)}"], "Guardrail: livestock monitoring should support welfare, sensor reliability, and human oversight before intervention.")
