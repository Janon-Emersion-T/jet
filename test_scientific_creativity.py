import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.scientific_creativity_tools import *


class ScientificCreativityTests(unittest.TestCase):
    def test_scientific_creativity_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "scientific_synthesis.json": {"syntheses": [{"integrated": True, "contested": True}, {"integrated": False, "contested": False}]},
                "innovation_acceleration.json": {"programs": [{"accelerated": True, "stalled": True}, {"accelerated": False, "stalled": False}]},
                "creativity_orchestration.json": {"ensembles": [{"orchestrated": True, "chaotic": True}, {"orchestrated": False, "chaotic": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.scientific_creativity_tools.SCIENTIFIC_CREATIVITY_DIR", root):
                self.assertIn("Contested syntheses: 1", universal_scientific_synthesis_engine())
                self.assertIn("Stalled programs: 1", autonomous_innovation_acceleration_matrix())
                self.assertIn("Chaotic ensembles: 1", infinite_scale_creativity_orchestration_layer())

    def test_routes_cover_1026_to_1028(self):
        for phase in range(1026, 1029):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
