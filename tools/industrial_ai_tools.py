from __future__ import annotations

import json
from pathlib import Path


INDUSTRIAL_AI_DIR = Path("storage/industrial_ai")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def ai_simulation_environment() -> str:
    payload = _safe_json(INDUSTRIAL_AI_DIR / "simulation_environment.json", {})
    scenarios = payload.get("scenarios", []) if isinstance(payload, dict) else []
    live = [item for item in scenarios if isinstance(item, dict) and item.get("status") == "live"]
    reproducible = [item for item in scenarios if isinstance(item, dict) and bool(item.get("reproducible", False))]
    return _overview("AI SIMULATION ENVIRONMENT - PHASE 611", "simulation-environment overview", [f"Scenarios tracked: {len(scenarios)}", f"Live scenarios: {len(live)}", f"Reproducible scenarios: {len(reproducible)}"], "Guardrail: simulation environments should remain controlled, reproducible, and safely separated from live operations.")


def reinforcement_learning_sandbox() -> str:
    payload = _safe_json(INDUSTRIAL_AI_DIR / "rl_sandbox.json", {})
    agents = payload.get("agents", []) if isinstance(payload, dict) else []
    training = [item for item in agents if isinstance(item, dict) and item.get("status") == "training"]
    safe = [item for item in agents if isinstance(item, dict) and bool(item.get("safety_bounds", False))]
    return _overview("REINFORCEMENT LEARNING SANDBOX - PHASE 612", "rl-sandbox overview", [f"Agents tracked: {len(agents)}", f"Training agents: {len(training)}", f"Safety-bounded agents: {len(safe)}"], "Guardrail: RL experimentation should stay sandboxed, reward-audited, and safety-bounded before any real-world transfer.")


def autonomous_robotics_planner() -> str:
    payload = _safe_json(INDUSTRIAL_AI_DIR / "robotics_planner.json", {})
    plans = payload.get("plans", []) if isinstance(payload, dict) else []
    collision_checked = [item for item in plans if isinstance(item, dict) and bool(item.get("collision_checked", False))]
    approved = [item for item in plans if isinstance(item, dict) and item.get("status") == "approved"]
    return _overview("AUTONOMOUS ROBOTICS PLANNER - PHASE 613", "robotics-planning overview", [f"Plans tracked: {len(plans)}", f"Collision-checked plans: {len(collision_checked)}", f"Approved plans: {len(approved)}"], "Guardrail: robotics planning should privilege safety constraints, fallback behavior, and operator approval before actuation.")


def robot_fleet_coordination() -> str:
    payload = _safe_json(INDUSTRIAL_AI_DIR / "robot_fleet.json", {})
    robots = payload.get("robots", []) if isinstance(payload, dict) else []
    online = [item for item in robots if isinstance(item, dict) and item.get("status") == "online"]
    queued = [item for item in robots if isinstance(item, dict) and bool(item.get("queue_assigned", False))]
    return _overview("ROBOT FLEET COORDINATION - PHASE 614", "robot-fleet overview", [f"Robots tracked: {len(robots)}", f"Online robots: {len(online)}", f"Queue-assigned robots: {len(queued)}"], "Guardrail: fleet coordination should avoid unsafe contention, preserve visibility, and support graceful degradation before dispatching robots.")


def ai_manufacturing_optimization() -> str:
    payload = _safe_json(INDUSTRIAL_AI_DIR / "manufacturing_optimization.json", {})
    lines = payload.get("lines", []) if isinstance(payload, dict) else []
    optimized = [item for item in lines if isinstance(item, dict) and bool(item.get("optimized", False))]
    bottlenecks = [item for item in lines if isinstance(item, dict) and item.get("status") == "bottleneck"]
    return _overview("AI MANUFACTURING OPTIMIZATION - PHASE 615", "manufacturing-optimization overview", [f"Production lines: {len(lines)}", f"Optimized lines: {len(optimized)}", f"Bottleneck lines: {len(bottlenecks)}"], "Guardrail: manufacturing optimization should respect safety, quality, and throughput tradeoffs before changing production flow.")


