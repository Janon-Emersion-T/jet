from __future__ import annotations

import json
from pathlib import Path


STRATEGIC_GOVERNANCE_DIR = Path("storage/strategic_governance_expansion")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def ai_sales_ecosystem() -> str:
    payload = _safe_json(STRATEGIC_GOVERNANCE_DIR / "sales_ecosystem.json", {})
    pipelines = payload.get("pipelines", []) if isinstance(payload, dict) else []
    active = [item for item in pipelines if isinstance(item, dict) and item.get("status") == "active"]
    assisted = [item for item in pipelines if isinstance(item, dict) and bool(item.get("assisted", False))]
    return _overview("AI SALES ECOSYSTEM - PHASE 751", "sales-ecosystem overview", [f"Pipelines tracked: {len(pipelines)}", f"Active pipelines: {len(active)}", f"AI-assisted pipelines: {len(assisted)}"], "Guardrail: sales automation should preserve consent, truthful claims, and human accountability before customer outreach.")


def negotiation_intelligence_framework() -> str:
    payload = _safe_json(STRATEGIC_GOVERNANCE_DIR / "negotiation_intelligence.json", {})
    negotiations = payload.get("negotiations", []) if isinstance(payload, dict) else []
    prepared = [item for item in negotiations if isinstance(item, dict) and bool(item.get("prepared", False))]
    bounded = [item for item in negotiations if isinstance(item, dict) and bool(item.get("bounded", False))]
    return _overview("NEGOTIATION INTELLIGENCE FRAMEWORK - PHASE 752", "negotiation-intelligence overview", [f"Negotiations tracked: {len(negotiations)}", f"Prepared negotiations: {len(prepared)}", f"Bounded negotiations: {len(bounded)}"], "Guardrail: negotiation support should preserve legal compliance, fairness, and explicit human sign-off before commitments.")


def enterprise_relationship_intelligence() -> str:
    payload = _safe_json(STRATEGIC_GOVERNANCE_DIR / "relationship_intelligence.json", {})
    accounts = payload.get("accounts", []) if isinstance(payload, dict) else []
    mapped = [item for item in accounts if isinstance(item, dict) and bool(item.get("mapped", False))]
    at_risk = [item for item in accounts if isinstance(item, dict) and item.get("status") == "at-risk"]
    return _overview("ENTERPRISE RELATIONSHIP INTELLIGENCE - PHASE 753", "relationship-intelligence overview", [f"Accounts tracked: {len(accounts)}", f"Mapped accounts: {len(mapped)}", f"At-risk accounts: {len(at_risk)}"], "Guardrail: relationship intelligence should preserve privacy, relevance, and respectful engagement before action.")


def ai_board_member_assistant() -> str:
    payload = _safe_json(STRATEGIC_GOVERNANCE_DIR / "board_assistant.json", {})
    briefs = payload.get("briefs", []) if isinstance(payload, dict) else []
    reviewed = [item for item in briefs if isinstance(item, dict) and bool(item.get("reviewed", False))]
    strategic = [item for item in briefs if isinstance(item, dict) and bool(item.get("strategic", False))]
    return _overview("AI BOARD MEMBER ASSISTANT - PHASE 754", "board-assistant overview", [f"Briefs tracked: {len(briefs)}", f"Reviewed briefs: {len(reviewed)}", f"Strategic briefs: {len(strategic)}"], "Guardrail: board assistance should remain advisory, evidence-backed, and subordinate to human fiduciary duties.")


def autonomous_operational_restructuring() -> str:
    payload = _safe_json(STRATEGIC_GOVERNANCE_DIR / "operational_restructuring.json", {})
    plans = payload.get("plans", []) if isinstance(payload, dict) else []
    modeled = [item for item in plans if isinstance(item, dict) and bool(item.get("modeled", False))]
    approved = [item for item in plans if isinstance(item, dict) and bool(item.get("approved", False))]
    return _overview("AUTONOMOUS OPERATIONAL RESTRUCTURING - PHASE 755", "operational-restructuring overview", [f"Plans tracked: {len(plans)}", f"Modeled plans: {len(modeled)}", f"Approved plans: {len(approved)}"], "Guardrail: restructuring guidance should preserve labor impact review, transparency, and human approval before operational changes.")


