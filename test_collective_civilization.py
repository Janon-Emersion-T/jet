import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.collective_civilization_tools import *


class CollectiveCivilizationTests(unittest.TestCase):
    def test_collective_civilization_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "democracy_simulation.json": {"constituencies": [{"represented": True, "contested": True}, {"represented": False, "contested": False}]},
                "collective_intelligence.json": {"nodes": [{"status": "connected", "curated": True}, {"status": "offline", "curated": False}]},
                "distributed_governance.json": {"councils": [{"delegated": True, "audited": True}, {"delegated": False, "audited": False}]},
                "scientific_council.json": {"briefs": [{"reviewed": True, "consensus": True}, {"reviewed": False, "consensus": False}]},
                "innovation_ecosystem.json": {"programs": [{"status": "active", "funded": True}, {"status": "idle", "funded": False}]},
                "knowledge_sync.json": {"sources": [{"synchronized": True, "status": "lagging"}, {"synchronized": False, "status": "current"}]},
                "planet_scale_index.json": {"corpora": [{"indexed": True, "multilingual": True}, {"indexed": False, "multilingual": False}]},
                "universal_translation.json": {"language_pairs": [{"supported": True, "nuance_checked": True}, {"supported": False, "nuance_checked": False}]},
                "cultural_preservation.json": {"archives": [{"digitized": True, "risk": "high"}, {"digitized": False, "risk": "low"}]},
                "historical_reconstruction.json": {"reconstructions": [{"sourced": True, "disputed": True}, {"sourced": False, "disputed": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.collective_civilization_tools.COLLECTIVE_CIV_DIR", root):
                self.assertIn("Contested constituencies: 1", ai_democracy_simulation())
                self.assertIn("Curated nodes: 1", collective_intelligence_network())
                self.assertIn("Audited councils: 1", distributed_human_ai_governance())
                self.assertIn("Consensus briefs: 1", ai_assisted_scientific_council())
                self.assertIn("Funded programs: 1", autonomous_innovation_ecosystem())
                self.assertIn("Lagging sources: 1", global_knowledge_synchronization())
                self.assertIn("Multilingual corpora: 1", planet_scale_semantic_index())
                self.assertIn("Nuance-checked pairs: 1", universal_translation_framework())
                self.assertIn("High-risk archives: 1", human_cultural_preservation_ai())
                self.assertIn("Disputed reconstructions: 1", historical_reconstruction_engine())

    def test_routes_cover_701_to_710(self):
        for phase in range(701, 711):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
