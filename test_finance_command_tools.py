import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.finance_command_tools import *


class FinanceCommandToolsTests(unittest.TestCase):
    def test_finance_command_tools_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "payment_milestones.json": {"payment_milestones": [{"on-track": True, "overdue": True}, {"on-track": False, "overdue": False}]},
                "invoice_disputes.json": {"invoice_disputes": [{"documented": True, "unresolved": True}, {"documented": False, "unresolved": False}]},
                "cash_flow_prediction.json": {"cash_flow_scenarios": [{"stable": True, "strained": True}, {"stable": False, "strained": False}]},
                "expense_anomalies.json": {"expense_events": [{"normal": True, "anomalous": True}, {"normal": False, "anomalous": False}]},
                "tax_planning_assistant.json": {"tax_scenarios": [{"compliant": True, "uncertain": True}, {"compliant": False, "uncertain": False}]},
                "financial_runway_simulator.json": {"runway_models": [{"durable": True, "short": True}, {"durable": False, "short": False}]},
                "company_valuation_estimator.json": {"valuation_models": [{"defensible": True, "speculative": True}, {"defensible": False, "speculative": False}]},
                "investor_pitch_intelligence.json": {"pitch_sections": [{"convincing": True, "weak": True}, {"convincing": False, "weak": False}]},
                "board_report_generator.json": {"board_sections": [{"ready": True, "thin": True}, {"ready": False, "thin": False}]},
                "executive_war_room_mode.json": {"decision_panels": [{"actionable": True, "chaotic": True}, {"actionable": False, "chaotic": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.finance_command_tools.FINANCE_COMMAND_DIR", root):
                self.assertIn("Overdue milestones: 1", payment_milestone_tracker())
                self.assertIn("Unresolved disputes: 1", invoice_dispute_assistant())
                self.assertIn("Strained scenarios: 1", cash_flow_prediction_engine())
                self.assertIn("Anomalous events: 1", expense_anomaly_detector())
                self.assertIn("Uncertain scenarios: 1", tax_planning_assistant())
                self.assertIn("Short models: 1", financial_runway_simulator())
                self.assertIn("Speculative models: 1", company_valuation_estimator())
                self.assertIn("Weak sections: 1", investor_pitch_intelligence())
                self.assertIn("Thin sections: 1", board_report_generator())
                self.assertIn("Chaotic panels: 1", executive_war_room_mode())

    def test_routes_cover_1591_to_1600(self):
        for phase in range(1591, 1601):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
