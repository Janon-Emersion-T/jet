from __future__ import annotations

import json
from pathlib import Path


MARKETING_PERFORMANCE_DIR = Path("storage/marketing_performance")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(MARKETING_PERFORMANCE_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def marketing_roi_brain() -> str:
    return _render("MARKETING ROI BRAIN - PHASE 1551", "marketing-roi overview", "marketing_roi.json", "campaigns", "profitable", "wasteful", "Campaigns tracked", "Profitable campaigns", "Wasteful campaigns", "Guardrail: ROI analysis should preserve attribution caveats, cost transparency, and channel-specific uncertainty before budget changes.")


def seo_revenue_attribution() -> str:
    return _render("SEO REVENUE ATTRIBUTION - PHASE 1552", "seo-revenue overview", "seo_revenue_attribution.json", "seo_paths", "attributed", "uncertain", "SEO paths tracked", "Attributed paths", "Uncertain paths", "Guardrail: SEO attribution should preserve lag awareness, assisted-conversion nuance, and transparent assumptions before conclusions.")


def content_to_lead_intelligence() -> str:
    return _render("CONTENT-TO-LEAD INTELLIGENCE - PHASE 1553", "content-to-lead overview", "content_to_lead.json", "content_assets", "converting", "ignored", "Content assets tracked", "Converting assets", "Ignored assets", "Guardrail: content intelligence should preserve audience context, source provenance, and avoid overfitting to short-term lead spikes.")


def social_media_performance_predictor() -> str:
    return _render("SOCIAL MEDIA PERFORMANCE PREDICTOR - PHASE 1554", "social-performance overview", "social_performance_predictor.json", "social_posts", "outperforming", "underperforming", "Social posts tracked", "Outperforming posts", "Underperforming posts", "Guardrail: social performance prediction should preserve platform volatility caveats and avoid overstating confidence from sparse samples.")


def campaign_budget_optimizer() -> str:
    return _render("CAMPAIGN BUDGET OPTIMIZER - PHASE 1555", "campaign-budget overview", "campaign_budget_optimizer.json", "budget_routes", "balanced", "overspent", "Budget routes tracked", "Balanced routes", "Overspent routes", "Guardrail: budget optimization should preserve channel diversity, experiment headroom, and transparent spend assumptions.")


def ad_creative_testing_engine() -> str:
    return _render("AD CREATIVE TESTING ENGINE - PHASE 1556", "creative-testing overview", "ad_creative_testing.json", "creative_tests", "validated", "inconclusive", "Creative tests tracked", "Validated tests", "Inconclusive tests", "Guardrail: creative testing should preserve sample-size caution, audience segmentation context, and visible confidence bounds.")


def landing_page_psychology_analyzer() -> str:
    return _render("LANDING PAGE PSYCHOLOGY ANALYZER - PHASE 1557", "landing-page-psychology overview", "landing_page_psychology.json", "page_reviews", "persuasive", "confusing", "Page reviews tracked", "Persuasive pages", "Confusing pages", "Guardrail: psychology analysis should preserve user dignity, avoid manipulative dark patterns, and keep rationale reviewable.")


def conversion_friction_detector() -> str:
    return _render("CONVERSION FRICTION DETECTOR - PHASE 1558", "conversion-friction overview", "conversion_friction.json", "conversion_steps", "smooth", "frictional", "Conversion steps tracked", "Smooth steps", "Frictional steps", "Guardrail: friction detection should preserve accessibility, explicit evidence, and distinguish signal from anecdotal drop-off.")


def user_journey_simulator() -> str:
    return _render("USER JOURNEY SIMULATOR - PHASE 1559", "user-journey overview", "user_journey_simulator.json", "journeys", "coherent", "broken", "Journeys tracked", "Coherent journeys", "Broken journeys", "Guardrail: journey simulation should preserve real-user variability, not assume uniform intent, and surface weak inference points.")


def trust_signal_optimizer() -> str:
    return _render("TRUST SIGNAL OPTIMIZER - PHASE 1560", "trust-signal overview", "trust_signal_optimizer.json", "trust_signals", "credible", "weak", "Trust signals tracked", "Credible signals", "Weak signals", "Guardrail: trust optimization should preserve authenticity, factual accuracy, and avoid fabricated authority cues.")
