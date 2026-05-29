import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.client_delivery_finance_tools import *


class ClientDeliveryFinanceTests(unittest.TestCase):
    def test_client_delivery_finance_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "saas_pricing_simulator.json": {"pricing_scenarios": [{"viable": True, "fragile": True}, {"viable": False, "fragile": False}]},
                "productized_service_builder.json": {"service_blueprints": [{"productized": True, "underspecified": True}, {"productized": False, "underspecified": False}]},
                "white_label_product_manager.json": {"white_label_streams": [{"coherent": True, "risky": True}, {"coherent": False, "risky": False}]},
                "marketplace_listing_optimizer.json": {"listings": [{"optimized": True, "weak": True}, {"optimized": False, "weak": False}]},
                "affiliate_program_brain.json": {"affiliate_routes": [{"healthy": True, "abusive": True}, {"healthy": False, "abusive": False}]},
                "referral_intelligence_system.json": {"referral_loops": [{"productive": True, "weak": True}, {"productive": False, "weak": False}]},
                "client_onboarding_autopilot.json": {"onboarding_flows": [{"smooth": True, "confusing": True}, {"smooth": False, "confusing": False}]},
                "requirement_workshop_assistant.json": {"workshop_outputs": [{"clear": True, "ambiguous": True}, {"clear": False, "ambiguous": False}]},
                "meeting_to_sow_generator.json": {"sow_drafts": [{"usable": True, "incomplete": True}, {"usable": False, "incomplete": False}]},
                "milestone_planner.json": {"milestones": [{"realistic": True, "slipping": True}, {"realistic": False, "slipping": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.client_delivery_finance_tools.CLIENT_DELIVERY_FINANCE_DIR", root):
                self.assertIn("Fragile scenarios: 1", saas_pricing_simulator())
                self.assertIn("Underspecified blueprints: 1", productized_service_builder())
                self.assertIn("Risky streams: 1", white_label_product_manager())
                self.assertIn("Weak listings: 1", marketplace_listing_optimizer())
                self.assertIn("Abusive routes: 1", affiliate_program_brain())
                self.assertIn("Weak loops: 1", referral_intelligence_system())
                self.assertIn("Confusing flows: 1", client_onboarding_autopilot())
                self.assertIn("Ambiguous outputs: 1", client_requirement_workshop_assistant())
                self.assertIn("Incomplete drafts: 1", meeting_to_sow_generator())
                self.assertIn("Slipping milestones: 1", milestone_planner())

    def test_routes_cover_1581_to_1590(self):
        for phase in range(1581, 1591):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
