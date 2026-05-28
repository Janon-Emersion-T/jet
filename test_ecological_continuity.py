import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.ecological_continuity_tools import *


class EcologicalContinuityTests(unittest.TestCase):
    def test_ecological_continuity_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "multi_species_cooperation.json": {"coalitions": [{"aligned": True, "strained": True}, {"aligned": False, "strained": False}]},
                "ecological_stewardship.json": {"habitats": [{"stewarded": True, "degraded": True}, {"stewarded": False, "degraded": False}]},
                "civilization_memory_archive.json": {"archives": [{"healed": True, "fractured": True}, {"healed": False, "fractured": False}]},
                "semantic_continuity.json": {"vocabularies": [{"synchronized": True, "drifting": True}, {"synchronized": False, "drifting": False}]},
                "planetary_logistics_optimizer.json": {"routes": [{"optimized": True, "fragile": True}, {"optimized": False, "fragile": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.ecological_continuity_tools.ECOLOGICAL_CONTINUITY_DIR", root):
                self.assertIn("Strained coalitions: 1", autonomous_multi_species_cooperation_engine())
                self.assertIn("Degraded habitats: 1", universal_ecological_stewardship_intelligence())
                self.assertIn("Fractured archives: 1", self_healing_civilization_memory_archive())
                self.assertIn("Drifting vocabularies: 1", planetary_semantic_continuity_system())
                self.assertIn("Fragile routes: 1", recursive_planetary_logistics_optimizer())

    def test_routes_cover_1021_to_1025(self):
        for phase in range(1021, 1026):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
