import tempfile
import unittest
from pathlib import Path

from core.routes.security_routes import handle_security_routes
from tools.api_token_leak_tools import api_token_leak_detector, detect_api_token_leaks


class APITokenLeakTests(unittest.TestCase):
    def test_detects_and_redacts_known_api_tokens(self):
        token = "ghp_abcdefghijklmnopqrstuvwxyz123456"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".env").write_text(f"GITHUB_TOKEN={token}\n", encoding="utf-8")
            _, findings, error = detect_api_token_leaks(root)
            report = api_token_leak_detector(root)
        self.assertIsNone(error)
        self.assertEqual(findings[0].provider, "GitHub")
        self.assertIn("<redacted-api-token>", report)
        self.assertNotIn(token, report)

    def test_environment_reference_is_not_flagged(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "client.py").write_text("api_token = os.environ['API_TOKEN']\n", encoding="utf-8")
            report = api_token_leak_detector(root)
        self.assertIn("Potential leaks: 0", report)

    def test_route_exposes_phase_361_help(self):
        report = handle_security_routes("361 help", "361 help", "")
        self.assertIn("API TOKEN LEAK DETECTOR COMMANDS - PHASE 361", report)


if __name__ == "__main__":
    unittest.main()
