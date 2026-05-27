import tempfile
import unittest
from pathlib import Path

from core.routes.security_routes import handle_security_routes
from tools.owasp_analyzer_tools import analyze_owasp, owasp_analyzer


class OWASPAnalyzerTests(unittest.TestCase):
    def test_classifies_injection_and_misconfiguration(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "app.py").write_text(
                "eval(user_input)\nDEBUG = True\n",
                encoding="utf-8",
            )
            _, findings, error = analyze_owasp(root)
        self.assertIsNone(error)
        self.assertEqual(findings[0].category, "A03 Injection")
        self.assertTrue(any(item.category == "A05 Security Misconfiguration" for item in findings))

    def test_redacts_cryptographic_secret_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".env").write_text("TOKEN='token-value-to-hide'\n", encoding="utf-8")
            report = owasp_analyzer(root)
        self.assertIn("A02 Cryptographic Failures", report)
        self.assertIn("<redacted>", report)
        self.assertNotIn("token-value-to-hide", report)

    def test_route_exposes_phase_355_help(self):
        report = handle_security_routes("355 help", "355 help", "")
        self.assertIn("OWASP ANALYZER COMMANDS - PHASE 355", report)


if __name__ == "__main__":
    unittest.main()
