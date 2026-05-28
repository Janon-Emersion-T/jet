from __future__ import annotations

import json
from pathlib import Path


GLOBAL_DEVELOPMENT_DIR = Path("storage/global_development")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def refugee_logistics_optimization() -> str:
    payload = _safe_json(GLOBAL_DEVELOPMENT_DIR / "refugee_logistics.json", {})
    corridors = payload.get("corridors", []) if isinstance(payload, dict) else []
    routed = [item for item in corridors if isinstance(item, dict) and bool(item.get("routed", False))]
    constrained = [item for item in corridors if isinstance(item, dict) and bool(item.get("constrained", False))]
    return _overview("REFUGEE LOGISTICS OPTIMIZATION - PHASE 781", "refugee-logistics overview", [f"Corridors tracked: {len(corridors)}", f"Routed corridors: {len(routed)}", f"Constrained corridors: {len(constrained)}"], "Guardrail: refugee logistics should preserve safety, dignity, and human rights before optimization is actioned.")


def global_health_intelligence_network() -> str:
    payload = _safe_json(GLOBAL_DEVELOPMENT_DIR / "global_health_network.json", {})
    nodes = payload.get("nodes", []) if isinstance(payload, dict) else []
    active = [item for item in nodes if isinstance(item, dict) and item.get("status") == "active"]
    verified = [item for item in nodes if isinstance(item, dict) and bool(item.get("verified", False))]
    return _overview("GLOBAL HEALTH INTELLIGENCE NETWORK - PHASE 782", "global-health-network overview", [f"Nodes tracked: {len(nodes)}", f"Active nodes: {len(active)}", f"Verified nodes: {len(verified)}"], "Guardrail: health intelligence should preserve privacy, epidemiological rigor, and public-health oversight before alerts.")


def pandemic_simulation_assistant() -> str:
    payload = _safe_json(GLOBAL_DEVELOPMENT_DIR / "pandemic_simulation.json", {})
    scenarios = payload.get("scenarios", []) if isinstance(payload, dict) else []
    modeled = [item for item in scenarios if isinstance(item, dict) and bool(item.get("modeled", False))]
    severe = [item for item in scenarios if isinstance(item, dict) and item.get("severity") == "severe"]
    return _overview("PANDEMIC SIMULATION ASSISTANT - PHASE 783", "pandemic-simulation overview", [f"Scenarios tracked: {len(scenarios)}", f"Modeled scenarios: {len(modeled)}", f"Severe scenarios: {len(severe)}"], "Guardrail: pandemic simulations should preserve uncertainty, public-health review, and non-alarmist communication before use.")


def autonomous_vaccine_research_framework() -> str:
    payload = _safe_json(GLOBAL_DEVELOPMENT_DIR / "vaccine_research.json", {})
    candidates = payload.get("candidates", []) if isinstance(payload, dict) else []
    screened = [item for item in candidates if isinstance(item, dict) and bool(item.get("screened", False))]
    promising = [item for item in candidates if isinstance(item, dict) and bool(item.get("promising", False))]
    return _overview("AUTONOMOUS VACCINE RESEARCH FRAMEWORK - PHASE 784", "vaccine-research overview", [f"Candidates tracked: {len(candidates)}", f"Screened candidates: {len(screened)}", f"Promising candidates: {len(promising)}"], "Guardrail: vaccine research support should preserve lab validation, biosafety, and regulatory review before claims.")


def ai_epidemiology_engine() -> str:
    payload = _safe_json(GLOBAL_DEVELOPMENT_DIR / "epidemiology_engine.json", {})
    outbreaks = payload.get("outbreaks", []) if isinstance(payload, dict) else []
    tracked = [item for item in outbreaks if isinstance(item, dict) and bool(item.get("tracked", False))]
    uncertain = [item for item in outbreaks if isinstance(item, dict) and bool(item.get("uncertain", False))]
    return _overview("AI EPIDEMIOLOGY ENGINE - PHASE 785", "epidemiology-engine overview", [f"Outbreaks tracked: {len(outbreaks)}", f"Tracked outbreaks: {len(tracked)}", f"Uncertain outbreaks: {len(uncertain)}"], "Guardrail: epidemiology support should preserve uncertainty, explainability, and public-health oversight before response actions.")


