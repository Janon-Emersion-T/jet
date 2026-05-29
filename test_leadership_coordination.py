import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.leadership_coordination_tools import *


class LeadershipCoordinationTests(unittest.TestCase):
    def test_leadership_coordination_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "leadership_augmentation.json": {"leaders": [{"augmented": True, "isolated": True}, {"augmented": False, "isolated": False}]},
                "executive_cognition.json": {"executives": [{"supported": True, "overloaded": True}, {"supported": False, "overloaded": False}]},
                "board_reasoning.json": {"board_cases": [{"reasoned": True, "conflicted": True}, {"reasoned": False, "conflicted": False}]},
                "strategic_planning.json": {"strategies": [{"planned": True, "fragmented": True}, {"planned": False, "fragmented": False}]},
                "mission_alignment.json": {"missions": [{"aligned": True, "drifting": True}, {"aligned": False, "drifting": False}]},
                "purpose_governance.json": {"governance_loops": [{"purposeful": True, "captured": True}, {"purposeful": False, "captured": False}]},
                "institutional_ethics.json": {"ethics_programs": [{"adaptive": True, "compromised": True}, {"adaptive": False, "compromised": False}]},
                "global_coordination.json": {"coalitions": [{"coordinated": True, "misaligned": True}, {"coordinated": False, "misaligned": False}]},
                "humanitarian_optimization.json": {"aid_networks": [{"optimized": True, "underserved": True}, {"optimized": False, "underserved": False}]},
                "civilization_prosperity.json": {"prosperity_loops": [{"prospering": True, "uneven": True}, {"prospering": False, "uneven": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.leadership_coordination_tools.LEADERSHIP_COORDINATION_DIR", root):
                self.assertIn("Isolated leaders: 1", universal_leadership_augmentation_ai())
                self.assertIn("Overloaded executives: 1", adaptive_executive_cognition_framework())
                self.assertIn("Conflicted cases: 1", autonomous_board_level_reasoning_engine())
                self.assertIn("Fragmented strategies: 1", infinite_scale_strategic_planning_substrate())
                self.assertIn("Drifting missions: 1", recursive_mission_alignment_ai())
                self.assertIn("Captured loops: 1", universal_purpose_driven_governance_framework())
                self.assertIn("Compromised programs: 1", adaptive_institutional_ethics_engine())
                self.assertIn("Misaligned coalitions: 1", autonomous_global_coordination_ai())
                self.assertIn("Underserved aid networks: 1", infinite_scale_humanitarian_optimization_framework())
                self.assertIn("Uneven loops: 1", recursive_civilization_prosperity_engine())

    def test_routes_cover_1221_to_1230(self):
        for phase in range(1221, 1231):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
