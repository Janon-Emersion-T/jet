import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.partnership_sales_tools import *


class PartnershipSalesTests(unittest.TestCase):
    def test_partnership_sales_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "podcast_workflow.json": {"episode_workflows": [{"ready": True, "blocked": True}, {"ready": False, "blocked": False}]},
                "newsletter_intelligence.json": {"newsletter_issues": [{"engaging": True, "ignored": True}, {"engaging": False, "ignored": False}]},
                "community_building_assistant.json": {"community_loops": [{"healthy": True, "stalled": True}, {"healthy": False, "stalled": False}]},
                "partnership_discovery.json": {"partner_candidates": [{"aligned": True, "weak-fit": True}, {"aligned": False, "weak-fit": False}]},
                "tender_opportunity_detector.json": {"tender_leads": [{"eligible": True, "mismatched": True}, {"eligible": False, "mismatched": False}]},
                "government_proposal_assistant.json": {"proposal_sections": [{"compliant": True, "missing": True}, {"compliant": False, "missing": False}]},
                "enterprise_sales_enablement.json": {"sales_assets": [{"useful": True, "weak": True}, {"useful": False, "weak": False}]},
                "competitive_positioning.json": {"positioning_angles": [{"distinct": True, "blurry": True}, {"distinct": False, "blurry": False}]},
                "pricing_psychology.json": {"pricing_tests": [{"clear": True, "confusing": True}, {"clear": False, "confusing": False}]},
                "service_packaging_engine.json": {"service_packages": [{"coherent": True, "messy": True}, {"coherent": False, "messy": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.partnership_sales_tools.PARTNERSHIP_SALES_DIR", root):
                self.assertIn("Blocked workflows: 1", podcast_workflow_assistant())
                self.assertIn("Ignored issues: 1", newsletter_intelligence_engine())
                self.assertIn("Stalled loops: 1", community_building_assistant())
                self.assertIn("Weak-fit candidates: 1", partnership_discovery_ai())
                self.assertIn("Mismatched leads: 1", tender_opportunity_detector())
                self.assertIn("Missing sections: 1", government_proposal_assistant())
                self.assertIn("Weak assets: 1", enterprise_sales_enablement_brain())
                self.assertIn("Blurry angles: 1", competitive_positioning_engine())
                self.assertIn("Confusing tests: 1", pricing_psychology_analyzer())
                self.assertIn("Messy packages: 1", dynamic_service_packaging_engine())

    def test_routes_cover_1571_to_1580(self):
        for phase in range(1571, 1581):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
