import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.server_ops_governance_tools import *


class ServerOpsGovernanceTests(unittest.TestCase):
    def test_server_ops_governance_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "multi_app_server_inventory.json": {"app_nodes": [{"tracked": True, "unknown": True}, {"tracked": False, "unknown": False}]},
                "domain_server_mapping.json": {"domain_maps": [{"mapped": True, "orphaned": True}, {"mapped": False, "orphaned": False}]},
                "ssl_renewal_intelligence.json": {"certificate_paths": [{"covered": True, "expiring": True}, {"covered": False, "expiring": False}]},
                "dns_propagation_monitor.json": {"dns_checks": [{"settled": True, "lagging": True}, {"settled": False, "lagging": False}]},
                "mail_deliverability_command.json": {"deliverability_signals": [{"healthy": True, "failing": True}, {"healthy": False, "failing": False}]},
                "queue_failure_analyst.json": {"queue_events": [{"healthy": True, "failing": True}, {"healthy": False, "failing": False}]},
                "cron_job_governor.json": {"cron_jobs": [{"tracked": True, "misfiring": True}, {"tracked": False, "misfiring": False}]},
                "storage_permission_fixer.json": {"permission_paths": [{"correct": True, "broken": True}, {"correct": False, "broken": False}]},
                "laravel_route_health.json": {"route_checks": [{"healthy": True, "broken": True}, {"healthy": False, "broken": False}]},
                "cache_invalidation_advisor.json": {"cache_paths": [{"clear": True, "stale": True}, {"clear": False, "stale": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.server_ops_governance_tools.SERVER_OPS_GOVERNANCE_DIR", root):
                self.assertIn("Unknown nodes: 1", multi_app_server_inventory())
                self.assertIn("Orphaned domains: 1", domain_to_server_mapping_brain())
                self.assertIn("Expiring certificates: 1", ssl_renewal_intelligence())
                self.assertIn("Lagging checks: 1", dns_propagation_monitor())
                self.assertIn("Failing signals: 1", mail_deliverability_command_center())
                self.assertIn("Failing events: 1", queue_failure_analyst())
                self.assertIn("Misfiring jobs: 1", cron_job_governor())
                self.assertIn("Broken paths: 1", storage_permission_fixer())
                self.assertIn("Broken routes: 1", laravel_route_health_monitor())
                self.assertIn("Stale paths: 1", cache_invalidation_advisor())

    def test_routes_cover_1611_to_1620(self):
        for phase in range(1611, 1621):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
