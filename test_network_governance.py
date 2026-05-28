import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.network_governance_tools import (
    ai_accountability_tracker,
    ai_network_optimization,
    autonomous_infrastructure_diagnostics,
    autonomous_vpn_management,
    live_topology_visualization,
)


class NetworkGovernanceTests(unittest.TestCase):
    def test_accountability_diagnostics_topology_network_and_vpn_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "accountability.json").write_text(
                json.dumps({"records": [{"owner": "ops", "reviewed": True}, {"owner": "", "reviewed": False}]}),
                encoding="utf-8",
            )
            (root / "diagnostics.json").write_text(
                json.dumps({"checks": [{"status": "healthy"}, {"status": "degraded"}, {"status": "failing"}]}),
                encoding="utf-8",
            )
            (root / "topology.json").write_text(
                json.dumps(
                    {
                        "nodes": [{"zone": "edge"}, {"zone": "core"}, {"zone": "edge"}],
                        "edges": [{"from": 1, "to": 2}, {"from": 2, "to": 3}],
                    }
                ),
                encoding="utf-8",
            )
            (root / "optimization.json").write_text(
                json.dumps({"links": [{"utilization": 85, "optimized": False}, {"utilization": 30, "optimized": True}]}),
                encoding="utf-8",
            )
            (root / "vpn.json").write_text(
                json.dumps({"tunnels": [{"active": True, "days_to_expiry": 10}, {"active": False, "days_to_expiry": 40}]}),
                encoding="utf-8",
            )
            with patch("tools.network_governance_tools.NETWORK_DIR", root):
                accountability = ai_accountability_tracker()
                diagnostics = autonomous_infrastructure_diagnostics()
                topology = live_topology_visualization()
                network = ai_network_optimization()
                vpn = autonomous_vpn_management()
        self.assertIn("Records tracked: 2", accountability)
        self.assertIn("Reviewed records: 1", accountability)
        self.assertIn("Degraded checks: 1", diagnostics)
        self.assertIn("Failing checks: 1", diagnostics)
        self.assertIn("Edges tracked: 2", topology)
        self.assertIn("Zones: core, edge", topology)
        self.assertIn("Congested links: 1", network)
        self.assertIn("Already tuned links: 1", network)
        self.assertIn("Active tunnels: 1", vpn)
        self.assertIn("Tunnels nearing expiry: 1", vpn)

    def test_routes_cover_516_to_520(self):
        for phase in range(516, 521):
            result = handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help")
            self.assertIsNotNone(result, f"missing route for {phase}")


if __name__ == "__main__":
    unittest.main()
