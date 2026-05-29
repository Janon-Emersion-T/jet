import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.lkprofessionals_growth_tools import *


class LKProfessionalsGrowthToolsTests(unittest.TestCase):
    def test_lkprofessionals_growth_tools_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "company_ai_nervous_system.json": {"signal_routes": [{"connected": True, "siloed": True}, {"connected": False, "siloed": False}]},
                "lkprofessionals_operations_brain.json": {"operations_views": [{"coherent": True, "fragmented": True}, {"coherent": False, "fragmented": False}]},
                "client_portfolio_intelligence.json": {"portfolio_accounts": [{"healthy": True, "at-risk": True}, {"healthy": False, "at-risk": False}]},
                "retainer_management_assistant.json": {"retainer_plans": [{"on-track": True, "drifting": True}, {"on-track": False, "drifting": False}]},
                "recurring_revenue_optimizer.json": {"revenue_streams": [{"retained": True, "churning": True}, {"retained": False, "churning": False}]},
                "lead_to_invoice_workflow.json": {"workflow_steps": [{"connected": True, "broken": True}, {"connected": False, "broken": False}]},
                "sales_pipeline_forecaster.json": {"pipeline_deals": [{"likely": True, "stalled": True}, {"likely": False, "stalled": False}]},
                "proposal_follow_up_automator.json": {"follow_ups": [{"timely": True, "spammy": True}, {"timely": False, "spammy": False}]},
                "client_satisfaction_predictor.json": {"satisfaction_signals": [{"satisfied": True, "dissatisfied": True}, {"satisfied": False, "dissatisfied": False}]},
                "churn_prevention_engine.json": {"retention_paths": [{"recoverable": True, "churning": True}, {"recoverable": False, "churning": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.lkprofessionals_growth_tools.LKPROFESSIONALS_GROWTH_DIR", root):
                self.assertIn("Siloed routes: 1", company_wide_ai_nervous_system())
                self.assertIn("Fragmented views: 1", lkprofessionals_operations_brain())
                self.assertIn("At-risk accounts: 1", client_portfolio_intelligence())
                self.assertIn("Drifting plans: 1", retainer_management_assistant())
                self.assertIn("Churning streams: 1", recurring_revenue_optimizer())
                self.assertIn("Broken steps: 1", lead_to_invoice_workflow())
                self.assertIn("Stalled deals: 1", sales_pipeline_forecaster())
                self.assertIn("Spammy follow-ups: 1", proposal_follow_up_automator())
                self.assertIn("Dissatisfied signals: 1", client_satisfaction_predictor())
                self.assertIn("Churning paths: 1", churn_prevention_engine())

    def test_routes_cover_1541_to_1550(self):
        for phase in range(1541, 1551):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
