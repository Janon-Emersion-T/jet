import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.civilization_continuity_tools import *


class CivilizationContinuityTests(unittest.TestCase):
    def test_civilization_continuity_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "human_potential.json": {"cohorts": [{"amplified": True, "uneven": True}, {"amplified": False, "uneven": False}]},
                "intelligence_collaboration.json": {"teams": [{"linked": True, "siloed": True}, {"linked": False, "siloed": False}]},
                "recursive_innovation.json": {"loops": [{"compounding": True, "unstable": True}, {"compounding": False, "unstable": False}]},
                "scientific_frontier.json": {"programs": [{"expanding": True, "speculative": True}, {"expanding": False, "speculative": False}]},
                "civilization_mentor.json": {"mentors": [{"status": "active", "overfit": True}, {"status": "idle", "overfit": False}]},
                "planetary_evolution.json": {"pathways": [{"guided": True, "controversial": True}, {"guided": False, "controversial": False}]},
                "universal_discovery.json": {"discoveries": [{"surfaced": True, "tentative": True}, {"surfaced": False, "tentative": False}]},
                "cooperative_intelligence.json": {"cooperatives": [{"synchronized": True, "fragmented": True}, {"synchronized": False, "fragmented": False}]},
                "interstellar_preparation.json": {"preparations": [{"staged": True, "premature": True}, {"staged": False, "premature": False}]},
                "species_continuity.json": {"plans": [{"durable": True, "exposed": True}, {"durable": False, "exposed": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.civilization_continuity_tools.CIV_CONT_DIR", root):
                self.assertIn("Uneven cohorts: 1", human_potential_amplification_layer())
                self.assertIn("Siloed teams: 1", global_intelligence_collaboration_system())
                self.assertIn("Unstable loops: 1", recursive_innovation_engine())
                self.assertIn("Speculative programs: 1", self_expanding_scientific_frontier())
                self.assertIn("Overfit mentors: 1", autonomous_civilization_mentor())
                self.assertIn("Controversial pathways: 1", ai_guided_planetary_evolution())
                self.assertIn("Tentative discoveries: 1", universal_discovery_engine())
                self.assertIn("Fragmented cooperatives: 1", infinite_scale_cooperative_intelligence())
                self.assertIn("Premature preparations: 1", autonomous_interstellar_preparation_ai())
                self.assertIn("Exposed plans: 1", species_continuity_intelligence())

    def test_routes_cover_891_to_900(self):
        for phase in range(891, 901):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
