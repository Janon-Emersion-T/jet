import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.civilization_kernel_tools import *


class CivilizationKernelTests(unittest.TestCase):
    def test_civilization_kernel_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "synthetic_civilization_lab.json": {"labs": [{"status": "active", "speculative": True}, {"status": "idle", "speculative": False}]},
                "hybrid_strategic_council.json": {"councils": [{"hybrid": True, "conflicted": True}, {"hybrid": False, "conflicted": False}]},
                "discovery_acceleration.json": {"programs": [{"accelerated": True, "thin": True}, {"accelerated": False, "thin": False}]},
                "multi_species_ethics.json": {"species": [{"protected": True, "conflicted": True}, {"protected": False, "conflicted": False}]},
                "knowledge_evolution.json": {"branches": [{"evolved": True, "stale": True}, {"evolved": False, "stale": False}]},
                "cosmic_perspective.json": {"perspectives": [{"expanded": True, "disorienting": True}, {"expanded": False, "disorienting": False}]},
                "collaborative_architecture.json": {"architectures": [{"scaled": True, "fragmented": True}, {"scaled": False, "fragmented": False}]},
                "autonomous_civilization_stack.json": {"stacks": [{"sustained": True, "unstable": True}, {"sustained": False, "unstable": False}]},
                "planetary_operations.json": {"operations": [{"resilient": True, "overloaded": True}, {"resilient": False, "overloaded": False}]},
                "civilization_kernel.json": {"kernels": [{"flourishing": True, "skewed": True}, {"flourishing": False, "skewed": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.civilization_kernel_tools.CIV_KERNEL_DIR", root):
                self.assertIn("Speculative labs: 1", synthetic_civilization_laboratory())
                self.assertIn("Conflicted councils: 1", human_ai_hybrid_strategic_council())
                self.assertIn("Thin programs: 1", universal_discovery_acceleration_engine())
                self.assertIn("Conflicted species: 1", multi_species_ethical_coexistence_ai())
                self.assertIn("Stale branches: 1", autonomous_knowledge_evolution_framework())
                self.assertIn("Disorienting perspectives: 1", ai_driven_cosmic_perspective_simulator())
                self.assertIn("Fragmented architectures: 1", infinite_collaborative_intelligence_architecture())
                self.assertIn("Unstable stacks: 1", self_sustaining_autonomous_civilization_stack())
                self.assertIn("Overloaded operations: 1", hyper_resilient_planetary_operations_ai())
                self.assertIn("Skewed kernels: 1", human_flourishing_civilization_kernel())

    def test_routes_cover_941_to_950(self):
        for phase in range(941, 951):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
