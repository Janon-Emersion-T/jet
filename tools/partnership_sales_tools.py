from __future__ import annotations

import json
from pathlib import Path


PARTNERSHIP_SALES_DIR = Path("storage/partnership_sales")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(PARTNERSHIP_SALES_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def podcast_workflow_assistant() -> str:
    return _render("PODCAST WORKFLOW ASSISTANT - PHASE 1571", "podcast-workflow overview", "podcast_workflow.json", "episode_workflows", "ready", "blocked", "Episode workflows tracked", "Ready workflows", "Blocked workflows", "Guardrail: podcast workflow planning should preserve attribution, release consent, and clear editorial review steps.")


def newsletter_intelligence_engine() -> str:
    return _render("NEWSLETTER INTELLIGENCE ENGINE - PHASE 1572", "newsletter-intelligence overview", "newsletter_intelligence.json", "newsletter_issues", "engaging", "ignored", "Newsletter issues tracked", "Engaging issues", "Ignored issues", "Guardrail: newsletter analysis should preserve subscriber trust, consent-based distribution, and avoid manipulative subject-line tactics.")


def community_building_assistant() -> str:
    return _render("COMMUNITY-BUILDING ASSISTANT - PHASE 1573", "community-building overview", "community_building_assistant.json", "community_loops", "healthy", "stalled", "Community loops tracked", "Healthy loops", "Stalled loops", "Guardrail: community strategy should preserve moderation fairness, member safety, and genuine value over vanity growth.")


def partnership_discovery_ai() -> str:
    return _render("PARTNERSHIP DISCOVERY AI - PHASE 1574", "partnership-discovery overview", "partnership_discovery.json", "partner_candidates", "aligned", "weak-fit", "Partner candidates tracked", "Aligned candidates", "Weak-fit candidates", "Guardrail: partnership discovery should preserve brand fit, explicit mutual benefit, and conflict-of-interest visibility.")


def tender_opportunity_detector() -> str:
    return _render("TENDER OPPORTUNITY DETECTOR - PHASE 1575", "tender-opportunity overview", "tender_opportunity_detector.json", "tender_leads", "eligible", "mismatched", "Tender leads tracked", "Eligible leads", "Mismatched leads", "Guardrail: tender detection should preserve qualification clarity and avoid presenting uncertain fit as a sure opportunity.")


def government_proposal_assistant() -> str:
    return _render("GOVERNMENT PROPOSAL ASSISTANT - PHASE 1576", "government-proposal overview", "government_proposal_assistant.json", "proposal_sections", "compliant", "missing", "Proposal sections tracked", "Compliant sections", "Missing sections", "Guardrail: proposal drafting should preserve factual accuracy, requirement traceability, and explicit human review for compliance claims.")


def enterprise_sales_enablement_brain() -> str:
    return _render("ENTERPRISE SALES ENABLEMENT BRAIN - PHASE 1577", "enterprise-sales overview", "enterprise_sales_enablement.json", "sales_assets", "useful", "weak", "Sales assets tracked", "Useful assets", "Weak assets", "Guardrail: sales enablement should preserve truthful positioning, accurate feature claims, and context for buyer objections.")


def competitive_positioning_engine() -> str:
    return _render("COMPETITIVE POSITIONING ENGINE - PHASE 1578", "competitive-positioning overview", "competitive_positioning.json", "positioning_angles", "distinct", "blurry", "Positioning angles tracked", "Distinct angles", "Blurry angles", "Guardrail: positioning analysis should preserve factual competitor comparisons and avoid unsupported disparagement.")


def pricing_psychology_analyzer() -> str:
    return _render("PRICING PSYCHOLOGY ANALYZER - PHASE 1579", "pricing-psychology overview", "pricing_psychology.json", "pricing_tests", "clear", "confusing", "Pricing tests tracked", "Clear tests", "Confusing tests", "Guardrail: pricing psychology should preserve customer clarity, fair disclosure, and avoid exploitative dark-pattern pricing.")


def dynamic_service_packaging_engine() -> str:
    return _render("DYNAMIC SERVICE PACKAGING ENGINE - PHASE 1580", "service-packaging overview", "service_packaging_engine.json", "service_packages", "coherent", "messy", "Service packages tracked", "Coherent packages", "Messy packages", "Guardrail: service packaging should preserve scope clarity, delivery realism, and explicit separation between options and promises.")
