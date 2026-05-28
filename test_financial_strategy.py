import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.financial_strategy_tools import (
    business_intelligence_dashboard,
    crypto_monitoring_assistant,
    investment_analysis_assistant,
    personal_finance_advisor,
)


class FinancialStrategyTests(unittest.TestCase):
    def test_finance_investment_and_crypto_render(self):
        with tempfile.TemporaryDirectory() as directory:
            finance_dir = Path(directory)
            (finance_dir / "budget.json").write_text(
                json.dumps({"monthly_income": 5000, "monthly_expenses": 3200}),
                encoding="utf-8",
            )
            (finance_dir / "portfolio.json").write_text(
                json.dumps({"positions": [{"symbol": "VOO", "cost_basis": 1000, "market_value": 1150}]}),
                encoding="utf-8",
            )
            (finance_dir / "crypto.json").write_text(
                json.dumps({"assets": [{"symbol": "BTC", "alert": True}]}),
                encoding="utf-8",
            )
            with patch("tools.financial_strategy_tools.FINANCE_DIR", finance_dir), \
                    patch.dict(os.environ, {"CRYPTO_WALLET_ADDRESS": "wallet-123"}, clear=False):
                finance = personal_finance_advisor()
                investment = investment_analysis_assistant()
                crypto = crypto_monitoring_assistant()
        self.assertIn("Monthly net: 1800.00", finance)
        self.assertIn("Tracked positions: 1", investment)
        self.assertIn("Unrealized P/L: 150.00", investment)
        self.assertIn("Alerting assets: 1", crypto)
        self.assertIn("Wallet address configured: YES", crypto)

    def test_business_dashboard_and_routes_cover_451_to_459(self):
        with tempfile.TemporaryDirectory() as directory:
            finance_dir = Path(directory)
            (finance_dir / "business_metrics.json").write_text(
                json.dumps({"monthly_revenue": 12000, "monthly_expenses": 7600, "active_customers": 84}),
                encoding="utf-8",
            )
            with patch("tools.financial_strategy_tools.FINANCE_DIR", finance_dir):
                dashboard = business_intelligence_dashboard()
        self.assertIn("Monthly revenue: 12000.00", dashboard)
        self.assertIn("Active customers: 84", dashboard)
        for phase in range(451, 460):
            result = handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help")
            self.assertIsNotNone(result, f"missing route for {phase}")


if __name__ == "__main__":
    unittest.main()
