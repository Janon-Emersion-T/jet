import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.security_governance_batch_tools import *


class SecurityGovernanceBatchTests(unittest.TestCase):
    def test_security_governance_batch_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "ai_security_review_board.json": {"review_items": [{"reviewed": True, "escalated": True}, {"reviewed": False, "escalated": False}]},
                "dependency_license_auditor.json": {"license_checks": [{"clear": True, "conflicting": True}, {"clear": False, "conflicting": False}]},
                "open_source_risk_scorer.json": {"package_profiles": [{"low-risk": True, "high-risk": True}, {"low-risk": False, "high-risk": False}]},
                "package_update_strategy.json": {"update_paths": [{"safe": True, "disruptive": True}, {"safe": False, "disruptive": False}]},
                "cve_impact_mapper.json": {"cve_matches": [{"contextualized": True, "exposed": True}, {"contextualized": False, "exposed": False}]},
                "secret_rotation_planner.json": {"rotation_paths": [{"planned": True, "stale": True}, {"planned": False, "stale": False}]},
                "credential_hygiene_assistant.json": {"credential_profiles": [{"healthy": True, "risky": True}, {"healthy": False, "risky": False}]},
                "ssh_key_inventory_manager.json": {"ssh_keys": [{"tracked": True, "unknown": True}, {"tracked": False, "unknown": False}]},
                "firewall_policy_analyzer.json": {"firewall_rules": [{"restricted": True, "permissive": True}, {"restricted": False, "permissive": False}]},
                "server_exposure_mapper.json": {"exposure_paths": [{"contained": True, "exposed": True}, {"contained": False, "exposed": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.security_governance_batch_tools.SECURITY_GOVERNANCE_BATCH_DIR", root):
                self.assertIn("Escalated items: 1", ai_security_review_board())
                self.assertIn("Conflicting checks: 1", dependency_license_auditor())
                self.assertIn("High-risk packages: 1", open_source_risk_scorer())
                self.assertIn("Disruptive paths: 1", package_update_strategy_engine())
                self.assertIn("Exposed matches: 1", cve_impact_mapper())
                self.assertIn("Stale paths: 1", secret_rotation_planner())
                self.assertIn("Risky profiles: 1", credential_hygiene_assistant())
                self.assertIn("Unknown keys: 1", ssh_key_inventory_manager())
                self.assertIn("Permissive rules: 1", firewall_policy_analyzer())
                self.assertIn("Exposed paths: 1", server_exposure_mapper())

    def test_routes_cover_1681_to_1690(self):
        for phase in range(1681, 1691):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
