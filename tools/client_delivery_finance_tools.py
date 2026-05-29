from __future__ import annotations

import json
from pathlib import Path


CLIENT_DELIVERY_FINANCE_DIR = Path("storage/client_delivery_finance")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(CLIENT_DELIVERY_FINANCE_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def saas_pricing_simulator() -> str:
    return _render("SAAS PRICING SIMULATOR - PHASE 1581", "saas-pricing overview", "saas_pricing_simulator.json", "pricing_scenarios", "viable", "fragile", "Pricing scenarios tracked", "Viable scenarios", "Fragile scenarios", "Guardrail: pricing simulation should preserve assumption visibility, margin realism, and customer fairness before recommendations.")


def productized_service_builder() -> str:
    return _render("PRODUCTIZED-SERVICE BUILDER - PHASE 1582", "productized-service overview", "productized_service_builder.json", "service_blueprints", "productized", "underspecified", "Service blueprints tracked", "Productized blueprints", "Underspecified blueprints", "Guardrail: productized service design should preserve scope clarity, fulfillment realism, and explicit exclusions.")


def white_label_product_manager() -> str:
    return _render("WHITE-LABEL PRODUCT MANAGER - PHASE 1583", "white-label-product overview", "white_label_product_manager.json", "white_label_streams", "coherent", "risky", "White-label streams tracked", "Coherent streams", "Risky streams", "Guardrail: white-label planning should preserve contractual clarity, client boundaries, and source-brand obligations.")


def marketplace_listing_optimizer() -> str:
    return _render("MARKETPLACE LISTING OPTIMIZER - PHASE 1584", "marketplace-listing overview", "marketplace_listing_optimizer.json", "listings", "optimized", "weak", "Listings tracked", "Optimized listings", "Weak listings", "Guardrail: listing optimization should preserve truthful claims, platform compliance, and avoid misleading urgency tactics.")


def affiliate_program_brain() -> str:
    return _render("AFFILIATE PROGRAM BRAIN - PHASE 1585", "affiliate-program overview", "affiliate_program_brain.json", "affiliate_routes", "healthy", "abusive", "Affiliate routes tracked", "Healthy routes", "Abusive routes", "Guardrail: affiliate planning should preserve disclosure compliance, partner fairness, and fraud visibility in incentive design.")


def referral_intelligence_system() -> str:
    return _render("REFERRAL INTELLIGENCE SYSTEM - PHASE 1586", "referral-intelligence overview", "referral_intelligence_system.json", "referral_loops", "productive", "weak", "Referral loops tracked", "Productive loops", "Weak loops", "Guardrail: referral intelligence should preserve customer trust, fair rewards, and transparent attribution rules.")


def client_onboarding_autopilot() -> str:
    return _render("CLIENT ONBOARDING AUTOPILOT - PHASE 1587", "client-onboarding overview", "client_onboarding_autopilot.json", "onboarding_flows", "smooth", "confusing", "Onboarding flows tracked", "Smooth flows", "Confusing flows", "Guardrail: onboarding automation should preserve consent, human escalation paths, and clear expectations around next steps.")


def client_requirement_workshop_assistant() -> str:
    return _render("CLIENT REQUIREMENT WORKSHOP ASSISTANT - PHASE 1588", "requirement-workshop overview", "requirement_workshop_assistant.json", "workshop_outputs", "clear", "ambiguous", "Workshop outputs tracked", "Clear outputs", "Ambiguous outputs", "Guardrail: requirement workshops should preserve stakeholder nuance, source wording, and explicit uncertainty where scope is unresolved.")


def meeting_to_sow_generator() -> str:
    return _render("MEETING-TO-SOW GENERATOR - PHASE 1589", "meeting-to-sow overview", "meeting_to_sow_generator.json", "sow_drafts", "usable", "incomplete", "SOW drafts tracked", "Usable drafts", "Incomplete drafts", "Guardrail: SOW generation should preserve contractual precision, meeting context, and mandatory human review before sending.")


def milestone_planner() -> str:
    return _render("MILESTONE PLANNER - PHASE 1590", "milestone-planning overview", "milestone_planner.json", "milestones", "realistic", "slipping", "Milestones tracked", "Realistic milestones", "Slipping milestones", "Guardrail: milestone planning should preserve delivery realism, dependency visibility, and team-capacity constraints.")
