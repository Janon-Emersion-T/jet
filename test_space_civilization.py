import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.space_civilization_tools import *


class SpaceCivilizationTests(unittest.TestCase):
    def test_space_civilization_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "planetary_coordination.json": {"councils": [{"aligned": True, "priority": "urgent"}, {"aligned": False, "priority": "normal"}]},
                "space_colonization.json": {"missions": [{"modeled": True, "constrained": True}, {"modeled": False, "constrained": False}]},
                "habitat_simulation.json": {"habitats": [{"viable": True, "status": "stressed"}, {"viable": False, "status": "stable"}]},
                "interplanetary_logistics.json": {"routes": [{"status": "active", "delayed": True}, {"status": "idle", "delayed": False}]},
                "extraterrestrial_research.json": {"studies": [{"reviewed": True, "sensitive": True}, {"reviewed": False, "sensitive": False}]},
                "biosphere_management.json": {"systems": [{"balanced": True, "status": "fragile"}, {"balanced": False, "status": "stable"}]},
                "long_duration_survival.json": {"plans": [{"resilient": True, "status": "scarce"}, {"resilient": False, "status": "stable"}]},
                "terraforming_simulation.json": {"scenarios": [{"modeled": True, "risk": "high"}, {"modeled": False, "risk": "low"}]},
                "cosmic_data_analysis.json": {"datasets": [{"indexed": True, "anomalous": True}, {"indexed": False, "anomalous": False}]},
                "scientific_archive.json": {"archives": [{"curated": True, "incomplete": True}, {"curated": False, "incomplete": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.space_civilization_tools.SPACE_CIV_DIR", root):
                self.assertIn("Urgent councils: 1", planetary_coordination_framework())
                self.assertIn("Constrained missions: 1", space_colonization_planning_ai())
                self.assertIn("Stressed habitats: 1", autonomous_habitat_simulation())
                self.assertIn("Delayed routes: 1", interplanetary_logistics_engine())
                self.assertIn("Sensitive studies: 1", extraterrestrial_research_assistant())
                self.assertIn("Fragile systems: 1", ai_biosphere_management())
                self.assertIn("Scarcity-flagged plans: 1", long_duration_survival_intelligence())
                self.assertIn("High-risk scenarios: 1", autonomous_terraforming_simulation())
                self.assertIn("Anomalous datasets: 1", cosmic_scale_data_analysis())
                self.assertIn("Incomplete archives: 1", universal_scientific_archive_ai())

    def test_routes_cover_801_to_810(self):
        for phase in range(801, 811):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
