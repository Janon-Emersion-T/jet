import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.trust_observability_tools import *


class TrustObservabilityTests(unittest.TestCase):
    def test_trust_observability_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "agent_memory_vault.json": {"vault_segments": [{"encrypted": True, "exposed": True}, {"encrypted": False, "exposed": False}]},
                "knowledge_constitution.json": {"knowledge_charters": [{"codified": True, "inconsistent": True}, {"codified": False, "inconsistent": False}]},
                "trust_boundary_manager.json": {"trust_boundaries": [{"isolated": True, "porous": True}, {"isolated": False, "porous": False}]},
                "permission_negotiation_engine.json": {"permission_requests": [{"justified": True, "overbroad": True}, {"justified": False, "overbroad": False}]},
                "risk_containment_layer.json": {"containment_rules": [{"contained": True, "leaking": True}, {"contained": False, "leaking": False}]},
                "action_insurance_framework.json": {"insurance_policies": [{"covered": True, "uninsured": True}, {"covered": False, "uninsured": False}]},
                "reversible_automation_architecture.json": {"automation_paths": [{"reversible": True, "irreversible": True}, {"reversible": False, "irreversible": False}]},
                "rollback_intelligence.json": {"rollback_strategies": [{"ready": True, "partial": True}, {"ready": False, "partial": False}]},
                "audit_trail_explainer.json": {"audit_entries": [{"explained": True, "opaque": True}, {"explained": False, "opaque": False}]},
                "observability_brain.json": {"observability_surfaces": [{"visible": True, "blind": True}, {"visible": False, "blind": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.trust_observability_tools.TRUST_OBSERVABILITY_DIR", root):
                self.assertIn("Exposed segments: 1", encrypted_agent_memory_vault())
                self.assertIn("Inconsistent charters: 1", personal_knowledge_constitution())
                self.assertIn("Porous boundaries: 1", autonomous_trust_boundary_manager())
                self.assertIn("Overbroad requests: 1", dynamic_permission_negotiation_engine())
                self.assertIn("Leaking rules: 1", runtime_risk_containment_layer())
                self.assertIn("Uninsured policies: 1", agent_action_insurance_framework())
                self.assertIn("Irreversible paths: 1", reversible_automation_architecture())
                self.assertIn("Partial strategies: 1", system_wide_rollback_intelligence())
                self.assertIn("Opaque entries: 1", autonomous_audit_trail_explainer())
                self.assertIn("Blind surfaces: 1", full_stack_observability_brain())

    def test_routes_cover_1511_to_1520(self):
        for phase in range(1511, 1521):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
