from __future__ import annotations

import json
import os
from pathlib import Path


FINANCE_DIR = Path("storage/finance")


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


def personal_finance_advisor() -> str:
    budget = _safe_json(FINANCE_DIR / "budget.json", {})
    income = float(budget.get("monthly_income", 0) or 0) if isinstance(budget, dict) else 0.0
    expenses = float(budget.get("monthly_expenses", 0) or 0) if isinstance(budget, dict) else 0.0
    savings = income - expenses
    return "\n".join(
        [
            "PERSONAL FINANCE ADVISOR - PHASE 451",
            "Mode: local budgeting snapshot.",
            f"Monthly income: {income:.2f}",
            f"Monthly expenses: {expenses:.2f}",
            f"Monthly net: {savings:.2f}",
            "Guidance: protect runway first, then debt reduction, emergency savings, and long-term allocation.",
        ]
    )


def investment_analysis_assistant() -> str:
    portfolio = _list_entries(FINANCE_DIR / "portfolio.json", "positions")
    total_cost = sum(float(item.get("cost_basis", 0) or 0) for item in portfolio if isinstance(item, dict))
    total_value = sum(float(item.get("market_value", 0) or 0) for item in portfolio if isinstance(item, dict))
    pnl = total_value - total_cost
    return "\n".join(
        [
            "INVESTMENT ANALYSIS ASSISTANT - PHASE 452",
            "Mode: portfolio summary review.",
            f"Tracked positions: {len(portfolio)}",
            f"Cost basis total: {total_cost:.2f}",
            f"Market value total: {total_value:.2f}",
            f"Unrealized P/L: {pnl:.2f}",
            "Safety: advisory only; no trade, allocation, or brokerage action was executed.",
        ]
    )


def trading_strategy_sandbox() -> str:
    strategies = _list_entries(FINANCE_DIR / "strategies.json", "strategies")
    enabled = [item for item in strategies if isinstance(item, dict) and item.get("enabled", False)]
    return "\n".join(
        [
            "TRADING STRATEGY SANDBOX - PHASE 453",
            "Mode: paper-strategy review only.",
            f"Stored strategies: {len(strategies)}",
            f"Enabled simulations: {len(enabled)}",
            "Policy: keep this sandbox non-custodial, backtest-aware, and approval-gated before any live execution.",
        ]
    )


def market_data_analyzer() -> str:
    data = _list_entries(FINANCE_DIR / "market_data.json", "assets")
    movers = sorted(
        [item for item in data if isinstance(item, dict)],
        key=lambda item: abs(float(item.get("change_percent", 0) or 0)),
        reverse=True,
    )
    top = movers[0] if movers else {}
    top_name = top.get("symbol", "none") if isinstance(top, dict) else "none"
    top_change = float(top.get("change_percent", 0) or 0) if isinstance(top, dict) else 0.0
    return "\n".join(
        [
            "MARKET DATA ANALYZER - PHASE 454",
            "Mode: local market snapshot.",
            f"Tracked assets: {len(data)}",
            f"Largest mover: {top_name} ({top_change:.2f}%)",
            "Guidance: separate signal collection from decision-making and record source freshness with each snapshot.",
        ]
    )


def crypto_monitoring_assistant() -> str:
    assets = _list_entries(FINANCE_DIR / "crypto.json", "assets")
    alerts = [item for item in assets if isinstance(item, dict) and item.get("alert", False)]
    wallet_connected = bool(os.getenv("CRYPTO_WALLET_ADDRESS", "").strip())
    return "\n".join(
        [
            "CRYPTO MONITORING ASSISTANT - PHASE 455",
            "Mode: read-only crypto watchlist review.",
            f"Tracked crypto assets: {len(assets)}",
            f"Alerting assets: {len(alerts)}",
            f"Wallet address configured: {'YES' if wallet_connected else 'NO'}",
            "Safety: no wallet, exchange, or on-chain action was executed.",
        ]
    )


def business_intelligence_dashboard() -> str:
    metrics = _safe_json(FINANCE_DIR / "business_metrics.json", {})
    revenue = float(metrics.get("monthly_revenue", 0) or 0) if isinstance(metrics, dict) else 0.0
    expenses = float(metrics.get("monthly_expenses", 0) or 0) if isinstance(metrics, dict) else 0.0
    customers = int(metrics.get("active_customers", 0) or 0) if isinstance(metrics, dict) else 0
    return "\n".join(
        [
            "BUSINESS INTELLIGENCE DASHBOARD - PHASE 456",
            "Mode: business KPI snapshot.",
            f"Monthly revenue: {revenue:.2f}",
            f"Monthly expenses: {expenses:.2f}",
            f"Active customers: {customers}",
            "Dashboard loop: growth, margin, retention, pipeline, delivery health, and cash timing.",
        ]
    )


def executive_decision_assistant() -> str:
    decisions = _list_entries(FINANCE_DIR / "decisions.json", "decisions")
    open_items = [item for item in decisions if isinstance(item, dict) and item.get("status", "open") != "done"]
    priorities = [str(item.get("title", "untitled")) for item in open_items[:3] if isinstance(item, dict)]
    return "\n".join(
        [
            "EXECUTIVE DECISION ASSISTANT - PHASE 457",
            "Mode: executive decision queue review.",
            f"Open decisions: {len(open_items)}",
            f"Top decisions: {', '.join(priorities) if priorities else 'none'}",
            "Framework: clarify objective, downside, cost, reversibility, owner, and timing before committing.",
        ]
    )


def company_operations_ai() -> str:
    ops = _safe_json(FINANCE_DIR / "operations.json", {})
    teams = int(ops.get("teams", 0) or 0) if isinstance(ops, dict) else 0
    workflows = int(ops.get("critical_workflows", 0) or 0) if isinstance(ops, dict) else 0
    blockers = int(ops.get("active_blockers", 0) or 0) if isinstance(ops, dict) else 0
    return "\n".join(
        [
            "COMPANY OPERATIONS AI - PHASE 458",
            "Mode: operational control snapshot.",
            f"Teams tracked: {teams}",
            f"Critical workflows: {workflows}",
            f"Active blockers: {blockers}",
            "Recommended loop: inspect bottlenecks, surface owners, and escalate only the blockers that threaten delivery or cash flow.",
        ]
    )


def multi_company_management_ai() -> str:
    companies = _list_entries(FINANCE_DIR / "companies.json", "companies")
    active = [item for item in companies if isinstance(item, dict) and item.get("active", True)]
    names = [str(item.get("name", "unnamed")) for item in active[:4] if isinstance(item, dict)]
    return "\n".join(
        [
            "MULTI-COMPANY MANAGEMENT AI - PHASE 459",
            "Mode: multi-entity overview.",
            f"Tracked companies: {len(companies)}",
            f"Active companies: {len(active)}",
            f"Preview: {', '.join(names) if names else 'none'}",
            "Governance note: keep entity-level metrics, approvals, and obligations separated before any shared automation grows teeth.",
        ]
    )
