import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.marketing_performance_tools import *


class MarketingPerformanceTests(unittest.TestCase):
    def test_marketing_performance_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "marketing_roi.json": {"campaigns": [{"profitable": True, "wasteful": True}, {"profitable": False, "wasteful": False}]},
                "seo_revenue_attribution.json": {"seo_paths": [{"attributed": True, "uncertain": True}, {"attributed": False, "uncertain": False}]},
                "content_to_lead.json": {"content_assets": [{"converting": True, "ignored": True}, {"converting": False, "ignored": False}]},
                "social_performance_predictor.json": {"social_posts": [{"outperforming": True, "underperforming": True}, {"outperforming": False, "underperforming": False}]},
                "campaign_budget_optimizer.json": {"budget_routes": [{"balanced": True, "overspent": True}, {"balanced": False, "overspent": False}]},
                "ad_creative_testing.json": {"creative_tests": [{"validated": True, "inconclusive": True}, {"validated": False, "inconclusive": False}]},
                "landing_page_psychology.json": {"page_reviews": [{"persuasive": True, "confusing": True}, {"persuasive": False, "confusing": False}]},
                "conversion_friction.json": {"conversion_steps": [{"smooth": True, "frictional": True}, {"smooth": False, "frictional": False}]},
                "user_journey_simulator.json": {"journeys": [{"coherent": True, "broken": True}, {"coherent": False, "broken": False}]},
                "trust_signal_optimizer.json": {"trust_signals": [{"credible": True, "weak": True}, {"credible": False, "weak": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.marketing_performance_tools.MARKETING_PERFORMANCE_DIR", root):
                self.assertIn("Wasteful campaigns: 1", marketing_roi_brain())
                self.assertIn("Uncertain paths: 1", seo_revenue_attribution())
                self.assertIn("Ignored assets: 1", content_to_lead_intelligence())
                self.assertIn("Underperforming posts: 1", social_media_performance_predictor())
                self.assertIn("Overspent routes: 1", campaign_budget_optimizer())
                self.assertIn("Inconclusive tests: 1", ad_creative_testing_engine())
                self.assertIn("Confusing pages: 1", landing_page_psychology_analyzer())
                self.assertIn("Frictional steps: 1", conversion_friction_detector())
                self.assertIn("Broken journeys: 1", user_journey_simulator())
                self.assertIn("Weak signals: 1", trust_signal_optimizer())

    def test_routes_cover_1551_to_1560(self):
        for phase in range(1551, 1561):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
