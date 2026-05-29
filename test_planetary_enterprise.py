import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.planetary_enterprise_tools import *


class PlanetaryEnterpriseTests(unittest.TestCase):
    def test_planetary_enterprise_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "planetary_coordination.json": {"coordination_loops": [{"coordinated": True, "fragmented": True}, {"coordinated": False, "fragmented": False}]},
                "macroeconomic_balancing.json": {"economies": [{"balanced": True, "volatile": True}, {"balanced": False, "volatile": False}]},
                "energy_allocation.json": {"allocations": [{"optimized": True, "deprived": True}, {"optimized": False, "deprived": False}]},
                "supply_stabilization.json": {"supply_chains": [{"stabilized": True, "disrupted": True}, {"stabilized": False, "disrupted": False}]},
                "distribution_equity.json": {"distributions": [{"equitable": True, "skewed": True}, {"equitable": False, "skewed": False}]},
                "labor_optimization.json": {"labor_models": [{"optimized": True, "extractive": True}, {"optimized": False, "extractive": False}]},
                "automation_transition.json": {"transitions": [{"supported": True, "displacing": True}, {"supported": False, "displacing": False}]},
                "innovation_prioritization.json": {"priorities": [{"prioritized": True, "neglected": True}, {"prioritized": False, "neglected": False}]},
                "capital_allocation.json": {"portfolios": [{"allocated": True, "concentrated": True}, {"allocated": False, "concentrated": False}]},
                "entrepreneurship_simulation.json": {"ventures": [{"simulated": True, "fragile": True}, {"simulated": False, "fragile": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.planetary_enterprise_tools.PLANETARY_ENTERPRISE_DIR", root):
                self.assertIn("Fragmented loops: 1", universal_planetary_coordination_intelligence())
                self.assertIn("Volatile economies: 1", adaptive_macroeconomic_balancing_ai())
                self.assertIn("Deprived allocations: 1", autonomous_energy_allocation_substrate())
                self.assertIn("Disrupted chains: 1", infinite_scale_supply_stabilization_framework())
                self.assertIn("Skewed distributions: 1", recursive_distribution_equity_engine())
                self.assertIn("Extractive models: 1", universal_labor_optimization_ai())
                self.assertIn("Displacing transitions: 1", adaptive_automation_transition_framework())
                self.assertIn("Neglected opportunities: 1", autonomous_innovation_prioritization_engine())
                self.assertIn("Concentrated portfolios: 1", infinite_scale_capital_allocation_ai())
                self.assertIn("Fragile ventures: 1", recursive_entrepreneurship_simulation_framework())

    def test_routes_cover_1201_to_1210(self):
        for phase in range(1201, 1211):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
