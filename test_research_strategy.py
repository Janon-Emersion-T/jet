import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.research_strategy_tools import *


class ResearchStrategyTests(unittest.TestCase):
    def test_research_strategy_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "research_fusion.json": {"programs": [{"fused": True, "blocked": True}, {"fused": False, "blocked": False}]},
                "interstellar_strategy.json": {"strategies": [{"adaptive": True, "fragile": True}, {"adaptive": False, "fragile": False}]},
                "existential_risk.json": {"risks": [{"modeled": True, "escalating": True}, {"modeled": False, "escalating": False}]},
                "predictive_civilization.json": {"scenarios": [{"predicted": True, "volatile": True}, {"predicted": False, "volatile": False}]},
                "cosmic_operations.json": {"operations": [{"planned": True, "overextended": True}, {"planned": False, "overextended": False}]},
                "prosperity_balancing.json": {"balances": [{"balanced": True, "uneven": True}, {"balanced": False, "uneven": False}]},
                "moral_reasoning.json": {"reasoners": [{"aligned": True, "contested": True}, {"aligned": False, "contested": False}]},
                "flourishing_simulation.json": {"cohorts": [{"simulated": True, "stressed": True}, {"simulated": False, "stressed": False}]},
                "multi_generational_planning.json": {"plans": [{"long_horizon": True, "unfunded": True}, {"long_horizon": False, "unfunded": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.research_strategy_tools.RESEARCH_STRATEGY_DIR", root):
                self.assertIn("Blocked programs: 1", cross_disciplinary_research_fusion_ai())
                self.assertIn("Fragile strategies: 1", adaptive_interstellar_strategy_simulator())
                self.assertIn("Escalating risks: 1", recursive_existential_risk_analyzer())
                self.assertIn("Volatile scenarios: 1", universal_predictive_civilization_engine())
                self.assertIn("Overextended operations: 1", autonomous_cosmic_scale_operations_planner())
                self.assertIn("Uneven plans: 1", planetary_prosperity_balancing_framework())
                self.assertIn("Contested reasoners: 1", infinite_scale_moral_reasoning_mesh())
                self.assertIn("Stressed cohorts: 1", human_flourishing_simulation_substrate())
                self.assertIn("Unfunded plans: 1", autonomous_multi_generational_planning_system())

    def test_routes_cover_1029_to_1037(self):
        for phase in range(1029, 1038):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
