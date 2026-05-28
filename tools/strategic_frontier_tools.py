from __future__ import annotations

import json
from pathlib import Path


STRATEGIC_FRONTIER_DIR = Path("storage/strategic_frontier")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def strategic_operations_planner() -> str:
    payload = _safe_json(STRATEGIC_FRONTIER_DIR / "strategic_operations.json", {})
    plans = payload.get("plans", []) if isinstance(payload, dict) else []
    prioritized = [item for item in plans if isinstance(item, dict) and bool(item.get("prioritized", False))]
    funded = [item for item in plans if isinstance(item, dict) and bool(item.get("funded", False))]
    return _overview("STRATEGIC OPERATIONS PLANNER - PHASE 651", "strategic-operations overview", [f"Plans tracked: {len(plans)}", f"Prioritized plans: {len(prioritized)}", f"Funded plans: {len(funded)}"], "Guardrail: strategic operations planning should remain capacity-aware, evidence-backed, and explicitly governed before execution.")


def multi_domain_simulation_engine() -> str:
    payload = _safe_json(STRATEGIC_FRONTIER_DIR / "multi_domain_simulation.json", {})
    domains = payload.get("domains", []) if isinstance(payload, dict) else []
    linked = [item for item in domains if isinstance(item, dict) and bool(item.get("linked", False))]
    validated = [item for item in domains if isinstance(item, dict) and bool(item.get("validated", False))]
    return _overview("MULTI-DOMAIN SIMULATION ENGINE - PHASE 652", "multi-domain-simulation overview", [f"Domains tracked: {len(domains)}", f"Linked domains: {len(linked)}", f"Validated domains: {len(validated)}"], "Guardrail: multi-domain simulations should preserve domain boundaries, assumptions, and reviewability before informing decisions.")


def ai_aerospace_assistant() -> str:
    payload = _safe_json(STRATEGIC_FRONTIER_DIR / "aerospace_assistant.json", {})
    missions = payload.get("missions", []) if isinstance(payload, dict) else []
    reviewed = [item for item in missions if isinstance(item, dict) and bool(item.get("reviewed", False))]
    high_risk = [item for item in missions if isinstance(item, dict) and item.get("risk") == "high"]
    return _overview("AI AEROSPACE ASSISTANT - PHASE 653", "aerospace-assistant overview", [f"Missions tracked: {len(missions)}", f"Reviewed missions: {len(reviewed)}", f"High-risk missions: {len(high_risk)}"], "Guardrail: aerospace guidance should remain engineering-reviewed, safety-bounded, and clear about uncertainty before action.")


def satellite_data_interpretation() -> str:
    payload = _safe_json(STRATEGIC_FRONTIER_DIR / "satellite_data.json", {})
    scenes = payload.get("scenes", []) if isinstance(payload, dict) else []
    processed = [item for item in scenes if isinstance(item, dict) and bool(item.get("processed", False))]
    flagged = [item for item in scenes if isinstance(item, dict) and bool(item.get("flagged", False))]
    return _overview("SATELLITE DATA INTERPRETATION - PHASE 654", "satellite-interpretation overview", [f"Scenes tracked: {len(scenes)}", f"Processed scenes: {len(processed)}", f"Flagged scenes: {len(flagged)}"], "Guardrail: satellite interpretation should preserve provenance, calibration context, and analyst review before use.")


def autonomous_mission_planning() -> str:
    payload = _safe_json(STRATEGIC_FRONTIER_DIR / "mission_planning.json", {})
    plans = payload.get("plans", []) if isinstance(payload, dict) else []
    approved = [item for item in plans if isinstance(item, dict) and item.get("status") == "approved"]
    constrained = [item for item in plans if isinstance(item, dict) and bool(item.get("constraint_checked", False))]
    return _overview("AUTONOMOUS MISSION PLANNING - PHASE 655", "mission-planning overview", [f"Mission plans: {len(plans)}", f"Approved plans: {len(approved)}", f"Constraint-checked plans: {len(constrained)}"], "Guardrail: mission planning should prioritize safety envelopes, resource limits, and accountable approval before execution.")


