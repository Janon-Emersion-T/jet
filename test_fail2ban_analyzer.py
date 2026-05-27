import tempfile
import unittest
from pathlib import Path

from core.routes.security_routes import handle_security_routes
from tools.fail2ban_analyzer_tools import analyze_fail2ban, fail2ban_analyzer


class Fail2banAnalyzerTests(unittest.TestCase):
    def test_detects_weak_sshd_jail_configuration(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "jail.local").write_text(
                "[sshd]\nenabled = false\nmaxretry = 12\nbantime = 60\nignoreip = 0.0.0.0/0\n",
                encoding="utf-8",
            )
            _, findings, files_reviewed, error = analyze_fail2ban(root)
        self.assertIsNone(error)
        self.assertEqual(files_reviewed, 1)
        self.assertEqual(len(findings), 4)
        self.assertTrue(any(item.directive == "enabled" for item in findings))

    def test_hardened_sshd_jail_has_no_configured_indicator(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "jail.local").write_text(
                "[sshd]\nenabled = true\nmaxretry = 3\nbantime = 1h\nignoreip = 127.0.0.1\n",
                encoding="utf-8",
            )
            report = fail2ban_analyzer(root)
        self.assertIn("Configuration files reviewed: 1", report)
        self.assertIn("Review points: 0", report)

    def test_route_exposes_phase_365_help(self):
        report = handle_security_routes("365 help", "365 help", "")
        self.assertIn("FAIL2BAN ANALYZER COMMANDS - PHASE 365", report)


if __name__ == "__main__":
    unittest.main()
