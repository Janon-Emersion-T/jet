import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.planetary_humanitarian_tools import *


class PlanetaryHumanitarianTests(unittest.TestCase):
    def test_planetary_humanitarian_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "synthetic_society.json": {"populations": [{"modeled": True, "diverse": True}, {"modeled": False, "diverse": False}]},
                "civilization_planning.json": {"plans": [{"reviewed": True, "equitable": True}, {"reviewed": False, "equitable": False}]},
                "planetary_optimization.json": {"systems": [{"optimized": True, "constrained": True}, {"optimized": False, "constrained": False}]},
                "resource_balancing.json": {"resources": [{"balanced": True, "status": "stressed"}, {"balanced": False, "status": "stable"}]},
                "climate_intervention.json": {"interventions": [{"modeled": True, "risk": "high"}, {"modeled": False, "risk": "low"}]},
                "ocean_monitoring.json": {"zones": [{"monitored": True, "status": "degraded"}, {"monitored": False, "status": "healthy"}]},
                "wildlife_preservation.json": {"habitats": [{"protected": True, "risk": "threatened"}, {"protected": False, "risk": "stable"}]},
                "biodiversity_prediction.json": {"forecasts": [{"calibrated": True, "trend": "declining"}, {"calibrated": False, "trend": "recovering"}]},
                "ecosystem_recovery.json": {"programs": [{"status": "active", "restored": True}, {"status": "idle", "restored": False}]},
                "humanitarian_operations.json": {"operations": [{"coordinated": True, "priority": "urgent"}, {"coordinated": False, "priority": "normal"}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.planetary_humanitarian_tools.PLANETARY_HUMANITARIAN_DIR", root):
                self.assertIn("Diverse populations: 1", synthetic_society_simulation())
                self.assertIn("Equitable plans: 1", ai_assisted_civilization_planning())
                self.assertIn("Constrained systems: 1", planetary_scale_optimization_ai())
                self.assertIn("Stressed resources: 1", sustainable_resource_balancing_engine())
                self.assertIn("High-risk interventions: 1", climate_intervention_simulation())
                self.assertIn("Degraded zones: 1", ocean_monitoring_intelligence())
                self.assertIn("Threatened habitats: 1", wildlife_preservation_ai())
                self.assertIn("Declining forecasts: 1", biodiversity_prediction_system())
                self.assertIn("Restored programs: 1", ecosystem_recovery_planner())
                self.assertIn("Urgent operations: 1", ai_humanitarian_operations_layer())

    def test_routes_cover_771_to_780(self):
        for phase in range(771, 781):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
