from __future__ import annotations

import json
from pathlib import Path


BRAND_CONTENT_GROWTH_DIR = Path("storage/brand_content_growth")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(BRAND_CONTENT_GROWTH_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def brand_voice_consistency_engine() -> str:
    return _render("BRAND VOICE CONSISTENCY ENGINE - PHASE 1561", "brand-voice overview", "brand_voice_consistency.json", "brand_assets", "consistent", "drifting", "Brand assets tracked", "Consistent assets", "Drifting assets", "Guardrail: voice consistency should preserve audience fit, factual accuracy, and room for intentional experimentation.")


def multi_brand_content_governor() -> str:
    return _render("MULTI-BRAND CONTENT GOVERNOR - PHASE 1562", "multi-brand-content overview", "multi_brand_content.json", "brand_streams", "aligned", "crossed", "Brand streams tracked", "Aligned streams", "Crossed streams", "Guardrail: multi-brand governance should preserve brand separation, approval boundaries, and traceable ownership of content.")


def automated_case_study_miner() -> str:
    return _render("AUTOMATED CASE-STUDY MINER - PHASE 1563", "case-study-mining overview", "case_study_miner.json", "project_highlights", "usable", "thin", "Project highlights tracked", "Usable highlights", "Thin highlights", "Guardrail: case-study mining should preserve client confidentiality, factual grounding, and explicit approval before publication.")


def testimonial_extraction_assistant() -> str:
    return _render("TESTIMONIAL EXTRACTION ASSISTANT - PHASE 1564", "testimonial-extraction overview", "testimonial_extraction.json", "testimonial_candidates", "quotable", "unclear", "Testimonial candidates tracked", "Quotable candidates", "Unclear candidates", "Guardrail: testimonial extraction should preserve quote accuracy, consent, and context around praise or critique.")


def reputation_moat_builder() -> str:
    return _render("REPUTATION MOAT BUILDER - PHASE 1565", "reputation-moat overview", "reputation_moat_builder.json", "reputation_assets", "defensible", "fragile", "Reputation assets tracked", "Defensible assets", "Fragile assets", "Guardrail: reputation strategy should preserve authenticity, avoid deceptive amplification, and keep source evidence inspectable.")


def thought_leadership_planner() -> str:
    return _render("THOUGHT-LEADERSHIP PLANNER - PHASE 1566", "thought-leadership overview", "thought_leadership_planner.json", "content_themes", "distinctive", "generic", "Content themes tracked", "Distinctive themes", "Generic themes", "Guardrail: thought-leadership planning should preserve originality, source credit, and avoid confident claims without evidence.")


def founder_personal_brand_engine() -> str:
    return _render("FOUNDER PERSONAL BRAND ENGINE - PHASE 1567", "founder-brand overview", "founder_personal_brand.json", "brand_moves", "authentic", "performative", "Brand moves tracked", "Authentic moves", "Performative moves", "Guardrail: founder branding should preserve authenticity, privacy boundaries, and accurate public positioning.")


def linkedin_authority_system() -> str:
    return _render("LINKEDIN AUTHORITY SYSTEM - PHASE 1568", "linkedin-authority overview", "linkedin_authority_system.json", "linkedin_posts", "authoritative", "forgettable", "LinkedIn posts tracked", "Authoritative posts", "Forgettable posts", "Guardrail: authority building should preserve substance, truthfulness, and avoid engagement bait disguised as expertise.")


def youtube_strategy_assistant() -> str:
    return _render("YOUTUBE STRATEGY ASSISTANT - PHASE 1569", "youtube-strategy overview", "youtube_strategy_assistant.json", "video_plans", "clear", "weak", "Video plans tracked", "Clear plans", "Weak plans", "Guardrail: YouTube strategy should preserve audience value, source accuracy, and avoid optimizing for retention at the expense of trust.")


def short_form_video_factory() -> str:
    return _render("SHORT-FORM VIDEO FACTORY - PHASE 1570", "short-form-video overview", "short_form_video_factory.json", "video_batches", "publishable", "repetitive", "Video batches tracked", "Publishable batches", "Repetitive batches", "Guardrail: short-form production should preserve brand fit, factual integrity, and sustainable publishing cadence.")
