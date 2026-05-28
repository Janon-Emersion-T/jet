import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.diplomatic_resilience_tools import *


class DiplomaticResilienceTests(unittest.TestCase):
    def test_diplomatic_resilience_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "diplomatic_simulation.json": {"dialogues": [{"simulated": True, "tense": True}, {"simulated": False, "tense": False}]},
                "consensus_governance.json": {"councils": [{"consensus": True, "fractured": True}, {"consensus": False, "fractured": False}]},
                "policy_consequence.json": {"policies": [{"predicted": True, "inequitable": True}, {"predicted": False, "inequitable": False}]},
                "social_stability_optimizer.json": {"optimizers": [{"stabilized": True, "brittle": True}, {"stabilized": False, "brittle": False}]},
                "trust_propagation.json": {"channels": [{"trusted": True, "weak": True}, {"trusted": False, "weak": False}]},
                "cognitive_fusion.json": {"domains": [{"fused": True, "noisy": True}, {"fused": False, "noisy": False}]},
                "meta_learning_substrate.json": {"substrates": [{"learning": True, "drifting": True}, {"learning": False, "drifting": False}]},
                "recursive_planning_network.json": {"nodes": [{"recursive": True, "overloaded": True}, {"recursive": False, "overloaded": False}]},
                "adaptive_law_simulator.json": {"statutes": [{"simulated": True, "conflicted": True}, {"simulated": False, "conflicted": False}]},
                "resilience_cognition_layer.json": {"layers": [{"resilient": True, "fragmented": True}, {"resilient": False, "fragmented": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.diplomatic_resilience_tools.DIPLOMATIC_RESILIENCE_DIR", root):
                self.assertIn("Tense dialogues: 1", infinite_context_diplomatic_simulation_engine())
                self.assertIn("Fractured councils: 1", human_machine_consensus_governance_ai())
                self.assertIn("Inequitable outcomes: 1", autonomous_policy_consequence_predictor())
                self.assertIn("Brittle optimizers: 1", recursive_social_stability_optimizer())
                self.assertIn("Weak channels: 1", universal_trust_propagation_framework())
                self.assertIn("Noisy domains: 1", cross_domain_cognitive_fusion_engine())
                self.assertIn("Drifting substrates: 1", autonomous_meta_learning_substrate())
                self.assertIn("Overloaded nodes: 1", infinite_scale_recursive_planning_network())
                self.assertIn("Conflicted statutes: 1", planetary_adaptive_law_simulator())
                self.assertIn("Fragmented layers: 1", distributed_resilience_cognition_layer())

    def test_routes_cover_1011_to_1020(self):
        for phase in range(1011, 1021):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
