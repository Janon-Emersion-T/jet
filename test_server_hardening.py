import tempfile
import unittest
from pathlib import Path

from core.routes.security_routes import handle_security_routes
from tools.server_hardening_tools import assess_server_hardening, server_hardening_advisor


class ServerHardeningAdvisorTests(unittest.TestCase):
    def test_detects_weak_sysctl_and_nginx_settings(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "sysctl.conf").write_text(
                "net.ipv4.tcp_syncookies = 0\nkernel.kptr_restrict = 0\n",
                encoding="utf-8",
            )
            (root / "nginx.conf").write_text("server_tokens on;\n", encoding="utf-8")
            _, findings, files_reviewed, error = assess_server_hardening(root)
        self.assertIsNone(error)
        self.assertEqual(files_reviewed, 2)
        self.assertEqual(len(findings), 3)
        self.assertTrue(any(item.area == "Nginx" for item in findings))

    def test_hardened_settings_have_no_configured_indicator(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "sysctl.conf").write_text(
                "net.ipv4.ip_forward = 0\nnet.ipv4.tcp_syncookies = 1\nkernel.kptr_restrict = 2\n",
                encoding="utf-8",
            )
            (root / "nginx.conf").write_text("server_tokens off;\n", encoding="utf-8")
            report = server_hardening_advisor(root)
        self.assertIn("Configuration files reviewed: 2", report)
        self.assertIn("Review points: 0", report)

    def test_route_exposes_phase_366_help(self):
        report = handle_security_routes("366 help", "366 help", "")
        self.assertIn("SERVER HARDENING ADVISOR COMMANDS - PHASE 366", report)


if __name__ == "__main__":
    unittest.main()
