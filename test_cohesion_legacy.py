import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.cohesion_legacy_tools import *


class CohesionLegacyTests(unittest.TestCase):
    def test_cohesion_legacy_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "social_cohesion.json": {"cohesion_networks": [{"cohesive": True, "fractured": True}, {"cohesive": False, "fractured": False}]},
                "belonging_optimization.json": {"belonging_programs": [{"supportive": True, "isolating": True}, {"supportive": False, "isolating": False}]},
                "cultural_preservation.json": {"cultures": [{"preserved": True, "eroding": True}, {"preserved": False, "eroding": False}]},
                "diversity_harmonization.json": {"diversity_networks": [{"harmonized": True, "flattened": True}, {"harmonized": False, "flattened": False}]},
                "inclusion_framework.json": {"inclusion_paths": [{"inclusive": True, "excluded": True}, {"inclusive": False, "excluded": False}]},
                "collaborative_civilization.json": {"civilization_partnerships": [{"collaborative": True, "fragmented": True}, {"collaborative": False, "fragmented": False}]},
                "intergenerational_continuity.json": {"continuity_chains": [{"continuous": True, "broken": True}, {"continuous": False, "broken": False}]},
                "wisdom_transfer.json": {"wisdom_paths": [{"transferred": True, "stalled": True}, {"transferred": False, "stalled": False}]},
                "memory_inheritance.json": {"memory_lines": [{"inherited": True, "lossy": True}, {"inherited": False, "lossy": False}]},
                "ancestry_simulation.json": {"ancestries": [{"simulated": True, "speculative": True}, {"simulated": False, "speculative": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.cohesion_legacy_tools.COHESION_LEGACY_DIR", root):
                self.assertIn("Fractured networks: 1", universal_social_cohesion_substrate())
                self.assertIn("Isolating programs: 1", adaptive_belonging_optimization_framework())
                self.assertIn("Eroding cultures: 1", autonomous_cultural_preservation_ai())
                self.assertIn("Flattened networks: 1", infinite_scale_diversity_harmonization_engine())
                self.assertIn("Excluded paths: 1", recursive_inclusion_framework())
                self.assertIn("Fragmented partnerships: 1", universal_collaborative_civilization_ai())
                self.assertIn("Broken chains: 1", adaptive_intergenerational_continuity_substrate())
                self.assertIn("Stalled wisdom: 1", autonomous_wisdom_transfer_engine())
                self.assertIn("Lossy memory: 1", infinite_scale_memory_inheritance_framework())
                self.assertIn("Speculative ancestries: 1", recursive_ancestry_simulation_ai())

    def test_routes_cover_1241_to_1250(self):
        for phase in range(1241, 1251):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
