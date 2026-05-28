import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.trust_civic_tools import *


class TrustCivicTests(unittest.TestCase):
    def test_trust_civic_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "archive_preservation.json": {"archives": [{"preserved": True, "fragile": True}, {"preserved": False, "fragile": False}]},
                "language_evolution.json": {"languages": [{"tracked": True, "drifting": True}, {"tracked": False, "drifting": False}]},
                "knowledge_transfer.json": {"cohorts": [{"connected": True, "broken": True}, {"connected": False, "broken": False}]},
                "constitutional_ethics.json": {"clauses": [{"reviewed": True, "conflicted": True}, {"reviewed": False, "conflicted": False}]},
                "planetary_empathy.json": {"simulations": [{"immersive": True, "manipulative": True}, {"immersive": False, "manipulative": False}]},
                "collective_emotional_intelligence.json": {"groups": [{"attuned": True, "strained": True}, {"attuned": False, "strained": False}]},
                "conflict_deescalation.json": {"incidents": [{"deescalated": True, "risk": "high"}, {"deescalated": False, "risk": "low"}]},
                "global_trust.json": {"anchors": [{"verified": True, "weak": True}, {"verified": False, "weak": False}]},
                "truth_consensus.json": {"nodes": [{"converged": True, "disputed": True}, {"converged": False, "disputed": False}]},
                "misinformation_resilience.json": {"campaigns": [{"contained": True, "spreading": True}, {"contained": False, "spreading": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.trust_civic_tools.TRUST_CIVIC_DIR", root):
                self.assertIn("Fragile archives: 1", universal_archive_preservation_layer())
                self.assertIn("Drifting languages: 1", autonomous_language_evolution_tracker())
                self.assertIn("Broken transfer paths: 1", cross_generational_knowledge_transfer_ai())
                self.assertIn("Conflicted clauses: 1", ai_guided_constitutional_ethics_engine())
                self.assertIn("Manipulative simulations: 1", planetary_empathy_simulation_framework())
                self.assertIn("Strained groups: 1", collective_emotional_intelligence_layer())
                self.assertIn("High-risk incidents: 1", human_conflict_de_escalation_ai())
                self.assertIn("Weak anchors: 1", global_trust_infrastructure())
                self.assertIn("Disputed nodes: 1", distributed_truth_consensus_network())
                self.assertIn("Spreading campaigns: 1", autonomous_misinformation_resilience_system())

    def test_routes_cover_901_to_910(self):
        for phase in range(901, 911):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
