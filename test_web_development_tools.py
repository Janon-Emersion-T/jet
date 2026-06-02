import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.nlp import route_resolver
from core import command_router
from core.patches.proposal_manager import ProposalManager
from core.routing.nlp_route_selector import select_route
from core.routing.route_registry import get_route_modules
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

    def test_route_selector_prefers_web_development_for_build_prompts(self):
        nlp = type(
            "NLP",
            (),
            {
                "normalized_text": "create laravel web application in /var/www/testjarvis",
                "clean_text": "create laravel web application in varwwwtestjarvis",
                "canonical_command": None,
                "intent": "web_development",
                "domain": type("Domain", (), {"domain": "development"})(),
            },
        )()

        decision = select_route(
            "Create a Laravel web application in /var/www/testJarvis",
            nlp,
            get_route_modules(),
        )

        self.assertIsNotNone(decision.module)
        self.assertEqual(decision.module.name, "web_development")

    def test_route_selector_keeps_meta_tag_questions_in_html_knowledge(self):
        nlp = type(
            "NLP",
            (),
            {
                "normalized_text": "explain the meta tag",
                "clean_text": "explain the meta tag",
                "canonical_command": None,
                "intent": "general_chat",
                "domain": type("Domain", (), {"domain": "frontend"})(),
            },
        )()

        decision = select_route("Explain the meta tag", nlp, get_route_modules())

        self.assertIsNotNone(decision.module)
        self.assertEqual(decision.module.name, "html_knowledge")

    def test_route_selector_ignores_html_route_for_meta_in_build_prompt(self):
        nlp = type(
            "NLP",
            (),
            {
                "normalized_text": "create laravel web application with meta tags in /var/www/testjarvis",
                "clean_text": "create laravel web application with meta tags in varwwwtestjarvis",
                "canonical_command": None,
                "intent": "web_development",
                "domain": type("Domain", (), {"domain": "development"})(),
            },
        )()

        decision = select_route(
            "Create a Laravel web application with meta tags in /var/www/testJarvis",
            nlp,
            get_route_modules(),
        )

        self.assertIsNotNone(decision.module)
        self.assertEqual(decision.module.name, "web_development")

    def test_live_intelligence_fallback_is_user_friendly(self):
        with patch("core.command_router.requires_realtime", return_value=True), \
                patch(
                    "core.command_router.get_live_news_context",
                    return_value={
                        "results": [
                            {
                                "type": "error",
                                "message": "Web search failed: 400 Client Error"
                            }
                        ],
                        "summary_context": "Web search failed: 400 Client Error",
                    },
                ):
            response = command_router.route_command("What is the current status of the war in the middle east")

        self.assertIn("couldn't fetch live web updates", response.lower())
        self.assertNotIn("400 client error", response.lower())
        self.assertNotIn("api key", response.lower())

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
