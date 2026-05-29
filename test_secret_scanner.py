import tempfile
import unittest
from pathlib import Path

from core.routes.security_routes import handle_security_routes
from tools.secret_scanner_tools import scan_secrets, secret_scanner


class SecretScannerTests(unittest.TestCase):
    def test_detects_and_redacts_password_and_private_key(self):
        password = "verySensitiveDatabasePassword"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".env").write_text(f'DB_PASSWORD="{password}"\n', encoding="utf-8")
            (root / "deploy.key").write_text(
                "-----BEGIN OPENSSH PRIVATE KEY-----\nexample\n",
                encoding="utf-8",
            )
            _, findings, error = scan_secrets(root)
            report = secret_scanner(root)
        self.assertIsNone(error)
        self.assertTrue(any(item.secret_type == "Embedded credential assignment" for item in findings))
        self.assertTrue(any(item.secret_type == "Private key material" for item in findings))
        self.assertNotIn(password, report)
        self.assertIn("<redacted-secret>", report)

    def test_environment_reference_is_not_flagged(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "settings.py").write_text("password = os.environ['DB_PASSWORD']\n", encoding="utf-8")
            report = secret_scanner(root)
        self.assertIn("Potential secrets: 0", report)

    def test_route_exposes_phase_362_help(self):
        report = handle_security_routes("362 help", "362 help", "")
        self.assertIn("SECRET SCANNER COMMANDS - PHASE 362", report)


if __name__ == "__main__":
    unittest.main()
