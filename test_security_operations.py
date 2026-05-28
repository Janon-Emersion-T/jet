import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.security_operations_tools import (
    ai_forensic_investigation_assistant,
    ai_penetration_testing_sandbox,
    ai_soc_dashboard,
    autonomous_incident_containment,
    blue_team_defense_assistant,
    compliance_monitoring_framework,
    predictive_infrastructure_maintenance,
    red_team_simulation_engine,
)


class SecurityOperationsTests(unittest.TestCase):
    def test_security_operations_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            files = {
                "forensics.json": {"cases": [{"status": "active", "evidence_preserved": True}, {"status": "closed", "evidence_preserved": False}]},
                "incident_containment.json": {"actions": [{"mode": "automatic", "result": "isolated"}, {"mode": "manual", "result": "observed"}]},
                "predictive_maintenance.json": {"assets": [{"risk": "high", "maintenance_scheduled": True}, {"risk": "low", "maintenance_scheduled": False}]},
                "soc_dashboard.json": {"alerts": [{"status": "open", "severity": "critical"}, {"status": "closed", "severity": "medium"}]},
                "pentest_sandbox.json": {"scenarios": [{"isolated": True, "status": "completed"}, {"isolated": False, "status": "draft"}]},
                "red_team.json": {"exercises": [{"adversarial_chain": True, "status": "validated"}, {"adversarial_chain": False, "status": "draft"}]},
                "blue_team.json": {"playbooks": [{"tuned": True, "automated": True}, {"tuned": False, "automated": False}]},
                "compliance_monitoring.json": {"checks": [{"status": "failing", "continuous": True}, {"status": "passing", "continuous": False}]},
            }
            for name, payload in files.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.security_operations_tools.SECURITY_OPS_DIR", root):
                self.assertIn("Cases tracked: 2", ai_forensic_investigation_assistant())
                self.assertIn("Automatic actions: 1", autonomous_incident_containment())
                self.assertIn("High-risk assets: 1", predictive_infrastructure_maintenance())
                self.assertIn("Critical alerts: 1", ai_soc_dashboard())
                self.assertIn("Completed scenarios: 1", ai_penetration_testing_sandbox())
                self.assertIn("Validated exercises: 1", red_team_simulation_engine())
                self.assertIn("Automated playbooks: 1", blue_team_defense_assistant())
                self.assertIn("Failing checks: 1", compliance_monitoring_framework())

    def test_routes_cover_536_to_543(self):
        for phase in range(536, 544):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
