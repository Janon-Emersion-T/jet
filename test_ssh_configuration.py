import tempfile
import unittest
from pathlib import Path

from core.routes.security_routes import handle_security_routes
from tools.ssh_configuration_tools import check_ssh_configuration, ssh_configuration_checker


class SSHConfigurationTests(unittest.TestCase):
    def test_detects_unsafe_sshd_directives(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "sshd_config").write_text(
                "PermitRootLogin yes\nPasswordAuthentication yes\nPermitEmptyPasswords yes\n",
                encoding="utf-8",
            )
            _, findings, files_reviewed, error = check_ssh_configuration(root)
        self.assertIsNone(error)
        self.assertEqual(files_reviewed, 1)
        self.assertEqual(len(findings), 3)
        self.assertTrue(any(item.severity == "critical" for item in findings))

    def test_hardened_sshd_config_has_no_configured_indicator(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "sshd_config").write_text(
                "PermitRootLogin no\nPasswordAuthentication no\nPubkeyAuthentication yes\nX11Forwarding no\n",
                encoding="utf-8",
            )
            report = ssh_configuration_checker(root)
        self.assertIn("Configuration files reviewed: 1", report)
        self.assertIn("Review points: 0", report)

    def test_route_exposes_phase_363_help(self):
        report = handle_security_routes("363 help", "363 help", "")
        self.assertIn("SSH CONFIGURATION CHECKER COMMANDS - PHASE 363", report)


if __name__ == "__main__":
    unittest.main()
