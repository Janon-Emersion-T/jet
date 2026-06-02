import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.nlp import route_resolver
from core.patches.proposal_manager import ProposalManager
from core.routes.web_development_routes import handle_web_development_routes
from tools.safe_execution_tools import request_shell_command
from tools.web_development_tools import build_web_development_plan, format_web_development_plan


class WebDevelopmentToolTests(unittest.TestCase):
    def test_plan_detects_target_and_confirmation_needed_when_folder_has_work(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "existing-app"
            target.mkdir()
            (target / "README.md").write_text("existing", encoding="utf-8")

            plan_json = {
                "objective": "Build a Laravel web application",
                "target_path": str(target),
                "stack": ["Laravel", "Blade", "Tailwind", "Alpine", "Vite", "MySQL"],
                "project_type": "new_app",
                "confirmation_needed": False,
                "steps": [
                    {"step": 1, "title": "Install Laravel", "action": "install_laravel_project", "notes": "Create the project", "commands": [], "files": []}
                ],
                "risks": [],
                "validation": ["Run the build"]
            }

            with patch("tools.web_development_tools.ask_brain", return_value=json.dumps(plan_json)):
                plan = build_web_development_plan("Create a Laravel web application in " + str(target))

        self.assertEqual(plan["target_path"], str(target))
        self.assertTrue(plan["confirmation_needed"])
        self.assertEqual(plan["project_type"], "new_app")

    def test_plan_rendering_includes_steps(self):
        text = format_web_development_plan(
            {
                "objective": "Build a Laravel app",
                "target_path": "/var/www/testJarvis",
                "project_type": "new_app",
                "confirmation_needed": False,
                "steps": [
                    {"step": 1, "title": "Install Laravel", "action": "install_laravel_project", "notes": "Create the project", "commands": ["composer create-project"], "files": []}
                ],
                "risks": ["Existing work could be overwritten."],
                "validation": ["Run php artisan test"],
            }
        )

        self.assertIn("WEB DEVELOPMENT PLAN", text)
        self.assertIn("Install Laravel", text)
        self.assertIn("Existing work could be overwritten.", text)

    def test_route_resolver_sends_laravel_to_web_development(self):
        self.assertEqual(
            route_resolver.resolve_route_hint("web_development", "create laravel web application", {}),
            "web_development",
        )
        self.assertEqual(
            route_resolver.resolve_route_hint("project_analysis", "blade tailwind alpine vite", {}),
            "web_development",
        )

    def test_web_development_route_returns_plan_or_execution(self):
        with patch("core.routes.web_development_routes.build_web_development_plan") as plan_mock:
            plan_mock.return_value = {
                "objective": "Build a Laravel app",
                "target_path": "/var/www/testJarvis",
                "project_type": "plan",
                "confirmation_needed": False,
                "steps": [],
                "risks": [],
                "validation": [],
            }

            result = handle_web_development_routes(
                "Plan a Laravel app",
                "plan a Laravel app",
                "plan a Laravel app",
            )

        self.assertIn("WEB DEVELOPMENT PLAN", result)

    def test_shell_command_approval_blocks_dangerous_commands(self):
        result = request_shell_command("rm -rf storage")
        self.assertIn("blocked", result.lower())

    def test_proposal_manager_apply_requires_confirmation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            file_path = root / "sample.txt"
            file_path.write_text("old", encoding="utf-8")

            manager = ProposalManager(root=str(root))
            proposal = manager.create_proposal("sample.txt", "new", "update sample")

            preview = manager.apply(proposal["id"], confirmed=False)
            self.assertIn("Confirm-before-write", preview)

            applied = manager.apply(proposal["id"], confirmed=True)
            self.assertIn("Applied proposal", applied)
            self.assertEqual(file_path.read_text(encoding="utf-8"), "new")


if __name__ == "__main__":
    unittest.main()
