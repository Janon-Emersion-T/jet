import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.jarvis_platform_tools import (
    enterprise_grade_jarvis_os,
    human_ai_collaborative_workspace,
    unified_cognitive_dashboard,
)


class JarvisPlatformTests(unittest.TestCase):
    def test_platform_dashboard_and_workspace_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "jarvis_os.json").write_text(
                json.dumps({"services": [{"name": "router"}], "controls": [{"name": "approval"}]}),
                encoding="utf-8",
            )
            (root / "dashboard.json").write_text(
                json.dumps({"panels": [{"name": "health"}], "signals": [{"name": "memory"}, {"name": "risk"}]}),
                encoding="utf-8",
            )
            (root / "workspace.json").write_text(
                json.dumps({"spaces": [{"people": 3}, {"people": 2}]}),
                encoding="utf-8",
            )
            with patch("tools.jarvis_platform_tools.PLATFORM_DIR", root):
                platform = enterprise_grade_jarvis_os()
                dashboard = unified_cognitive_dashboard()
                workspace = human_ai_collaborative_workspace()
        self.assertIn("Core services: 1", platform)
        self.assertIn("Governance controls: 1", platform)
        self.assertIn("Signals aggregated: 2", dashboard)
        self.assertIn("Human collaborators represented: 5", workspace)

    def test_routes_cover_493_to_497(self):
        for phase in range(493, 498):
            result = handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help")
            self.assertIsNotNone(result, f"missing route for {phase}")


if __name__ == "__main__":
    unittest.main()
