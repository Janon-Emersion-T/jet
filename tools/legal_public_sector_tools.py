from __future__ import annotations

import json
from pathlib import Path


LEGAL_PUBLIC_DIR = Path("storage/legal_public_sector")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def ai_law_research_engine() -> str:
    payload = _safe_json(LEGAL_PUBLIC_DIR / "law_research.json", {})
    matters = payload.get("matters", []) if isinstance(payload, dict) else []
    sourced = [item for item in matters if isinstance(item, dict) and bool(item.get("sourced", False))]
    open_q = [item for item in matters if isinstance(item, dict) and bool(item.get("open_questions", False))]
    return _overview("AI LAW RESEARCH ENGINE - PHASE 638", "law-research overview", [f"Matters tracked: {len(matters)}", f"Sourced matters: {len(sourced)}", f"Matters with open questions: {len(open_q)}"], "Guardrail: legal research should remain source-grounded, jurisdiction-aware, and attorney-reviewable before it shapes advice.")


def case_law_intelligence_assistant() -> str:
    payload = _safe_json(LEGAL_PUBLIC_DIR / "case_law.json", {})
    cases = payload.get("cases", []) if isinstance(payload, dict) else []
    precedent = [item for item in cases if isinstance(item, dict) and bool(item.get("precedent", False))]
    conflicting = [item for item in cases if isinstance(item, dict) and bool(item.get("conflicting", False))]
    return _overview("CASE-LAW INTELLIGENCE ASSISTANT - PHASE 639", "case-law overview", [f"Cases tracked: {len(cases)}", f"Precedent cases: {len(precedent)}", f"Conflicting cases: {len(conflicting)}"], "Guardrail: case-law intelligence should preserve nuance, jurisdiction, and unresolved conflict rather than flattening precedent.")


def legal_risk_scoring_system() -> str:
    payload = _safe_json(LEGAL_PUBLIC_DIR / "legal_risk.json", {})
    items = payload.get("items", []) if isinstance(payload, dict) else []
    high = [item for item in items if isinstance(item, dict) and item.get("risk") == "high"]
    reviewed = [item for item in items if isinstance(item, dict) and bool(item.get("reviewed", False))]
    return _overview("LEGAL RISK SCORING SYSTEM - PHASE 640", "legal-risk overview", [f"Items tracked: {len(items)}", f"High-risk items: {len(high)}", f"Reviewed items: {len(reviewed)}"], "Guardrail: legal risk scoring should remain explainable, conservative, and subordinate to counsel review.")


def ai_court_document_analyzer() -> str:
    payload = _safe_json(LEGAL_PUBLIC_DIR / "court_documents.json", {})
    docs = payload.get("documents", []) if isinstance(payload, dict) else []
    parsed = [item for item in docs if isinstance(item, dict) and bool(item.get("parsed", False))]
    urgent = [item for item in docs if isinstance(item, dict) and item.get("priority") == "urgent"]
    return _overview("AI COURT DOCUMENT ANALYZER - PHASE 641", "court-document overview", [f"Documents tracked: {len(docs)}", f"Parsed documents: {len(parsed)}", f"Urgent documents: {len(urgent)}"], "Guardrail: court document analysis should preserve filing accuracy, deadlines, and attorney review.")


def autonomous_compliance_drafting() -> str:
    payload = _safe_json(LEGAL_PUBLIC_DIR / "compliance_drafting.json", {})
    drafts = payload.get("drafts", []) if isinstance(payload, dict) else []
    approved = [item for item in drafts if isinstance(item, dict) and item.get("status") == "approved"]
    exceptions = [item for item in drafts if isinstance(item, dict) and bool(item.get("exceptions", False))]
    return _overview("AUTONOMOUS COMPLIANCE DRAFTING - PHASE 642", "compliance-drafting overview", [f"Drafts tracked: {len(drafts)}", f"Approved drafts: {len(approved)}", f"Drafts with exceptions: {len(exceptions)}"], "Guardrail: compliance drafting should preserve evidence, approval boundaries, and legal review before adoption.")


def government_operations_intelligence() -> str:
    payload = _safe_json(LEGAL_PUBLIC_DIR / "government_ops.json", {})
    programs = payload.get("programs", []) if isinstance(payload, dict) else []
    active = [item for item in programs if isinstance(item, dict) and item.get("status") == "active"]
    delayed = [item for item in programs if isinstance(item, dict) and item.get("status") == "delayed"]
    return _overview("GOVERNMENT OPERATIONS INTELLIGENCE - PHASE 643", "government-operations overview", [f"Programs tracked: {len(programs)}", f"Active programs: {len(active)}", f"Delayed programs: {len(delayed)}"], "Guardrail: government operations intelligence should privilege accountability, public impact, and transparency before optimization.")


