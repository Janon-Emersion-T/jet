import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.sustainability_agri_tools import *


class SustainabilityAgriTests(unittest.TestCase):
    def test_sustainability_agri_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "energy_optimization.json": {"sites": [{"optimized": True, "status": "peak"}, {"optimized": False, "status": "normal"}]},
                "smart_grid.json": {"nodes": [{"balanced": True, "status": "unstable"}, {"balanced": False, "status": "stable"}]},
                "environmental_monitoring.json": {"sensors": [{"alert": True, "status": "healthy"}, {"alert": False, "status": "offline"}]},
                "climate_simulation.json": {"runs": [{"status": "completed", "uncertain": True}, {"status": "draft", "uncertain": False}]},
                "agri_orchestration.json": {"farms": [{"coordinated": True, "status": "stressed"}, {"coordinated": False, "status": "healthy"}]},
                "precision_farming.json": {"plots": [{"targeted": True, "yield": "low"}, {"targeted": False, "yield": "high"}]},
                "irrigation.json": {"zones": [{"optimized": True, "status": "dry"}, {"optimized": False, "status": "wet"}]},
                "livestock_monitoring.json": {"herds": [{"monitored": True, "risk": "high"}, {"monitored": False, "risk": "low"}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.sustainability_agri_tools.SUSTAINABILITY_DIR", root):
                self.assertIn("Peak-load sites: 1", autonomous_energy_optimization())
                self.assertIn("Unstable nodes: 1", smart_grid_management_ai())
                self.assertIn("Alerting sensors: 1", environmental_monitoring_intelligence())
                self.assertIn("Uncertain runs: 1", climate_simulation_assistant())
                self.assertIn("Stressed farms: 1", agricultural_ai_orchestration())
                self.assertIn("Low-yield plots: 1", precision_farming_engine())
                self.assertIn("Dry zones: 1", smart_irrigation_optimizer())
                self.assertIn("High-risk herds: 1", livestock_monitoring_ai())

    def test_routes_cover_621_to_628(self):
        for phase in range(621, 629):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
