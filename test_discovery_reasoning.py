import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.discovery_reasoning_tools import *


class DiscoveryReasoningTests(unittest.TestCase):
    def test_discovery_reasoning_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "mentorship_cognition.json": {"mentorships": [{"supported": True, "orphaned": True}, {"supported": False, "orphaned": False}]},
                "lifelong_development.json": {"journeys": [{"adaptive": True, "fragmented": True}, {"adaptive": False, "fragmented": False}]},
                "curiosity_amplification.json": {"explorations": [{"amplified": True, "distracted": True}, {"amplified": False, "distracted": False}]},
                "exploration_intelligence.json": {"missions": [{"scouted": True, "blind": True}, {"scouted": False, "blind": False}]},
                "knowledge_frontier.json": {"frontiers": [{"modeled": True, "uncertain": True}, {"modeled": False, "uncertain": False}]},
                "discovery_optimization.json": {"pipelines": [{"optimized": True, "biased": True}, {"optimized": False, "biased": False}]},
                "scientific_collaboration.json": {"collaborations": [{"paired": True, "blocked": True}, {"paired": False, "blocked": False}]},
                "theorem_generation.json": {"theorems": [{"generated": True, "unproved": True}, {"generated": False, "unproved": False}]},
                "mathematical_cognition.json": {"models": [{"reasoning": True, "inconsistent": True}, {"reasoning": False, "inconsistent": False}]},
                "abstraction_synthesis.json": {"abstractions": [{"synthesized": True, "leaky": True}, {"synthesized": False, "leaky": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.discovery_reasoning_tools.DISCOVERY_REASONING_DIR", root):
                self.assertIn("Orphaned mentorships: 1", universal_mentorship_cognition_engine())
                self.assertIn("Fragmented journeys: 1", adaptive_lifelong_development_substrate())
                self.assertIn("Distracted explorations: 1", autonomous_curiosity_amplification_system())
                self.assertIn("Blind missions: 1", infinite_scale_exploration_intelligence())
                self.assertIn("Uncertain frontiers: 1", recursive_knowledge_frontier_simulator())
                self.assertIn("Biased pipelines: 1", universal_discovery_optimization_engine())
                self.assertIn("Blocked collaborations: 1", adaptive_scientific_collaboration_ai())
                self.assertIn("Unproved theorems: 1", autonomous_theorem_generation_framework())
                self.assertIn("Inconsistent models: 1", infinite_scale_mathematical_cognition_substrate())
                self.assertIn("Leaky abstractions: 1", recursive_abstraction_synthesis_engine())

    def test_routes_cover_1121_to_1130(self):
        for phase in range(1121, 1131):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
