import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.ops_center_tools import (
    ai_operations_center_dashboard,
    ai_task_dependency_graph,
    department_specific_ai_agents,
    global_event_stream_processor,
)


class OpsCenterTests(unittest.TestCase):
    def test_department_dashboard_stream_and_graph_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "departments.json").write_text(
                json.dumps({"departments": [{"name": "sales", "agent_enabled": True}, {"name": "hr", "agent_enabled": False}]}),
                encoding="utf-8",
            )
            (root / "dashboard.json").write_text(
                json.dumps({"widgets": [{"name": "health"}, {"name": "queue"}], "alerts": [{"severity": "high"}]}),
                encoding="utf-8",
            )
            (root / "event_streams.json").write_text(
                json.dumps({"streams": [{"consumers": 2, "lag": 0}, {"consumers": 1, "lag": 4}]}),
                encoding="utf-8",
            )
            (root / "dependency_graph.json").write_text(
                json.dumps(
                    {
                        "tasks": [{"blocked": True}, {"blocked": False}, {"blocked": False}],
                        "edges": [{"from": 1, "to": 2}, {"from": 2, "to": 3}],
                    }
                ),
                encoding="utf-8",
            )
            with patch("tools.ops_center_tools.OPS_CENTER_DIR", root):
                agents = department_specific_ai_agents()
                dashboard = ai_operations_center_dashboard()
                streams = global_event_stream_processor()
                graph = ai_task_dependency_graph()
        self.assertIn("Departments tracked: 2", agents)
        self.assertIn("Departments with enabled agents: 1", agents)
        self.assertIn("Widgets tracked: 2", dashboard)
        self.assertIn("Active alerts: 1", dashboard)
        self.assertIn("Consumers declared: 3", streams)
        self.assertIn("Lagging streams: 1", streams)
        self.assertIn("Dependency edges: 2", graph)
        self.assertIn("Blocked tasks: 1", graph)

    def test_routes_cover_507_to_510(self):
        for phase in range(507, 511):
            result = handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help")
            self.assertIsNotNone(result, f"missing route for {phase}")


if __name__ == "__main__":
    unittest.main()
