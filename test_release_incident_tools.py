import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.release_incident_tools import *


class ReleaseIncidentToolsTests(unittest.TestCase):
    def test_release_incident_tools_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "release_readiness_gatekeeper.json": {"release_checks": [{"ready": True, "blocked": True}, {"ready": False, "blocked": False}]},
                "deployment_checklist_autopilot.json": {"checklist_items": [{"complete": True, "missing": True}, {"complete": False, "missing": False}]},
                "rollback_drill_assistant.json": {"rollback_runs": [{"practiced": True, "untested": True}, {"practiced": False, "untested": False}]},
                "incident_postmortem_generator.json": {"postmortem_sections": [{"complete": True, "thin": True}, {"complete": False, "thin": False}]},
                "sla_breach_predictor.json": {"sla_windows": [{"safe": True, "at-risk": True}, {"safe": False, "at-risk": False}]},
                "error_budget_tracker.json": {"budget_periods": [{"within-budget": True, "burning": True}, {"within-budget": False, "burning": False}]},
                "uptime_communication_assistant.json": {"incident_updates": [{"clear": True, "unclear": True}, {"clear": False, "unclear": False}]},
                "client_status_page_generator.json": {"status_pages": [{"ready": True, "stale": True}, {"ready": False, "stale": False}]},
                "production_hotfix_planner.json": {"hotfix_plans": [{"controlled": True, "risky": True}, {"controlled": False, "risky": False}]},
                "maintenance_window_scheduler.json": {"maintenance_windows": [{"safe": True, "disruptive": True}, {"safe": False, "disruptive": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.release_incident_tools.RELEASE_INCIDENT_DIR", root):
                self.assertIn("Blocked checks: 1", release_readiness_gatekeeper())
                self.assertIn("Missing items: 1", deployment_checklist_autopilot())
                self.assertIn("Untested runs: 1", rollback_drill_assistant())
                self.assertIn("Thin sections: 1", incident_postmortem_generator())
                self.assertIn("At-risk windows: 1", sla_breach_predictor())
                self.assertIn("Burning periods: 1", error_budget_tracker())
                self.assertIn("Unclear updates: 1", uptime_communication_assistant())
                self.assertIn("Stale pages: 1", client_status_page_generator())
                self.assertIn("Risky plans: 1", production_hotfix_planner())
                self.assertIn("Disruptive windows: 1", safe_maintenance_window_scheduler())

    def test_routes_cover_1671_to_1680(self):
        for phase in range(1671, 1681):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
