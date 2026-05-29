from __future__ import annotations

import json
from pathlib import Path


CX_DIR = Path("storage/customer_experience")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _list_entries(path: Path, key: str):
    payload = _safe_json(path, {key: []})
    if isinstance(payload, dict) and isinstance(payload.get(key), list):
        return payload[key]
    if isinstance(payload, list):
        return payload
    return []


def e_commerce_optimization_engine() -> str:
    metrics = _safe_json(CX_DIR / "ecommerce.json", {})
    conversion = float(metrics.get("conversion_rate", 0) or 0) if isinstance(metrics, dict) else 0.0
    cart_abandonment = float(metrics.get("cart_abandonment_rate", 0) or 0) if isinstance(metrics, dict) else 0.0
    aov = float(metrics.get("average_order_value", 0) or 0) if isinstance(metrics, dict) else 0.0
    return "\n".join(
        [
            "E-COMMERCE OPTIMIZATION ENGINE - PHASE 466",
            "Mode: local commerce metrics review.",
            f"Conversion rate: {conversion:.2f}%",
            f"Cart abandonment: {cart_abandonment:.2f}%",
            f"Average order value: {aov:.2f}",
            "Focus: product-page clarity, checkout friction, trust proof, order economics, and recovery loops.",
        ]
    )


def customer_sentiment_analyzer() -> str:
    entries = _list_entries(CX_DIR / "sentiment.json", "entries")
    positives = sum(1 for item in entries if isinstance(item, dict) and item.get("label") == "positive")
    negatives = sum(1 for item in entries if isinstance(item, dict) and item.get("label") == "negative")
    neutrals = len(entries) - positives - negatives
    return "\n".join(
        [
            "CUSTOMER SENTIMENT ANALYZER - PHASE 467",
            "Mode: customer-language sentiment snapshot.",
            f"Entries analyzed: {len(entries)}",
            f"Positive: {positives}",
            f"Neutral: {neutrals}",
            f"Negative: {negatives}",
            "Guidance: separate loud complaints from recurring friction themes before escalating product or service changes.",
        ]
    )


def review_monitoring_assistant() -> str:
    reviews = _list_entries(CX_DIR / "reviews.json", "reviews")
    low = [item for item in reviews if isinstance(item, dict) and float(item.get("rating", 5) or 5) <= 2]
    avg = (
        sum(float(item.get("rating", 0) or 0) for item in reviews if isinstance(item, dict)) / len(reviews)
        if reviews
        else 0.0
    )
    return "\n".join(
        [
            "REVIEW MONITORING ASSISTANT - PHASE 468",
            "Mode: review health overview.",
            f"Reviews tracked: {len(reviews)}",
            f"Average rating: {avg:.2f}",
            f"Low-rating reviews: {len(low)}",
            "Reminder: respond with empathy, extract patterns, and avoid treating isolated comments as the whole market.",
        ]
    )


def reputation_management_engine() -> str:
    incidents = _list_entries(CX_DIR / "reputation.json", "incidents")
    open_incidents = [item for item in incidents if isinstance(item, dict) and item.get("status", "open") != "resolved"]
    channels = sorted(
        {
            str(item.get("channel", "unknown"))
            for item in incidents
            if isinstance(item, dict) and item.get("channel")
        }
    )
    return "\n".join(
        [
            "REPUTATION MANAGEMENT ENGINE - PHASE 469",
            "Mode: reputation incident snapshot.",
            f"Tracked incidents: {len(incidents)}",
            f"Open incidents: {len(open_incidents)}",
            f"Channels: {', '.join(channels) if channels else 'none'}",
            "Approach: acknowledge fast, correct facts carefully, and keep an owner on each unresolved reputational risk.",
        ]
    )


def public_relations_assistant() -> str:
    campaigns = _list_entries(CX_DIR / "pr_campaigns.json", "campaigns")
    upcoming = [item for item in campaigns if isinstance(item, dict) and item.get("status", "draft") in {"draft", "scheduled"}]
    return "\n".join(
        [
            "PUBLIC RELATIONS ASSISTANT - PHASE 470",
            "Mode: PR planning overview.",
            f"Tracked campaigns: {len(campaigns)}",
            f"Upcoming campaigns: {len(upcoming)}",
            "Framework: angle, audience, proof, spokesperson, risk review, and follow-up narrative.",
        ]
    )
