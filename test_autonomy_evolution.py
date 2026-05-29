import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.autonomy_evolution_tools import (
    ai_civilization_sandbox,
    autonomous_learning_curriculum,
    recursive_self_improvement_framework,
)


class AutonomyEvolutionTests(unittest.TestCase):
    def test_civilization_curriculum_and_improvement_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "civilization.json").write_text(
                json.dumps({"agents": [{"id": 1}, {"id": 2}], "institutions": [{"name": "council"}]}),
                encoding="utf-8",
            )
            (root / "curriculum.json").write_text(
                json.dumps({"lessons": [{"track": "routing"}, {"track": "safety"}]}),
                encoding="utf-8",
            )
            (root / "self_improvement.json").write_text(
                json.dumps({"experiments": [{"status": "planned"}, {"status": "done"}]}),
                encoding="utf-8",
            )
            with patch("tools.autonomy_evolution_tools.AUTONOMY_DIR", root):
                civilization = ai_civilization_sandbox()
                curriculum = autonomous_learning_curriculum()
                improvement = recursive_self_improvement_framework()
        self.assertIn("Agents modeled: 2", civilization)
        self.assertIn("Institutions modeled: 1", civilization)
        self.assertIn("Lessons tracked: 2", curriculum)
        self.assertIn("Open experiments: 1", improvement)

    def test_routes_cover_481_to_485(self):
        for phase in range(481, 486):
            result = handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help")
            self.assertIsNotNone(result, f"missing route for {phase}")


if __name__ == "__main__":
    unittest.main()
