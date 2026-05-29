import tempfile
import unittest
from pathlib import Path

from core.routes.security_routes import handle_security_routes
from tools.firewall_assistant_tools import firewall_assistant, inspect_firewall_configuration


class FirewallAssistantTests(unittest.TestCase):
    def test_detects_permissive_iptables_input_rules(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "iptables.rules").write_text(
                "*filter\n:INPUT ACCEPT [0:0]\n-A INPUT -j ACCEPT\nCOMMIT\n",
                encoding="utf-8",
            )
            _, findings, files_reviewed, error = inspect_firewall_configuration(root)
        self.assertIsNone(error)
        self.assertEqual(files_reviewed, 1)
        self.assertEqual(len(findings), 2)

    def test_default_deny_rules_have_no_configured_indicator(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "iptables.rules").write_text(
                "*filter\n:INPUT DROP [0:0]\n"
                "-A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT\nCOMMIT\n",
                encoding="utf-8",
            )
            report = firewall_assistant(root)
        self.assertIn("Configuration files reviewed: 1", report)
        self.assertIn("Review points: 0", report)

    def test_route_exposes_phase_364_help(self):
        report = handle_security_routes("364 help", "364 help", "")
        self.assertIn("FIREWALL ASSISTANT COMMANDS - PHASE 364", report)


if __name__ == "__main__":
    unittest.main()
