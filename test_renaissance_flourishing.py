import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.renaissance_flourishing_tools import *


class RenaissanceFlourishingTests(unittest.TestCase):
    def test_renaissance_flourishing_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "planetary_renaissance.json": {"renaissance_paths": [{"renewed": True, "stalled": True}, {"renewed": False, "stalled": False}]},
                "innovation_civilization.json": {"innovation_ecologies": [{"adaptive": True, "captured": True}, {"adaptive": False, "captured": False}]},
                "universal_prosperity.json": {"prosperity_streams": [{"prosperous": True, "uneven": True}, {"prosperous": False, "uneven": False}]},
                "cooperative_evolution.json": {"evolution_paths": [{"cooperative": True, "competitive": True}, {"cooperative": False, "competitive": False}]},
                "harmony_optimization.json": {"harmony_loops": [{"harmonized": True, "suppressed": True}, {"harmonized": False, "suppressed": False}]},
                "coexistence_substrate.json": {"coexistence_paths": [{"coexisting": True, "fractured": True}, {"coexisting": False, "fractured": False}]},
                "peace_amplification.json": {"peace_paths": [{"amplified": True, "tense": True}, {"amplified": False, "tense": False}]},
                "resilience_civilization.json": {"civilization_resilience_paths": [{"resilient": True, "brittle": True}, {"resilient": False, "brittle": False}]},
                "flourishing_simulator.json": {"flourishing_scenarios": [{"simulated": True, "depriving": True}, {"simulated": False, "depriving": False}]},
                "wisdom_harmonization.json": {"wisdom_streams": [{"harmonized": True, "conflicted": True}, {"harmonized": False, "conflicted": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.renaissance_flourishing_tools.RENAISSANCE_FLOURISHING_DIR", root):
                self.assertIn("Stalled paths: 1", universal_planetary_renaissance_framework())
                self.assertIn("Captured ecologies: 1", adaptive_innovation_civilization_substrate())
                self.assertIn("Uneven streams: 1", autonomous_universal_prosperity_engine())
                self.assertIn("Competitive paths: 1", infinite_scale_cooperative_evolution_ai())
                self.assertIn("Suppressed loops: 1", recursive_harmony_optimization_framework())
                self.assertIn("Fractured paths: 1", universal_coexistence_substrate())
                self.assertIn("Tense peace: 1", adaptive_peace_amplification_engine())
                self.assertIn("Brittle paths: 1", autonomous_resilience_civilization_ai())
                self.assertIn("Depriving scenarios: 1", infinite_scale_flourishing_simulator())
                self.assertIn("Conflicted streams: 1", recursive_wisdom_harmonization_framework())

    def test_routes_cover_1301_to_1310(self):
        for phase in range(1301, 1311):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
