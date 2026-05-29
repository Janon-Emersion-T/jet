import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.retail_command_tools import *


class RetailCommandToolsTests(unittest.TestCase):
    def test_retail_command_tools_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "product_recommendation_engine.json": {"recommendation_sets": [{"relevant": True, "weak": True}, {"relevant": False, "weak": False}]},
                "stock_reorder_predictor.json": {"reorder_paths": [{"timely": True, "late": True}, {"timely": False, "late": False}]},
                "demand_seasonality_analyzer.json": {"seasonality_models": [{"grounded": True, "noisy": True}, {"grounded": False, "noisy": False}]},
                "sales_margin_optimizer.json": {"margin_paths": [{"healthy": True, "compressed": True}, {"healthy": False, "compressed": False}]},
                "customer_segmentation_engine.json": {"customer_segments": [{"actionable": True, "blurry": True}, {"actionable": False, "blurry": False}]},
                "loyalty_program_intelligence.json": {"loyalty_paths": [{"engaging": True, "stagnant": True}, {"engaging": False, "stagnant": False}]},
                "discount_abuse_detector.json": {"discount_events": [{"legitimate": True, "abusive": True}, {"legitimate": False, "abusive": False}]},
                "fraud_risk_scoring.json": {"risk_events": [{"low-risk": True, "high-risk": True}, {"low-risk": False, "high-risk": False}]},
                "returns_pattern_analyzer.json": {"return_patterns": [{"routine": True, "spiking": True}, {"routine": False, "spiking": False}]},
                "retail_command_intelligence.json": {"retail_panels": [{"actionable": True, "fragmented": True}, {"actionable": False, "fragmented": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.retail_command_tools.RETAIL_COMMAND_DIR", root):
                self.assertIn("Weak sets: 1", product_recommendation_engine())
                self.assertIn("Late reorders: 1", stock_reorder_predictor())
                self.assertIn("Noisy models: 1", demand_seasonality_analyzer())
                self.assertIn("Compressed margins: 1", sales_margin_optimizer())
                self.assertIn("Blurry segments: 1", customer_segmentation_engine())
                self.assertIn("Stagnant paths: 1", loyalty_program_intelligence())
                self.assertIn("Abusive events: 1", discount_abuse_detector())
                self.assertIn("High-risk events: 1", fraud_risk_scoring())
                self.assertIn("Spiking patterns: 1", returns_pattern_analyzer())
                self.assertIn("Fragmented panels: 1", retail_command_intelligence())

    def test_routes_cover_1641_to_1650(self):
        for phase in range(1641, 1651):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
