import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.executive_modes_tools import *


class ExecutiveModesToolsTests(unittest.TestCase):
    def test_executive_modes_tools_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "scope_creep_detector.json": {"scope_changes": [{"controlled": True, "creeping": True}, {"controlled": False, "creeping": False}]},
                "project_profitability_analyzer.json": {"project_margins": [{"profitable": True, "loss-making": True}, {"profitable": False, "loss-making": False}]},
                "delivery_risk_predictor.json": {"delivery_paths": [{"low-risk": True, "high-risk": True}, {"low-risk": False, "high-risk": False}]},
                "deadline_recovery_planner.json": {"recovery_plans": [{"recoverable": True, "slipping": True}, {"recoverable": False, "slipping": False}]},
                "resource_allocation_optimizer.json": {"allocation_models": [{"balanced": True, "overloaded": True}, {"balanced": False, "overloaded": False}]},
                "ai_project_manager_mode.json": {"pm_workflows": [{"organized": True, "unclear": True}, {"organized": False, "unclear": False}]},
                "ai_cto_mode.json": {"technology_tracks": [{"sound": True, "risky": True}, {"sound": False, "risky": False}]},
                "ai_cfo_mode.json": {"finance_views": [{"clear": True, "opaque": True}, {"clear": False, "opaque": False}]},
                "ai_coo_mode.json": {"operations_tracks": [{"smooth": True, "blocked": True}, {"smooth": False, "blocked": False}]},
                "founder_command_dashboard.json": {"command_panels": [{"actionable": True, "noisy": True}, {"actionable": False, "noisy": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.executive_modes_tools.EXECUTIVE_MODES_DIR", root):
                self.assertIn("Creeping changes: 1", scope_creep_detector())
                self.assertIn("Loss-making projects: 1", project_profitability_analyzer())
                self.assertIn("High-risk paths: 1", delivery_risk_predictor())
                self.assertIn("Slipping plans: 1", deadline_recovery_planner())
                self.assertIn("Overloaded models: 1", resource_allocation_optimizer())
                self.assertIn("Unclear workflows: 1", ai_project_manager_mode())
                self.assertIn("Risky tracks: 1", ai_cto_mode())
                self.assertIn("Opaque views: 1", ai_cfo_mode())
                self.assertIn("Blocked tracks: 1", ai_coo_mode())
                self.assertIn("Noisy panels: 1", founder_command_dashboard())

    def test_routes_cover_1531_to_1540(self):
        for phase in range(1531, 1541):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
