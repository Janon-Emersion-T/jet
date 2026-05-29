import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.talent_future_tools import *


class TalentFutureTests(unittest.TestCase):
    def test_talent_future_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "inspiration_network.json": {"inspiration_nodes": [{"inspired": True, "blocked": True}, {"inspired": False, "blocked": False}]},
                "genius_cultivation.json": {"cultivation_paths": [{"cultivated": True, "excluded": True}, {"cultivated": False, "excluded": False}]},
                "talent_emergence.json": {"talent_signals": [{"emerged": True, "suppressed": True}, {"emerged": False, "suppressed": False}]},
                "human_potential.json": {"potential_paths": [{"expanded": True, "underrealized": True}, {"expanded": False, "underrealized": False}]},
                "capability_expansion.json": {"capabilities": [{"expanded": True, "misapplied": True}, {"expanded": False, "misapplied": False}]},
                "empowerment_substrate.json": {"empowerment_paths": [{"empowered": True, "disempowered": True}, {"empowered": False, "disempowered": False}]},
                "aspiration_harmonization.json": {"aspirations": [{"aligned": True, "suppressed": True}, {"aligned": False, "suppressed": False}]},
                "achievement_optimization.json": {"achievement_paths": [{"optimized": True, "burned_out": True}, {"optimized": False, "burned_out": False}]},
                "possibility_simulation.json": {"possibility_branches": [{"simulated": True, "collapsed": True}, {"simulated": False, "collapsed": False}]},
                "future_civilization.json": {"civilization_futures": [{"modeled": True, "regressing": True}, {"modeled": False, "regressing": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.talent_future_tools.TALENT_FUTURE_DIR", root):
                self.assertIn("Blocked nodes: 1", universal_inspiration_network())
                self.assertIn("Excluded paths: 1", adaptive_genius_cultivation_framework())
                self.assertIn("Suppressed talent: 1", autonomous_talent_emergence_engine())
                self.assertIn("Underrealized paths: 1", infinite_scale_human_potential_ai())
                self.assertIn("Misapplied capabilities: 1", recursive_capability_expansion_framework())
                self.assertIn("Disempowered paths: 1", universal_empowerment_substrate())
                self.assertIn("Suppressed aspirations: 1", adaptive_aspiration_harmonizer())
                self.assertIn("Burned-out paths: 1", autonomous_achievement_optimization_engine())
                self.assertIn("Collapsed branches: 1", infinite_scale_possibility_simulator())
                self.assertIn("Regressing futures: 1", recursive_future_civilization_ai())

    def test_routes_cover_1291_to_1300(self):
        for phase in range(1291, 1301):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
