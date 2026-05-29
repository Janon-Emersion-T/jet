import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.civic_justice_tools import *


class CivicJusticeTests(unittest.TestCase):
    def test_civic_justice_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "diplomacy_coordination.json": {"dialogues": [{"coordinated": True, "tense": True}, {"coordinated": False, "tense": False}]},
                "treaty_negotiation.json": {"treaties": [{"negotiated": True, "blocked": True}, {"negotiated": False, "blocked": False}]},
                "resource_peace.json": {"compacts": [{"stabilized": True, "contested": True}, {"stabilized": False, "contested": False}]},
                "planetary_governance.json": {"institutions": [{"coordinated": True, "captured": True}, {"coordinated": False, "captured": False}]},
                "constitutional_evolution.json": {"constitutions": [{"evolving": True, "unstable": True}, {"evolving": False, "unstable": False}]},
                "civic_intelligence.json": {"civic_nodes": [{"informed": True, "disconnected": True}, {"informed": False, "disconnected": False}]},
                "democratic_participation.json": {"electorates": [{"engaged": True, "excluded": True}, {"engaged": False, "excluded": False}]},
                "ethical_legislation.json": {"bills": [{"simulated": True, "harmful": True}, {"simulated": False, "harmful": False}]},
                "justice_harmonization.json": {"jurisdictions": [{"harmonized": True, "inequitable": True}, {"harmonized": False, "inequitable": False}]},
                "legal_reasoning.json": {"cases": [{"reasoned": True, "ambiguous": True}, {"reasoned": False, "ambiguous": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.civic_justice_tools.CIVIC_JUSTICE_DIR", root):
                self.assertIn("Tense dialogues: 1", universal_diplomacy_coordination_ai())
                self.assertIn("Blocked treaties: 1", adaptive_treaty_negotiation_engine())
                self.assertIn("Contested compacts: 1", autonomous_resource_peace_framework())
                self.assertIn("Captured institutions: 1", infinite_scale_planetary_governance_substrate())
                self.assertIn("Unstable constitutions: 1", recursive_constitutional_evolution_engine())
                self.assertIn("Disconnected civic nodes: 1", universal_civic_intelligence_network())
                self.assertIn("Excluded electorates: 1", adaptive_democratic_participation_ai())
                self.assertIn("Harmful bills: 1", autonomous_ethical_legislation_simulator())
                self.assertIn("Inequitable jurisdictions: 1", infinite_scale_justice_harmonization_layer())
                self.assertIn("Ambiguous cases: 1", recursive_legal_reasoning_substrate())

    def test_routes_cover_1141_to_1150(self):
        for phase in range(1141, 1151):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