def ai_crisis_management_system() -> str:
    payload = _safe_json(STRATEGIC_GOVERNANCE_DIR / "crisis_management.json", {})
    incidents = payload.get("incidents", []) if isinstance(payload, dict) else []
    active = [item for item in incidents if isinstance(item, dict) and item.get("status") == "active"]
    escalated = [item for item in incidents if isinstance(item, dict) and bool(item.get("escalated", False))]
    return _overview("AI CRISIS MANAGEMENT SYSTEM - PHASE 756", "crisis-management overview", [f"Incidents tracked: {len(incidents)}", f"Active incidents: {len(active)}", f"Escalated incidents: {len(escalated)}"], "Guardrail: crisis management should preserve human command authority, clear escalation, and verified facts before intervention.")


def reputation_crisis_simulator() -> str:
    payload = _safe_json(STRATEGIC_GOVERNANCE_DIR / "reputation_crisis.json", {})
    scenarios = payload.get("scenarios", []) if isinstance(payload, dict) else []
    stressed = [item for item in scenarios if isinstance(item, dict) and item.get("severity") == "high"]
    rehearsed = [item for item in scenarios if isinstance(item, dict) and bool(item.get("rehearsed", False))]
    return _overview("REPUTATION CRISIS SIMULATOR - PHASE 757", "reputation-crisis overview", [f"Scenarios tracked: {len(scenarios)}", f"High-severity scenarios: {len(stressed)}", f"Rehearsed scenarios: {len(rehearsed)}"], "Guardrail: reputation simulations should preserve factual grounding and avoid manipulative or deceptive response patterns.")


def autonomous_diplomacy_engine() -> str:
    payload = _safe_json(STRATEGIC_GOVERNANCE_DIR / "autonomous_diplomacy.json", {})
    dialogues = payload.get("dialogues", []) if isinstance(payload, dict) else []
    mediated = [item for item in dialogues if isinstance(item, dict) and bool(item.get("mediated", False))]
    sensitive = [item for item in dialogues if isinstance(item, dict) and bool(item.get("sensitive", False))]
    return _overview("AUTONOMOUS DIPLOMACY ENGINE - PHASE 758", "autonomous-diplomacy overview", [f"Dialogues tracked: {len(dialogues)}", f"Mediated dialogues: {len(mediated)}", f"Sensitive dialogues: {len(sensitive)}"], "Guardrail: diplomatic support should remain human-led, accountable, and conflict-sensitive before public or state-facing use.")


def geopolitical_simulation_framework() -> str:
    payload = _safe_json(STRATEGIC_GOVERNANCE_DIR / "geopolitical_simulation.json", {})
    regions = payload.get("regions", []) if isinstance(payload, dict) else []
    modeled = [item for item in regions if isinstance(item, dict) and bool(item.get("modeled", False))]
    volatile = [item for item in regions if isinstance(item, dict) and item.get("risk") == "volatile"]
    return _overview("GEOPOLITICAL SIMULATION FRAMEWORK - PHASE 759", "geopolitical-simulation overview", [f"Regions tracked: {len(regions)}", f"Modeled regions: {len(modeled)}", f"Volatile regions: {len(volatile)}"], "Guardrail: geopolitical simulations should preserve uncertainty, non-escalation, and explicit human review before strategic use.")


def strategic_resource_allocation_ai() -> str:
    payload = _safe_json(STRATEGIC_GOVERNANCE_DIR / "resource_allocation.json", {})
    allocations = payload.get("allocations", []) if isinstance(payload, dict) else []
    optimized = [item for item in allocations if isinstance(item, dict) and bool(item.get("optimized", False))]
    constrained = [item for item in allocations if isinstance(item, dict) and bool(item.get("constrained", False))]
    return _overview("STRATEGIC RESOURCE ALLOCATION AI - PHASE 760", "resource-allocation overview", [f"Allocations tracked: {len(allocations)}", f"Optimized allocations: {len(optimized)}", f"Constrained allocations: {len(constrained)}"], "Guardrail: strategic allocation should preserve equity, mission intent, and explainability before deployment.")