def public_service_ai_framework() -> str:
    payload = _safe_json(LEGAL_PUBLIC_DIR / "public_service.json", {})
    services = payload.get("services", []) if isinstance(payload, dict) else []
    digital = [item for item in services if isinstance(item, dict) and bool(item.get("digital", False))]
    backlog = [item for item in services if isinstance(item, dict) and item.get("status") == "backlog"]
    return _overview("PUBLIC SERVICE AI FRAMEWORK - PHASE 644", "public-service overview", [f"Services tracked: {len(services)}", f"Digital services: {len(digital)}", f"Backlogged services: {len(backlog)}"], "Guardrail: public-service automation should prioritize accessibility, fairness, and human recourse before rollout.")


def smart_city_orchestration() -> str:
    payload = _safe_json(LEGAL_PUBLIC_DIR / "smart_city.json", {})
    systems = payload.get("systems", []) if isinstance(payload, dict) else []
    integrated = [item for item in systems if isinstance(item, dict) and bool(item.get("integrated", False))]
    alerts = [item for item in systems if isinstance(item, dict) and bool(item.get("alert", False))]
    return _overview("SMART CITY ORCHESTRATION - PHASE 645", "smart-city overview", [f"Systems tracked: {len(systems)}", f"Integrated systems: {len(integrated)}", f"Alerting systems: {len(alerts)}"], "Guardrail: smart city coordination should respect civic accountability, safety, and privacy before cross-system automation.")


def urban_traffic_optimization() -> str:
    payload = _safe_json(LEGAL_PUBLIC_DIR / "urban_traffic.json", {})
    corridors = payload.get("corridors", []) if isinstance(payload, dict) else []
    optimized = [item for item in corridors if isinstance(item, dict) and bool(item.get("optimized", False))]
    congested = [item for item in corridors if isinstance(item, dict) and item.get("status") == "congested"]
    return _overview("URBAN TRAFFIC OPTIMIZATION - PHASE 646", "urban-traffic overview", [f"Corridors tracked: {len(corridors)}", f"Optimized corridors: {len(optimized)}", f"Congested corridors: {len(congested)}"], "Guardrail: traffic optimization should balance safety, equity, and emergency access before signal changes.")


def emergency_response_coordination() -> str:
    payload = _safe_json(LEGAL_PUBLIC_DIR / "emergency_response.json", {})
    incidents = payload.get("incidents", []) if isinstance(payload, dict) else []
    coordinated = [item for item in incidents if isinstance(item, dict) and bool(item.get("coordinated", False))]
    severe = [item for item in incidents if isinstance(item, dict) and item.get("severity") == "severe"]
    return _overview("EMERGENCY RESPONSE COORDINATION - PHASE 647", "emergency-response overview", [f"Incidents tracked: {len(incidents)}", f"Coordinated incidents: {len(coordinated)}", f"Severe incidents: {len(severe)}"], "Guardrail: emergency coordination should foreground life safety, chain of command, and verified situational awareness before dispatching resources.")


def disaster_simulation_engine() -> str:
    payload = _safe_json(LEGAL_PUBLIC_DIR / "disaster_simulation.json", {})
    simulations = payload.get("simulations", []) if isinstance(payload, dict) else []
    complete = [item for item in simulations if isinstance(item, dict) and item.get("status") == "complete"]
    high_impact = [item for item in simulations if isinstance(item, dict) and item.get("impact") == "high"]
    return _overview("DISASTER SIMULATION ENGINE - PHASE 648", "disaster-simulation overview", [f"Simulations tracked: {len(simulations)}", f"Completed simulations: {len(complete)}", f"High-impact simulations: {len(high_impact)}"], "Guardrail: disaster simulation should preserve scenario realism, uncertainty, and operator review before planning responses.")


def autonomous_rescue_planning() -> str:
    payload = _safe_json(LEGAL_PUBLIC_DIR / "rescue_planning.json", {})
    plans = payload.get("plans", []) if isinstance(payload, dict) else []
    approved = [item for item in plans if isinstance(item, dict) and item.get("status") == "approved"]
    time_critical = [item for item in plans if isinstance(item, dict) and bool(item.get("time_critical", False))]
    return _overview("AUTONOMOUS RESCUE PLANNING - PHASE 649", "rescue-planning overview", [f"Plans tracked: {len(plans)}", f"Approved plans: {len(approved)}", f"Time-critical plans: {len(time_critical)}"], "Guardrail: rescue planning should prioritize responder safety, verified routes, and command oversight before action.")


def ai_defense_simulation_layer() -> str:
    payload = _safe_json(LEGAL_PUBLIC_DIR / "defense_simulation.json", {})
    exercises = payload.get("exercises", []) if isinstance(payload, dict) else []
    simulated = [item for item in exercises if isinstance(item, dict) and bool(item.get("simulated", False))]
    bounded = [item for item in exercises if isinstance(item, dict) and bool(item.get("bounded", False))]
    return _overview("AI DEFENSE SIMULATION LAYER - PHASE 650", "defense-simulation overview", [f"Exercises tracked: {len(exercises)}", f"Simulated exercises: {len(simulated)}", f"Bounded exercises: {len(bounded)}"], "Guardrail: defense simulation should remain policy-bounded, approval-gated, and clearly separated from live action.")
