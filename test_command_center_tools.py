import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.command_center_tools import *


class CommandCenterToolsTests(unittest.TestCase):
    def test_command_center_tools_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "operations_cockpit.json": {"cockpit_panels": [{"healthy": True, "missing": True}, {"healthy": False, "missing": False}]},
                "multi_project_command_center.json": {"project_views": [{"coordinated": True, "fragmented": True}, {"coordinated": False, "fragmented": False}]},
                "developer_productivity_intelligence.json": {"productivity_signals": [{"useful": True, "noisy": True}, {"useful": False, "noisy": False}]},
                "autonomous_backlog_grooming.json": {"backlog_items": [{"triaged": True, "stale": True}, {"triaged": False, "stale": False}]},
                "self_prioritizing_task_engine.json": {"task_routes": [{"prioritized": True, "misranked": True}, {"prioritized": False, "misranked": False}]},
                "requirement_ambiguity_detector.json": {"requirements": [{"clear": True, "ambiguous": True}, {"clear": False, "ambiguous": False}]},
                "specification_completeness_scorer.json": {"spec_sections": [{"complete": True, "missing": True}, {"complete": False, "missing": False}]},
                "client_brief_intelligence.json": {"briefs": [{"well-scoped": True, "vague": True}, {"well-scoped": False, "vague": False}]},
                "proposal_to_code_pipeline.json": {"delivery_paths": [{"connected": True, "broken": True}, {"connected": False, "broken": False}]},
                "contract_to_delivery_tracker.json": {"delivery_tracks": [{"aligned": True, "drifting": True}, {"aligned": False, "drifting": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.command_center_tools.COMMAND_CENTER_DIR", root):
                self.assertIn("Missing panels: 1", ai_operations_cockpit())
                self.assertIn("Fragmented views: 1", multi_project_command_center())
                self.assertIn("Noisy signals: 1", developer_productivity_intelligence())
                self.assertIn("Stale items: 1", autonomous_backlog_grooming())
                self.assertIn("Misranked routes: 1", self_prioritizing_task_engine())
                self.assertIn("Ambiguous requirements: 1", requirement_ambiguity_detector())
                self.assertIn("Missing sections: 1", specification_completeness_scorer())
                self.assertIn("Vague briefs: 1", client_brief_intelligence_layer())
                self.assertIn("Broken paths: 1", proposal_to_code_pipeline())
                self.assertIn("Drifting tracks: 1", contract_to_delivery_tracker())

    def test_routes_cover_1521_to_1530(self):
        for phase in range(1521, 1531):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
