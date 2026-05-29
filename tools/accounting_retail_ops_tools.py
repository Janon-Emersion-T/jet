from __future__ import annotations

import json
from pathlib import Path


ACCOUNTING_RETAIL_OPS_DIR = Path("storage/accounting_retail_ops")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(ACCOUNTING_RETAIL_OPS_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def accounting_rule_validator() -> str:
    return _render("ACCOUNTING RULE VALIDATOR - PHASE 1631", "accounting-rule overview", "accounting_rule_validator.json", "accounting_rules", "valid", "violating", "Accounting rules tracked", "Valid rules", "Violating rules", "Guardrail: accounting validation should preserve ledger evidence, jurisdiction caveats, and explicit separation between heuristic checks and formal accounting advice.")


def pos_transaction_intelligence() -> str:
    return _render("POS TRANSACTION INTELLIGENCE - PHASE 1632", "pos-transaction overview", "pos_transaction_intelligence.json", "transactions", "normal", "flagged", "Transactions tracked", "Normal transactions", "Flagged transactions", "Guardrail: POS analysis should preserve receipt evidence, cashier context, and avoid equating anomalies with fraud by default.")


def inventory_leakage_detector() -> str:
    return _render("INVENTORY LEAKAGE DETECTOR - PHASE 1633", "inventory-leakage overview", "inventory_leakage_detector.json", "inventory_movements", "accounted", "leaking", "Inventory movements tracked", "Accounted movements", "Leaking movements", "Guardrail: leakage detection should preserve reconciliation context and distinguish process gaps from confirmed loss.")


def warehouse_movement_predictor() -> str:
    return _render("WAREHOUSE MOVEMENT PREDICTOR - PHASE 1634", "warehouse-movement overview", "warehouse_movement_predictor.json", "movement_patterns", "predictable", "volatile", "Movement patterns tracked", "Predictable patterns", "Volatile patterns", "Guardrail: movement prediction should preserve seasonality context, supplier timing variance, and uncertainty around outliers.")


def supplier_reliability_scorer() -> str:
    return _render("SUPPLIER RELIABILITY SCORER - PHASE 1635", "supplier-reliability overview", "supplier_reliability_scorer.json", "supplier_profiles", "reliable", "fragile", "Supplier profiles tracked", "Reliable suppliers", "Fragile suppliers", "Guardrail: supplier scoring should preserve context, contract nuance, and avoid black-box rankings without explainable drivers.")


def purchase_order_optimizer() -> str:
    return _render("PURCHASE-ORDER OPTIMIZER - PHASE 1636", "purchase-order overview", "purchase_order_optimizer.json", "po_routes", "optimized", "wasteful", "PO routes tracked", "Optimized routes", "Wasteful routes", "Guardrail: PO optimization should preserve approval policy, inventory realism, and supplier constraints before recommendation.")


def barcode_workflow_assistant() -> str:
    return _render("BARCODE WORKFLOW ASSISTANT - PHASE 1637", "barcode-workflow overview", "barcode_workflow_assistant.json", "barcode_flows", "smooth", "blocked", "Barcode flows tracked", "Smooth flows", "Blocked flows", "Guardrail: barcode workflow guidance should preserve device compatibility, operator ergonomics, and explicit exception handling.")


def receipt_printing_diagnostics() -> str:
    return _render("RECEIPT-PRINTING DIAGNOSTICS - PHASE 1638", "receipt-printing overview", "receipt_printing_diagnostics.json", "printer_checks", "healthy", "failing", "Printer checks tracked", "Healthy checks", "Failing checks", "Guardrail: printing diagnostics should preserve device-specific context and avoid destructive reset guidance without confirmation.")


def e_commerce_checkout_analyzer() -> str:
    return _render("E-COMMERCE CHECKOUT ANALYZER - PHASE 1639", "checkout-analysis overview", "ecommerce_checkout_analyzer.json", "checkout_steps", "converting", "dropping", "Checkout steps tracked", "Converting steps", "Dropping steps", "Guardrail: checkout analysis should preserve accessibility, payment-provider nuance, and evidence for each suspected friction point.")


def cart_abandonment_intelligence() -> str:
    return _render("CART ABANDONMENT INTELLIGENCE - PHASE 1640", "cart-abandonment overview", "cart_abandonment_intelligence.json", "abandonment_signals", "recoverable", "lost", "Abandonment signals tracked", "Recoverable signals", "Lost signals", "Guardrail: abandonment analysis should preserve consent for remarketing, clear attribution assumptions, and non-manipulative recovery tactics.")
