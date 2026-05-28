import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.policy_systems_tools import *


class PolicySystemsTests(unittest.TestCase):
    def test_policy_systems_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "civic_education.json": {"curricula": [{"adaptive": True, "gaps": True}, {"adaptive": False, "gaps": False}]},
                "public_policy_simulator.json": {"policies": [{"simulated": True, "inequitable": True}, {"simulated": False, "inequitable": False}]},
                "social_equity.json": {"districts": [{"supported": True, "underserved": True}, {"supported": False, "underserved": False}]},
                "coordination_dashboard.json": {"streams": [{"visible": True, "blocked": True}, {"visible": False, "blocked": False}]},
                "diplomacy_simulator.json": {"dialogues": [{"simulated": True, "tense": True}, {"simulated": False, "tense": False}]},
                "galactic_logistics.json": {"routes": [{"modeled": True, "infeasible": True}, {"modeled": False, "infeasible": False}]},
                "societal_stability.json": {"societies": [{"stable": True, "brittle": True}, {"stable": False, "brittle": False}]},
                "ethical_expansion.json": {"expansions": [{"reviewed": True, "risk": "high"}, {"reviewed": False, "risk": "low"}]},
                "discovery_synthesizer.json": {"syntheses": [{"linked": True, "weak": True}, {"linked": False, "weak": False}]},
                "systems_thinking.json": {"systems": [{"modeled": True, "entangled": True}, {"modeled": False, "entangled": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.policy_systems_tools.POLICY_SYSTEMS_DIR", root):
                self.assertIn("Gap-marked curricula: 1", universal_civic_education_engine())
                self.assertIn("Inequitable policies: 1", hyper_personalized_public_policy_simulator())
                self.assertIn("Underserved districts: 1", ai_guided_social_equity_framework())
                self.assertIn("Blocked streams: 1", planetary_scale_coordination_dashboard())
                self.assertIn("Tense dialogues: 1", multi_civilization_diplomacy_simulator())
                self.assertIn("Infeasible routes: 1", autonomous_galactic_logistics_research())
                self.assertIn("Brittle societies: 1", long_duration_societal_stability_engine())
                self.assertIn("High-risk expansions: 1", ai_guided_ethical_expansion_framework())
                self.assertIn("Weak syntheses: 1", interdisciplinary_discovery_synthesizer())
                self.assertIn("Entangled systems: 1", universal_systems_thinking_engine())

    def test_routes_cover_911_to_920(self):
        for phase in range(911, 921):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
