import unittest

from core.routes.linux_admin_routes import handle_linux_admin_routes
from tools.infrastructure_monitoring_tools import (
    BackupArtifact,
    CPURAMSnapshot,
    DiskVolume,
    DisasterRecoveryState,
    InfrastructureTopology,
    NetworkListener,
    ServiceSnapshot,
    assess_cpu_ram,
    assess_disks,
    assess_services,
    backup_verification_engine,
    cpu_ram_monitoring_assistant,
    disaster_recovery_planner,
    disk_health_checker,
    infrastructure_topology_mapper,
    network_scanner,
    service_auto_recovery_planner,
    uptime_monitoring_assistant,
)


class InfrastructureMonitoringTests(unittest.TestCase):
    def test_cpu_ram_monitoring_reports_pressure(self):
        snapshot = CPURAMSnapshot(load_1m=8.0, cpu_count=2, memory_percent=92.0, swap_percent=55.0)
        self.assertEqual(len(assess_cpu_ram(snapshot)), 3)
        self.assertIn("Status: ATTENTION", cpu_ram_monitoring_assistant(snapshot))

    def test_disk_health_checker_reports_full_volume(self):
        volumes = [DiskVolume("/", 94.0, 1.2)]
        self.assertEqual(len(assess_disks(volumes)), 1)
        self.assertIn("HIGH /", disk_health_checker(volumes))

    def test_service_recovery_planner_reports_failed_service(self):
        services = [ServiceSnapshot("nginx", "failed", "enabled")]
        self.assertEqual(len(assess_services(services)), 1)
        self.assertIn("HIGH nginx", service_auto_recovery_planner(services))

    def test_uptime_monitoring_reports_recent_restart(self):
        report = uptime_monitoring_assistant(300)
        self.assertIn("Status: ATTENTION", report)
        self.assertIn("last ten minutes", report)

    def test_backup_verification_reports_empty_backup(self):
        artifacts = [BackupArtifact("backups/site.sql", 0, 1)]
        report = backup_verification_engine(artifacts)
        self.assertIn("HIGH backups/site.sql", report)

    def test_disaster_recovery_planner_reports_missing_runbook(self):
        state = DisasterRecoveryState(False, 0, None, False)
        report = disaster_recovery_planner(state)
        self.assertIn("HIGH Runbook", report)
        self.assertIn("HIGH Backups", report)

    def test_topology_mapper_reports_missing_routes(self):
        report = infrastructure_topology_mapper(InfrastructureTopology(["eth0"], [], []))
        self.assertIn("MEDIUM Routes", report)

    def test_network_scanner_reports_public_database_listener(self):
        listeners = [NetworkListener("tcp", "0.0.0.0:3306", 3306, "mysql")]
        report = network_scanner(listeners)
        self.assertIn("HIGH port 3306", report)

    def test_routes_expose_phase_help(self):
        for phase, expected in [
            ("368 help", "CPU/RAM MONITORING ASSISTANT COMMANDS - PHASE 368"),
            ("369 help", "DISK HEALTH CHECKER COMMANDS - PHASE 369"),
            ("370 help", "SERVICE AUTO-RECOVERY PLANNER COMMANDS - PHASE 370"),
            ("371 help", "UPTIME MONITORING ASSISTANT COMMANDS - PHASE 371"),
            ("372 help", "BACKUP VERIFICATION ENGINE COMMANDS - PHASE 372"),
            ("373 help", "DISASTER RECOVERY PLANNER COMMANDS - PHASE 373"),
            ("374 help", "INFRASTRUCTURE TOPOLOGY MAPPER COMMANDS - PHASE 374"),
            ("375 help", "NETWORK SCANNER COMMANDS - PHASE 375"),
        ]:
            self.assertIn(expected, handle_linux_admin_routes(phase, phase, ""))


if __name__ == "__main__":
    unittest.main()
