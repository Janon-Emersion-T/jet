import tempfile
import unittest
from pathlib import Path

from core.routes.security_routes import handle_security_routes
from tools.auth_bypass_tools import analyze_auth_bypass, auth_bypass_analyzer


class AuthBypassAnalyzerTests(unittest.TestCase):
    def test_detects_removed_laravel_auth_and_enabled_bypass_switch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "routes.php").write_text(
                "Route::post('/admin/users', fn () => 'ok')->withoutMiddleware('auth');\n",
                encoding="utf-8",
            )
            (root / "settings.py").write_text("ALLOW_UNAUTHENTICATED = True\n", encoding="utf-8")
            _, findings, error = analyze_auth_bypass(root)
        self.assertIsNone(error)
        self.assertTrue(any(item.framework == "Laravel" for item in findings))
        self.assertTrue(any(item.framework == "Application config" for item in findings))

    def test_authenticated_route_has_no_configured_indicator(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "routes.php").write_text(
                "Route::post('/admin/users', fn () => 'ok')->middleware('auth');\n",
                encoding="utf-8",
            )
            report = auth_bypass_analyzer(root)
        self.assertIn("Review points: 0", report)

    def test_route_exposes_phase_359_help(self):
        report = handle_security_routes("359 help", "359 help", "")
        self.assertIn("AUTH BYPASS ANALYZER COMMANDS - PHASE 359", report)


if __name__ == "__main__":
    unittest.main()