def space_systems_simulation() -> str:
    payload = _safe_json(STRATEGIC_FRONTIER_DIR / "space_systems.json", {})
    runs = payload.get("runs", []) if isinstance(payload, dict) else []
    complete = [item for item in runs if isinstance(item, dict) and item.get("status") == "complete"]
    anomalous = [item for item in runs if isinstance(item, dict) and bool(item.get("anomalous", False))]
    return _overview("SPACE SYSTEMS SIMULATION - PHASE 656", "space-systems overview", [f"Simulation runs: {len(runs)}", f"Completed runs: {len(complete)}", f"Anomalous runs: {len(anomalous)}"], "Guardrail: space systems simulation should preserve physical assumptions, anomaly visibility, and engineering review before operational use.")


def ai_astronomy_research_assistant() -> str:
    payload = _safe_json(STRATEGIC_FRONTIER_DIR / "astronomy_research.json", {})
    observations = payload.get("observations", []) if isinstance(payload, dict) else []
    annotated = [item for item in observations if isinstance(item, dict) and bool(item.get("annotated", False))]
    uncertain = [item for item in observations if isinstance(item, dict) and bool(item.get("uncertain", False))]
    return _overview("AI ASTRONOMY RESEARCH ASSISTANT - PHASE 657", "astronomy-research overview", [f"Observations tracked: {len(observations)}", f"Annotated observations: {len(annotated)}", f"Uncertain observations: {len(uncertain)}"], "Guardrail: astronomy assistance should highlight uncertainty, instrument limits, and researcher review rather than overclaiming results.")


def autonomous_observatory_manager() -> str:
    payload = _safe_json(STRATEGIC_FRONTIER_DIR / "observatory_manager.json", {})
    schedules = payload.get("schedules", []) if isinstance(payload, dict) else []
    active = [item for item in schedules if isinstance(item, dict) and item.get("status") == "active"]
    weather_safe = [item for item in schedules if isinstance(item, dict) and bool(item.get("weather_safe", False))]
    return _overview("AUTONOMOUS OBSERVATORY MANAGER - PHASE 658", "observatory-management overview", [f"Schedules tracked: {len(schedules)}", f"Active schedules: {len(active)}", f"Weather-safe schedules: {len(weather_safe)}"], "Guardrail: observatory automation should preserve equipment safety, weather constraints, and operator override before control.")


def quantum_computing_interface_layer() -> str:
    payload = _safe_json(STRATEGIC_FRONTIER_DIR / "quantum_interface.json", {})
    backends = payload.get("backends", []) if isinstance(payload, dict) else []
    connected = [item for item in backends if isinstance(item, dict) and item.get("status") == "connected"]
    calibrated = [item for item in backends if isinstance(item, dict) and bool(item.get("calibrated", False))]
    return _overview("QUANTUM COMPUTING INTERFACE LAYER - PHASE 659", "quantum-interface overview", [f"Backends tracked: {len(backends)}", f"Connected backends: {len(connected)}", f"Calibrated backends: {len(calibrated)}"], "Guardrail: quantum interfaces should preserve backend state, calibration context, and experiment isolation before execution.")


def quantum_algorithm_assistant() -> str:
    payload = _safe_json(STRATEGIC_FRONTIER_DIR / "quantum_algorithms.json", {})
    algorithms = payload.get("algorithms", []) if isinstance(payload, dict) else []
    compiled = [item for item in algorithms if isinstance(item, dict) and bool(item.get("compiled", False))]
    benchmarked = [item for item in algorithms if isinstance(item, dict) and bool(item.get("benchmarked", False))]
    return _overview("QUANTUM ALGORITHM ASSISTANT - PHASE 660", "quantum-algorithm overview", [f"Algorithms tracked: {len(algorithms)}", f"Compiled algorithms: {len(compiled)}", f"Benchmarked algorithms: {len(benchmarked)}"], "Guardrail: quantum algorithm support should remain benchmark-aware, backend-specific, and explicit about tradeoffs before recommendation.")
