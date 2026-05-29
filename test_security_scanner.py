import tempfile
import unittest
from pathlib import Path

from core.routes.security_routes import handle_security_routes
from tools.security_scanner_tools import scan_vulnerabilities, security_vulnerability_scanner


class SecurityScannerTests(unittest.TestCase):
    def test_scanner_redacts_secret_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "settings.py").write_text("api_key = 'very-secret-api-key-value'\n", encoding="utf-8")
            _, findings, error = scan_vulnerabilities(root)
        self.assertIsNone(error)
        self.assertEqual(findings[0].severity, "CRITICAL")
        self.assertIn("<redacted>", findings[0].evidence)
        self.assertNotIn("very-secret-api-key-value", findings[0].evidence)

    def test_scanner_reports_read_only_code_risks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "danger.py").write_text("eval(user_input)\nrequests.get(url, verify=False)\n", encoding="utf-8")
            report = security_vulnerability_scanner(root)
        self.assertIn("Command execution", report)
        self.assertIn("TLS verification disabled", report)
        self.assertIn("Read-only static heuristic scan", report)

    def test_route_exposes_phase_354_command(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report = security_vulnerability_scanner(root)
        self.assertIn("SECURITY VULNERABILITY SCANNER - PHASE 354", report)
        help_report = handle_security_routes("354 help", "354 help", "")
        self.assertIn("PHASE 354", help_report)


if __name__ == "__main__":
    unittest.main()
