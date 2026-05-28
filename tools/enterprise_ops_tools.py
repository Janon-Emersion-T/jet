from __future__ import annotations

import json
from pathlib import Path


OPS_DIR = Path("storage/enterprise_ops")


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


def legal_document_assistant() -> str:
    docs = _list_entries(OPS_DIR / "legal_documents.json", "documents")
    pending = [item for item in docs if isinstance(item, dict) and item.get("status", "draft") != "signed"]
    return "\n".join(
        [
            "LEGAL DOCUMENT ASSISTANT - PHASE 460",
            "Mode: document inventory review.",
            f"Tracked legal documents: {len(docs)}",
            f"Pending documents: {len(pending)}",
            "Safety: drafting and review guidance only; this is not a substitute for licensed legal advice.",
        ]
    )


def contract_analyzer() -> str:
    contracts = _list_entries(OPS_DIR / "contracts.json", "contracts")
    renewals = [
        item for item in contracts
        if isinstance(item, dict) and str(item.get("renewal_window", "")).strip()
    ]
    high_risk = [
        item for item in contracts
        if isinstance(item, dict) and str(item.get("risk", "")).lower() in {"high", "critical"}
    ]
    return "\n".join(
        [
            "CONTRACT ANALYZER - PHASE 461",
            "Mode: contract risk snapshot.",
            f"Tracked contracts: {len(contracts)}",
            f"Contracts with renewal windows: {len(renewals)}",
            f"High-risk contracts: {len(high_risk)}",
            "Focus: renewal dates, auto-renewal clauses, liability caps, exclusivity, termination, and payment terms.",
        ]
    )


def procurement_assistant() -> str:
    purchases = _list_entries(OPS_DIR / "procurement.json", "requests")
    awaiting = [item for item in purchases if isinstance(item, dict) and item.get("status", "pending") == "pending"]
    return "\n".join(
        [
            "PROCUREMENT ASSISTANT - PHASE 462",
            "Mode: purchasing queue review.",
            f"Tracked requests: {len(purchases)}",
            f"Pending approvals: {len(awaiting)}",
            "Workflow: requirement -> vendor comparison -> approval -> receipt -> reconciliation.",
        ]
    )


def inventory_forecasting_engine() -> str:
    items = _list_entries(OPS_DIR / "inventory.json", "items")
    low_stock = [
        item for item in items
        if isinstance(item, dict) and float(item.get("days_remaining", 999) or 999) <= 14
    ]
    return "\n".join(
        [
            "INVENTORY FORECASTING ENGINE - PHASE 463",
            "Mode: stock horizon review.",
            f"Tracked SKUs: {len(items)}",
            f"Low-runway SKUs: {len(low_stock)}",
            "Forecast signal: combine sell-through, lead time, seasonality, and safety stock before reordering.",
        ]
    )


def supply_chain_analyzer() -> str:
    vendors = _list_entries(OPS_DIR / "supply_chain.json", "vendors")
    delayed = [
        item for item in vendors
        if isinstance(item, dict) and str(item.get("status", "")).lower() in {"delayed", "at_risk"}
    ]
    single_points = [
        item for item in vendors
        if isinstance(item, dict) and bool(item.get("single_source", False))
    ]
    return "\n".join(
        [
            "SUPPLY CHAIN ANALYZER - PHASE 464",
            "Mode: supplier risk overview.",
            f"Tracked vendors: {len(vendors)}",
            f"Delayed or at-risk vendors: {len(delayed)}",
            f"Single-source dependencies: {len(single_points)}",
            "Focus: lead-time fragility, vendor concentration, geopolitical exposure, and alternate sourcing paths.",
        ]
    )


def pos_intelligence_engine() -> str:
    sales = _list_entries(OPS_DIR / "pos_sales.json", "sales")
    total_revenue = sum(float(item.get("revenue", 0) or 0) for item in sales if isinstance(item, dict))
    transactions = sum(int(item.get("transactions", 0) or 0) for item in sales if isinstance(item, dict))
    avg_ticket = total_revenue / transactions if transactions else 0.0
    return "\n".join(
        [
            "POS INTELLIGENCE ENGINE - PHASE 465",
            "Mode: point-of-sale snapshot.",
            f"Tracked sales periods: {len(sales)}",
            f"Total revenue: {total_revenue:.2f}",
            f"Average ticket: {avg_ticket:.2f}",
            "Suggested lens: ticket size, item mix, hourly peaks, margin by category, and refund patterns.",
        ]
    )
