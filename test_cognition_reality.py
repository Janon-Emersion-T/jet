import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.cognition_reality_tools import *


class CognitionRealityTests(unittest.TestCase):
    def test_cognition_reality_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "ethical_reasoning_network.json": {"nodes": [{"status": "active", "disputed": True}, {"status": "idle", "disputed": False}]},
                "planetary_health.json": {"indicators": [{"monitored": True, "status": "critical"}, {"monitored": False, "status": "stable"}]},
                "civilization_runtime.json": {"runtimes": [{"running": True, "unstable": True}, {"running": False, "unstable": False}]},
                "semantic_cognition.json": {"layers": [{"aligned": True, "noisy": True}, {"aligned": False, "noisy": False}]},
                "adaptive_substrate.json": {"substrates": [{"adaptive": True, "fractured": True}, {"adaptive": False, "fractured": False}]},
                "infinite_context_reasoning.json": {"contexts": [{"retained": True, "overloaded": True}, {"retained": False, "overloaded": False}]},
                "human_transcendence.json": {"experiments": [{"sandboxed": True, "risk": "high"}, {"sandboxed": False, "risk": "low"}]},
                "cognition_mesh.json": {"meshes": [{"interoperable": True, "drifted": True}, {"interoperable": False, "drifted": False}]},
                "recursive_planning.json": {"plans": [{"recursive": True, "unstable": True}, {"recursive": False, "unstable": False}]},
                "reality_model_refinement.json": {"models": [{"refined": True, "mismatched": True}, {"refined": False, "mismatched": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.cognition_reality_tools.COGNITION_REALITY_DIR", root):
                self.assertIn("Disputed nodes: 1", global_ethical_reasoning_network())
                self.assertIn("Critical indicators: 1", autonomous_planetary_health_monitor())
                self.assertIn("Unstable runtimes: 1", civilization_scale_simulation_runtime())
                self.assertIn("Noisy layers: 1", universal_semantic_cognition_layer())
                self.assertIn("Fractured substrates: 1", distributed_adaptive_intelligence_substrate())
                self.assertIn("Overloaded contexts: 1", infinite_context_reasoning_framework())
                self.assertIn("High-risk experiments: 1", ai_assisted_human_transcendence_sandbox())
                self.assertIn("Drifted meshes: 1", universal_interoperability_cognition_mesh())
                self.assertIn("Unstable plans: 1", planetary_scale_recursive_planning_ai())
                self.assertIn("Mismatched models: 1", autonomous_reality_model_refinement_system())

    def test_routes_cover_931_to_940(self):
        for phase in range(931, 941):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