def smart_nutrition_optimization() -> str:
    payload = _safe_json(GLOBAL_DEVELOPMENT_DIR / "nutrition_optimization.json", {})
    plans = payload.get("plans", []) if isinstance(payload, dict) else []
    tailored = [item for item in plans if isinstance(item, dict) and bool(item.get("tailored", False))]
    deficient = [item for item in plans if isinstance(item, dict) and item.get("status") == "deficient"]
    return _overview("SMART NUTRITION OPTIMIZATION - PHASE 786", "nutrition-optimization overview", [f"Plans tracked: {len(plans)}", f"Tailored plans: {len(tailored)}", f"Deficient plans: {len(deficient)}"], "Guardrail: nutrition guidance should preserve clinical appropriateness, cultural fit, and clear non-medical boundaries where needed.")


def global_food_distribution_ai() -> str:
    payload = _safe_json(GLOBAL_DEVELOPMENT_DIR / "food_distribution.json", {})
    routes = payload.get("routes", []) if isinstance(payload, dict) else []
    optimized = [item for item in routes if isinstance(item, dict) and bool(item.get("optimized", False))]
    underserved = [item for item in routes if isinstance(item, dict) and bool(item.get("underserved", False))]
    return _overview("GLOBAL FOOD DISTRIBUTION AI - PHASE 787", "food-distribution overview", [f"Routes tracked: {len(routes)}", f"Optimized routes: {len(optimized)}", f"Underserved routes: {len(underserved)}"], "Guardrail: food distribution optimization should preserve equity, spoilage awareness, and local coordination before execution.")


def autonomous_anti_poverty_framework() -> str:
    payload = _safe_json(GLOBAL_DEVELOPMENT_DIR / "anti_poverty.json", {})
    programs = payload.get("programs", []) if isinstance(payload, dict) else []
    targeted = [item for item in programs if isinstance(item, dict) and bool(item.get("targeted", False))]
    reviewed = [item for item in programs if isinstance(item, dict) and bool(item.get("reviewed", False))]
    return _overview("AUTONOMOUS ANTI-POVERTY FRAMEWORK - PHASE 788", "anti-poverty overview", [f"Programs tracked: {len(programs)}", f"Targeted programs: {len(targeted)}", f"Reviewed programs: {len(reviewed)}"], "Guardrail: anti-poverty planning should preserve dignity, participation, and measurable harm review before prioritization.")


def education_equality_intelligence() -> str:
    payload = _safe_json(GLOBAL_DEVELOPMENT_DIR / "education_equality.json", {})
    districts = payload.get("districts", []) if isinstance(payload, dict) else []
    supported = [item for item in districts if isinstance(item, dict) and bool(item.get("supported", False))]
    underserved = [item for item in districts if isinstance(item, dict) and item.get("status") == "underserved"]
    return _overview("EDUCATION EQUALITY INTELLIGENCE - PHASE 789", "education-equality overview", [f"Districts tracked: {len(districts)}", f"Supported districts: {len(supported)}", f"Underserved districts: {len(underserved)}"], "Guardrail: education equality systems should preserve fairness, context sensitivity, and public accountability before resource shifts.")


def ai_driven_infrastructure_planning() -> str:
    payload = _safe_json(GLOBAL_DEVELOPMENT_DIR / "infrastructure_planning.json", {})
    projects = payload.get("projects", []) if isinstance(payload, dict) else []
    prioritized = [item for item in projects if isinstance(item, dict) and bool(item.get("prioritized", False))]
    blocked = [item for item in projects if isinstance(item, dict) and item.get("status") == "blocked"]
    return _overview("AI-DRIVEN INFRASTRUCTURE PLANNING - PHASE 790", "infrastructure-planning overview", [f"Projects tracked: {len(projects)}", f"Prioritized projects: {len(prioritized)}", f"Blocked projects: {len(blocked)}"], "Guardrail: infrastructure planning should preserve environmental review, community input, and procurement transparency before action.")
