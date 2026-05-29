import tempfile
import unittest
from pathlib import Path

from core.routes.security_routes import handle_security_routes
from tools.csrf_analyzer_tools import analyze_csrf, csrf_analyzer


class CSRFAnalyzerTests(unittest.TestCase):
    def test_finds_unprotected_blade_form(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "edit.blade.php").write_text(
                '<form method="post" action="/profile"><button>Save</button></form>\n',
                encoding="utf-8",
            )
            _, findings, error = analyze_csrf(root)
        self.assertIsNone(error)
        self.assertEqual(findings[0].category, "Blade form missing CSRF token")

    def test_protected_blade_form_is_not_flagged(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "safe.blade.php").write_text(
                '<form method="post">@csrf<button>Save</button></form>\n',
                encoding="utf-8",
            )
            report = csrf_analyzer(root)
        self.assertIn("Review points: 0", report)

    def test_route_exposes_phase_357_help(self):
        report = handle_security_routes("357 help", "357 help", "")
        self.assertIn("CSRF ANALYZER COMMANDS - PHASE 357", report)


if __name__ == "__main__":
    unittest.main()
