from __future__ import annotations

import json
from pathlib import Path


RETAIL_COMMAND_DIR = Path("storage/retail_command")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(RETAIL_COMMAND_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def product_recommendation_engine() -> str:
    return _render("PRODUCT RECOMMENDATION ENGINE - PHASE 1641", "product-recommendation overview", "product_recommendation_engine.json", "recommendation_sets", "relevant", "weak", "Recommendation sets tracked", "Relevant sets", "Weak sets", "Guardrail: recommendation analysis should preserve customer context, avoid manipulative upselling, and keep the rationale inspectable.")


def stock_reorder_predictor() -> str:
    return _render("STOCK REORDER PREDICTOR - PHASE 1642", "stock-reorder overview", "stock_reorder_predictor.json", "reorder_paths", "timely", "late", "Reorder paths tracked", "Timely reorders", "Late reorders", "Guardrail: reorder prediction should preserve lead-time uncertainty, supplier variance, and buffer stock assumptions.")


def demand_seasonality_analyzer() -> str:
    return _render("DEMAND SEASONALITY ANALYZER - PHASE 1643", "demand-seasonality overview", "demand_seasonality_analyzer.json", "seasonality_models", "grounded", "noisy", "Seasonality models tracked", "Grounded models", "Noisy models", "Guardrail: seasonality analysis should preserve calendar context, promotion effects, and avoid overconfidence from thin history.")


def sales_margin_optimizer() -> str:
    return _render("SALES MARGIN OPTIMIZER - PHASE 1644", "sales-margin overview", "sales_margin_optimizer.json", "margin_paths", "healthy", "compressed", "Margin paths tracked", "Healthy margins", "Compressed margins", "Guardrail: margin optimization should preserve customer fairness, inventory realities, and transparent cost assumptions.")


def customer_segmentation_engine() -> str:
    return _render("CUSTOMER SEGMENTATION ENGINE - PHASE 1645", "customer-segmentation overview", "customer_segmentation_engine.json", "customer_segments", "actionable", "blurry", "Customer segments tracked", "Actionable segments", "Blurry segments", "Guardrail: segmentation should preserve privacy, avoid sensitive-inference overreach, and expose the logic behind each grouping.")


def loyalty_program_intelligence() -> str:
    return _render("LOYALTY PROGRAM INTELLIGENCE - PHASE 1646", "loyalty-program overview", "loyalty_program_intelligence.json", "loyalty_paths", "engaging", "stagnant", "Loyalty paths tracked", "Engaging paths", "Stagnant paths", "Guardrail: loyalty optimization should preserve customer trust, reward clarity, and avoid exploitative gamification.")


def discount_abuse_detector() -> str:
    return _render("DISCOUNT ABUSE DETECTOR - PHASE 1647", "discount-abuse overview", "discount_abuse_detector.json", "discount_events", "legitimate", "abusive", "Discount events tracked", "Legitimate events", "Abusive events", "Guardrail: discount abuse detection should preserve explainability and require evidence before punitive action.")


def fraud_risk_scoring() -> str:
    return _render("FRAUD-RISK SCORING - PHASE 1648", "fraud-risk overview", "fraud_risk_scoring.json", "risk_events", "low-risk", "high-risk", "Risk events tracked", "Low-risk events", "High-risk events", "Guardrail: fraud scoring should preserve appealability, avoid proxy bias, and surface the evidence behind elevated risk.")


def returns_pattern_analyzer() -> str:
    return _render("RETURNS PATTERN ANALYZER - PHASE 1649", "returns-pattern overview", "returns_pattern_analyzer.json", "return_patterns", "routine", "spiking", "Return patterns tracked", "Routine patterns", "Spiking patterns", "Guardrail: returns analysis should preserve product/context nuance and avoid assuming misuse from aggregate return behavior alone.")


def retail_command_intelligence() -> str:
    return _render("RETAIL COMMAND INTELLIGENCE - PHASE 1650", "retail-command overview", "retail_command_intelligence.json", "retail_panels", "actionable", "fragmented", "Retail panels tracked", "Actionable panels", "Fragmented panels", "Guardrail: retail command summaries should preserve data provenance, store-level nuance, and visible uncertainty in recommendations.")
