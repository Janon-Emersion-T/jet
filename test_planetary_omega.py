import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.planetary_omega_tools import *


class PlanetaryOmegaTests(unittest.TestCase):
    def test_planetary_omega_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "recursive_planetary_optimization.json": {"loops": [{"optimized": True, "unstable": True}, {"optimized": False, "unstable": False}]},
                "interstellar_governance.json": {"charters": [{"reviewed": True, "contested": True}, {"reviewed": False, "contested": False}]},
                "adaptive_learning_civilization.json": {"cohorts": [{"adaptive": True, "fragmented": True}, {"adaptive": False, "fragmented": False}]},
                "planetary_consciousness.json": {"studies": [{"status": "active", "speculative": True}, {"status": "idle", "speculative": False}]},
                "existential_continuity.json": {"continuities": [{"linked": True, "ambiguous": True}, {"linked": False, "ambiguous": False}]},
                "universal_diplomacy.json": {"dialogues": [{"mediated": True, "tense": True}, {"mediated": False, "tense": False}]},
                "continuity_archive_intelligence.json": {"archives": [{"indexed": True, "stale": True}, {"indexed": False, "stale": False}]},
                "governance_cognition.json": {"engines": [{"evolving": True, "drifted": True}, {"evolving": False, "drifted": False}]},
                "cooperative_planning.json": {"plans": [{"synchronized": True, "fragmented": True}, {"synchronized": False, "fragmented": False}]},
                "planetary_ecosystem_stewardship.json": {"ecosystems": [{"stewarded": True, "degraded": True}, {"stewarded": False, "degraded": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.planetary_omega_tools.PLANETARY_OMEGA_DIR", root):
                self.assertIn("Unstable loops: 1", recursive_planetary_optimization_framework())
                self.assertIn("Contested charters: 1", ai_guided_interstellar_governance_sandbox())
                self.assertIn("Fragmented cohorts: 1", universal_adaptive_learning_civilization())
                self.assertIn("Speculative studies: 1", planetary_consciousness_research_engine())
                self.assertIn("Ambiguous continuities: 1", autonomous_existential_continuity_system())
                self.assertIn("Tense dialogues: 1", ai_assisted_universal_diplomacy_layer())
                self.assertIn("Stale archives: 1", civilization_continuity_archive_intelligence())
                self.assertIn("Drifted engines: 1", self_evolving_governance_cognition_engine())
                self.assertIn("Fragmented plans: 1", infinite_scale_cooperative_planning_framework())
                self.assertIn("Degraded ecosystems: 1", ai_stewardship_of_planetary_ecosystems())

    def test_routes_cover_951_to_960(self):
        for phase in range(951, 961):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