def predictive_factory_analytics() -> str:
    payload = _safe_json(INDUSTRIAL_AI_DIR / "factory_analytics.json", {})
    assets = payload.get("assets", []) if isinstance(payload, dict) else []
    at_risk = [item for item in assets if isinstance(item, dict) and item.get("risk") == "high"]
    stable = [item for item in assets if isinstance(item, dict) and item.get("risk") == "low"]
    return _overview("PREDICTIVE FACTORY ANALYTICS - PHASE 616", "factory-analytics overview", [f"Assets tracked: {len(assets)}", f"High-risk assets: {len(at_risk)}", f"Low-risk assets: {len(stable)}"], "Guardrail: factory analytics should favor actionable evidence, clear thresholds, and human-readable diagnostics before driving operations.")


def autonomous_quality_assurance() -> str:
    payload = _safe_json(INDUSTRIAL_AI_DIR / "quality_assurance.json", {})
    checks = payload.get("checks", []) if isinstance(payload, dict) else []
    passed = [item for item in checks if isinstance(item, dict) and item.get("status") == "passed"]
    failed = [item for item in checks if isinstance(item, dict) and item.get("status") == "failed"]
    return _overview("AUTONOMOUS QUALITY ASSURANCE - PHASE 617", "quality-assurance overview", [f"Checks tracked: {len(checks)}", f"Passed checks: {len(passed)}", f"Failed checks: {len(failed)}"], "Guardrail: autonomous QA should preserve auditability, traceability, and stop conditions before allowing defects downstream.")


def machine_vision_inspection_system() -> str:
    payload = _safe_json(INDUSTRIAL_AI_DIR / "machine_vision.json", {})
    inspections = payload.get("inspections", []) if isinstance(payload, dict) else []
    defects = [item for item in inspections if isinstance(item, dict) and bool(item.get("defect_detected", False))]
    reviewed = [item for item in inspections if isinstance(item, dict) and bool(item.get("reviewed", False))]
    return _overview("MACHINE VISION INSPECTION SYSTEM - PHASE 618", "machine-vision overview", [f"Inspections tracked: {len(inspections)}", f"Defect detections: {len(defects)}", f"Reviewed inspections: {len(reviewed)}"], "Guardrail: machine vision should expose confidence, lighting limitations, and human review paths before rejecting output.")


def ai_predictive_maintenance() -> str:
    payload = _safe_json(INDUSTRIAL_AI_DIR / "predictive_maintenance_ai.json", {})
    machines = payload.get("machines", []) if isinstance(payload, dict) else []
    scheduled = [item for item in machines if isinstance(item, dict) and bool(item.get("maintenance_scheduled", False))]
    failing = [item for item in machines if isinstance(item, dict) and item.get("health") == "failing"]
    return _overview("AI PREDICTIVE MAINTENANCE - PHASE 619", "predictive-maintenance-ai overview", [f"Machines tracked: {len(machines)}", f"Scheduled maintenance machines: {len(scheduled)}", f"Failing-health machines: {len(failing)}"], "Guardrail: predictive maintenance should reduce downtime while preserving service windows and operator context before intervention.")


def industrial_iot_integration() -> str:
    payload = _safe_json(INDUSTRIAL_AI_DIR / "industrial_iot.json", {})
    devices = payload.get("devices", []) if isinstance(payload, dict) else []
    connected = [item for item in devices if isinstance(item, dict) and item.get("status") == "connected"]
    unsecured = [item for item in devices if isinstance(item, dict) and bool(item.get("unsecured", False))]
    return _overview("INDUSTRIAL IOT INTEGRATION - PHASE 620", "industrial-iot overview", [f"Devices tracked: {len(devices)}", f"Connected devices: {len(connected)}", f"Unsecured devices: {len(unsecured)}"], "Guardrail: industrial IoT integration should foreground device security, data integrity, and network segmentation before expansion.")
