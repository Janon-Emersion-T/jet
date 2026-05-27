import unittest

from core.routes.linux_admin_routes import handle_linux_admin_routes
from tools.vps_monitoring_tools import VPSSnapshot, assess_vps_snapshot, vps_monitoring_engine


class VPSMonitoringEngineTests(unittest.TestCase):
    def test_reports_high_resource_pressure(self):
        snapshot = VPSSnapshot(
            load_1m=6.5,
            cpu_count=2,
            memory_percent=94.0,
            disk_percent=92.0,
            uptime_seconds=86400,
        )
        findings = assess_vps_snapshot(snapshot)
        report = vps_monitoring_engine(snapshot)
        self.assertEqual(len(findings), 3)
        self.assertIn("Status: ATTENTION", report)
        self.assertIn("HIGH CPU load", report)
        self.assertIn("HIGH Memory", report)
        self.assertIn("HIGH Root disk", report)

    def test_healthy_snapshot_has_no_review_points(self):
        report = vps_monitoring_engine(VPSSnapshot(
            load_1m=0.4,
            cpu_count=4,
            memory_percent=35.0,
            disk_percent=42.0,
            uptime_seconds=86400,
        ))
        self.assertIn("Status: HEALTHY", report)
        self.assertIn("Review points: 0", report)

    def test_route_exposes_phase_367_help(self):
        report = handle_linux_admin_routes("367 help", "367 help", "")
        self.assertIn("VPS MONITORING ENGINE COMMANDS - PHASE 367", report)


if __name__ == "__main__":
    unittest.main()
