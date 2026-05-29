import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.workspace_isolation_tools import ai_workspace_isolation


class WorkspaceIsolationTests(unittest.TestCase):
    def test_workspace_isolation_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "workspaces.json").write_text(
                json.dumps(
                    {
                        "workspaces": [
                            {"name": "client-a", "isolated": True, "shared_tools": False, "policy": "strict"},
                            {"name": "internal-rnd", "isolated": True, "shared_tools": True, "policy": "balanced"},
                            {"name": "shared-lab", "isolated": False, "shared_tools": True, "policy": "balanced"},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            with patch("tools.workspace_isolation_tools.ISOLATION_DIR", root):
                report = ai_workspace_isolation()
        self.assertIn("Workspaces tracked: 3", report)
        self.assertIn("Isolated workspaces: 2", report)
        self.assertIn("Shared-tool workspaces: 2", report)
        self.assertIn("Policy sets: balanced, strict", report)

    def test_route_covers_506(self):
        result = handle_ai_operations_routes("506 help", "506 help", "506 help")
        self.assertIsNotNone(result)
        self.assertIn("PHASE 506", result)


if __name__ == "__main__":
    unittest.main()
