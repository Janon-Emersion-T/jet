from dataclasses import dataclass
from pathlib import Path
import os
import shutil
import subprocess
import time
from typing import List, Optional, Tuple

from tools.project_context_tools import get_current_project_path


@dataclass
class MetricFinding:
    area: str
    severity: str
    detail: str
    recommendation: str


@dataclass
class CPURAMSnapshot:
    load_1m: float
    cpu_count: int
    memory_percent: float
    swap_percent: float


@dataclass
class DiskVolume:
    mount: str
    percent_used: float
    free_gb: float


@dataclass
class ServiceSnapshot:
    name: str
    active_state: str
    enabled_state: str
    restart_policy: str = ""


@dataclass
class BackupArtifact:
    path: str
    size_bytes: int
    age_hours: float


@dataclass
class DisasterRecoveryState:
    has_runbook: bool
    backup_count: int
    latest_backup_age_hours: Optional[float]
    has_restore_notes: bool


@dataclass
class InfrastructureTopology:
    interfaces: List[str]
    routes: List[str]
    listeners: List[str]


@dataclass
class NetworkListener:
    protocol: str
    address: str
    port: int
    process: str = ""


def _run(command: List[str], timeout: int = 5) -> str:
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        return ""
    return result.stdout.strip()


def _status(findings: List[MetricFinding]) -> str:
    return "ATTENTION" if any(item.severity in {"high", "medium"} for item in findings) else "HEALTHY"


def collect_cpu_ram_snapshot() -> CPURAMSnapshot:
    cpu_count = max(os.cpu_count() or 1, 1)
    load_1m = os.getloadavg()[0] if hasattr(os, "getloadavg") else 0.0
    memory_percent = 0.0
    swap_percent = 0.0
    output = _run(["free", "-m"])
    lines = output.splitlines()
    try:
        mem = lines[1].split()
        if int(mem[1]) > 0:
            memory_percent = int(mem[2]) / int(mem[1]) * 100
        if len(lines) > 2:
            swap = lines[2].split()
            if int(swap[1]) > 0:
                swap_percent = int(swap[2]) / int(swap[1]) * 100
    except (IndexError, ValueError, ZeroDivisionError):
        pass
    return CPURAMSnapshot(load_1m, cpu_count, memory_percent, swap_percent)


def assess_cpu_ram(snapshot: CPURAMSnapshot) -> List[MetricFinding]:
    findings: List[MetricFinding] = []
    load_ratio = snapshot.load_1m / max(snapshot.cpu_count, 1)
    if load_ratio >= 1.5:
        findings.append(MetricFinding("CPU", "high", f"Load ratio is {load_ratio:.2f}.", "Inspect hot processes and request volume."))
    elif load_ratio >= 1.0:
        findings.append(MetricFinding("CPU", "medium", f"Load ratio is {load_ratio:.2f}.", "Watch sustained load before scaling."))
    if snapshot.memory_percent >= 90:
        findings.append(MetricFinding("RAM", "high", f"Memory use is {snapshot.memory_percent:.1f}%.", "Review memory-heavy services and leaks."))
    elif snapshot.memory_percent >= 80:
        findings.append(MetricFinding("RAM", "medium", f"Memory use is {snapshot.memory_percent:.1f}%.", "Monitor pressure and resident process growth."))
    if snapshot.swap_percent >= 50:
        findings.append(MetricFinding("Swap", "medium", f"Swap use is {snapshot.swap_percent:.1f}%.", "Investigate memory pressure before restarting services."))
    return findings


def cpu_ram_monitoring_assistant(snapshot: Optional[CPURAMSnapshot] = None) -> str:
    current = snapshot or collect_cpu_ram_snapshot()
    findings = assess_cpu_ram(current)
    lines = [
        "CPU/RAM MONITORING ASSISTANT - PHASE 368",
        "",
        "Mode: read-only CPU and memory pressure review.",
        f"Status: {_status(findings)}",
        f"- Load: {current.load_1m:.2f} across {current.cpu_count} CPUs",
        f"- Memory: {current.memory_percent:.1f}%",
        f"- Swap: {current.swap_percent:.1f}%",
        f"Review points: {len(findings)}",
    ]
    for finding in findings:
        lines.extend([f"- {finding.severity.upper()} {finding.area}: {finding.detail}", f"  Recommendation: {finding.recommendation}"])
    if not findings:
        lines.append("No configured CPU/RAM thresholds were exceeded.")
    lines.append("Safety: no processes were stopped, restarted, or changed.")
    return "\n".join(lines)


def collect_disk_volumes() -> List[DiskVolume]:
    usage = shutil.disk_usage("/")
    return [DiskVolume("/", usage.used / usage.total * 100, usage.free / (1024 ** 3))]


def assess_disks(volumes: List[DiskVolume]) -> List[MetricFinding]:
    findings: List[MetricFinding] = []
    for volume in volumes:
        if volume.percent_used >= 90:
            findings.append(MetricFinding(volume.mount, "high", f"Disk use is {volume.percent_used:.1f}% with {volume.free_gb:.1f} GB free.", "Review logs, backups, and large files before cleanup."))
        elif volume.percent_used >= 80:
            findings.append(MetricFinding(volume.mount, "medium", f"Disk use is {volume.percent_used:.1f}% with {volume.free_gb:.1f} GB free.", "Plan cleanup or capacity expansion."))
    return findings


def disk_health_checker(volumes: Optional[List[DiskVolume]] = None) -> str:
    current = volumes or collect_disk_volumes()
    findings = assess_disks(current)
    lines = [
        "DISK HEALTH CHECKER - PHASE 369",
        "",
        "Mode: read-only disk capacity review.",
        f"Status: {_status(findings)}",
        "Volumes:",
    ]
    for volume in current:
        lines.append(f"- {volume.mount}: {volume.percent_used:.1f}% used, {volume.free_gb:.1f} GB free")
    lines.append(f"Review points: {len(findings)}")
    for finding in findings:
        lines.extend([f"- {finding.severity.upper()} {finding.area}: {finding.detail}", f"  Recommendation: {finding.recommendation}"])
    if not findings:
        lines.append("No configured disk thresholds were exceeded.")
    lines.append("Safety: no files were deleted or modified.")
    return "\n".join(lines)


def assess_services(services: List[ServiceSnapshot]) -> List[MetricFinding]:
    findings: List[MetricFinding] = []
    for service in services:
        active = service.active_state.lower()
        enabled = service.enabled_state.lower()
        restart = service.restart_policy.lower()
        if active in {"failed", "inactive"}:
            findings.append(MetricFinding(service.name, "high", f"Service is {service.active_state}.", "Inspect logs and plan a controlled restart if appropriate."))
        if enabled in {"disabled", "masked"}:
            findings.append(MetricFinding(service.name, "medium", f"Service is {service.enabled_state}.", "Confirm whether this service should start at boot."))
        if active == "active" and restart in {"", "no", "none"}:
            findings.append(MetricFinding(service.name, "low", "No restart policy is visible.", "Consider a systemd restart policy for critical services."))
    return findings


def collect_service_snapshots() -> List[ServiceSnapshot]:
    names = ["nginx", "mysql", "mariadb", "redis-server", "php8.3-fpm", "php8.4-fpm"]
    services: List[ServiceSnapshot] = []
    for name in names:
        active = _run(["systemctl", "is-active", name]) or "unknown"
        enabled = _run(["systemctl", "is-enabled", name]) or "unknown"
        if active != "unknown" or enabled != "unknown":
            services.append(ServiceSnapshot(name, active, enabled))
    return services


def service_auto_recovery_planner(services: Optional[List[ServiceSnapshot]] = None) -> str:
    current = services if services is not None else collect_service_snapshots()
    findings = assess_services(current)
    lines = [
        "SERVICE AUTO-RECOVERY PLANNER - PHASE 370",
        "",
        "Mode: read-only service recovery planning.",
        f"Services reviewed: {len(current)}",
        f"Status: {_status(findings)}",
        f"Review points: {len(findings)}",
    ]
    for finding in findings:
        lines.extend([f"- {finding.severity.upper()} {finding.area}: {finding.detail}", f"  Recommendation: {finding.recommendation}"])
    if not findings:
        lines.append("No configured service recovery concerns detected.")
    lines.append("Safety: no services were restarted, enabled, or modified.")
    return "\n".join(lines)


def uptime_monitoring_assistant(uptime_seconds: Optional[float] = None) -> str:
    if uptime_seconds is None:
        try:
            uptime_seconds = float(Path("/proc/uptime").read_text(encoding="ascii").split()[0])
        except (OSError, ValueError, IndexError):
            uptime_seconds = 0.0
    findings: List[MetricFinding] = []
    if 0 < uptime_seconds < 600:
        findings.append(MetricFinding("Uptime", "medium", "Host restarted within the last ten minutes.", "Confirm whether the restart was expected and check key services."))
    elif uptime_seconds > 180 * 86400:
        findings.append(MetricFinding("Uptime", "low", "Host uptime exceeds 180 days.", "Review patch/reboot policy and maintenance windows."))
    lines = [
        "UPTIME MONITORING ASSISTANT - PHASE 371",
        "",
        "Mode: read-only uptime review.",
        f"Uptime: {uptime_seconds / 3600:.1f} hours",
        f"Status: {_status(findings)}",
        f"Review points: {len(findings)}",
    ]
    for finding in findings:
        lines.extend([f"- {finding.severity.upper()} {finding.area}: {finding.detail}", f"  Recommendation: {finding.recommendation}"])
    if not findings:
        lines.append("No configured uptime thresholds were exceeded.")
    lines.append("Safety: no reboot or service action was performed.")
    return "\n".join(lines)


def discover_backup_artifacts(project: Optional[Path] = None) -> List[BackupArtifact]:
    root = Path(project).resolve() if project else (get_current_project_path() or Path.cwd())
    patterns = ["*.zip", "*.tar", "*.tar.gz", "*.tgz", "*.sql", "*.bak"]
    candidates: List[Path] = []
    for folder in [root / "backups", root / "backup", root / "storage" / "backups"]:
        if folder.exists():
            for pattern in patterns:
                candidates.extend(folder.rglob(pattern))
    now = time.time()
    artifacts: List[BackupArtifact] = []
    for file in candidates[:100]:
        try:
            stat = file.stat()
        except OSError:
            continue
        artifacts.append(BackupArtifact(str(file.relative_to(root)), stat.st_size, (now - stat.st_mtime) / 3600))
    return artifacts


def assess_backups(artifacts: List[BackupArtifact]) -> List[MetricFinding]:
    findings: List[MetricFinding] = []
    if not artifacts:
        findings.append(MetricFinding("Backups", "high", "No backup artifacts were found.", "Confirm automated backups and restore coverage."))
        return findings
    latest = min(item.age_hours for item in artifacts)
    if latest > 48:
        findings.append(MetricFinding("Backups", "high", f"Latest backup is {latest:.1f} hours old.", "Check backup schedule and recent job failures."))
    for artifact in artifacts:
        if artifact.size_bytes == 0:
            findings.append(MetricFinding(artifact.path, "high", "Backup artifact is empty.", "Treat this backup as invalid and inspect the backup job."))
    return findings


def backup_verification_engine(artifacts: Optional[List[BackupArtifact]] = None, project: Optional[Path] = None) -> str:
    current = artifacts if artifacts is not None else discover_backup_artifacts(project)
    findings = assess_backups(current)
    lines = [
        "BACKUP VERIFICATION ENGINE - PHASE 372",
        "",
        "Mode: read-only backup artifact review.",
        f"Artifacts reviewed: {len(current)}",
        f"Status: {_status(findings)}",
        f"Review points: {len(findings)}",
    ]
    for artifact in current[:20]:
        lines.append(f"- {artifact.path}: {artifact.size_bytes} bytes, age {artifact.age_hours:.1f} hours")
    for finding in findings:
        lines.extend([f"- {finding.severity.upper()} {finding.area}: {finding.detail}", f"  Recommendation: {finding.recommendation}"])
    lines.append("Safety: no backups were restored, deleted, or modified.")
    return "\n".join(lines)


def disaster_recovery_planner(state: Optional[DisasterRecoveryState] = None, project: Optional[Path] = None) -> str:
    if state is None:
        root = Path(project).resolve() if project else (get_current_project_path() or Path.cwd())
        docs = [root / "DISASTER_RECOVERY.md", root / "docs" / "disaster_recovery.md", root / "docs" / "restore.md"]
        artifacts = discover_backup_artifacts(root)
        latest = min((item.age_hours for item in artifacts), default=None)
        state = DisasterRecoveryState(any(path.exists() for path in docs), len(artifacts), latest, any("restore" in path.name.lower() and path.exists() for path in docs))
    findings: List[MetricFinding] = []
    if not state.has_runbook:
        findings.append(MetricFinding("Runbook", "high", "No disaster recovery runbook was found.", "Create a recovery runbook with owners, RTO/RPO, and restore steps."))
    if state.backup_count == 0:
        findings.append(MetricFinding("Backups", "high", "No backups are visible to the planner.", "Connect backup verification to the recovery plan."))
    elif state.latest_backup_age_hours is not None and state.latest_backup_age_hours > 48:
        findings.append(MetricFinding("Backups", "medium", f"Latest backup is {state.latest_backup_age_hours:.1f} hours old.", "Review backup freshness against RPO."))
    if not state.has_restore_notes:
        findings.append(MetricFinding("Restore notes", "medium", "No restore notes were found.", "Document and periodically test restore commands."))
    lines = [
        "DISASTER RECOVERY PLANNER - PHASE 373",
        "",
        "Mode: read-only disaster recovery readiness review.",
        f"Status: {_status(findings)}",
        f"Review points: {len(findings)}",
    ]
    for finding in findings:
        lines.extend([f"- {finding.severity.upper()} {finding.area}: {finding.detail}", f"  Recommendation: {finding.recommendation}"])
    if not findings:
        lines.append("No configured disaster recovery readiness gaps detected.")
    lines.append("Safety: no restore, failover, or infrastructure change was performed.")
    return "\n".join(lines)


def infrastructure_topology_mapper(snapshot: Optional[InfrastructureTopology] = None) -> str:
    if snapshot is None:
        interfaces = (_run(["bash", "-lc", "ip -o link show 2>/dev/null | awk -F': ' '{print $2}'"]) or "").splitlines()
        routes = (_run(["bash", "-lc", "ip route 2>/dev/null"]) or "").splitlines()
        listeners = (_run(["bash", "-lc", "ss -tuln 2>/dev/null | tail -n +2 | head -30"]) or "").splitlines()
        snapshot = InfrastructureTopology(interfaces[:20], routes[:20], listeners[:30])
    findings: List[MetricFinding] = []
    if not snapshot.interfaces:
        findings.append(MetricFinding("Interfaces", "medium", "No network interfaces were discovered.", "Confirm `ip` tooling and host network visibility."))
    if not snapshot.routes:
        findings.append(MetricFinding("Routes", "medium", "No routes were discovered.", "Confirm default route and network configuration."))
    lines = [
        "INFRASTRUCTURE TOPOLOGY MAPPER - PHASE 374",
        "",
        "Mode: read-only local topology summary.",
        f"Status: {_status(findings)}",
        "Interfaces:",
        *(f"- {item}" for item in snapshot.interfaces[:20]),
        "Routes:",
        *(f"- {item}" for item in snapshot.routes[:20]),
        "Listeners:",
        *(f"- {item}" for item in snapshot.listeners[:20]),
        f"Review points: {len(findings)}",
    ]
    for finding in findings:
        lines.extend([f"- {finding.severity.upper()} {finding.area}: {finding.detail}", f"  Recommendation: {finding.recommendation}"])
    if not findings:
        lines.append("Topology summary collected without configured gaps.")
    lines.append("Safety: no network interface, route, or service state was changed.")
    return "\n".join(lines)


def collect_network_listeners() -> List[NetworkListener]:
    output = _run(["bash", "-lc", "ss -tulnH 2>/dev/null"])
    listeners: List[NetworkListener] = []
    for line in output.splitlines()[:100]:
        parts = line.split()
        if len(parts) < 5:
            continue
        protocol = parts[0]
        local = parts[4]
        port_text = local.rsplit(":", 1)[-1]
        if port_text.isdigit():
            listeners.append(NetworkListener(protocol, local, int(port_text)))
    return listeners


def assess_network_listeners(listeners: List[NetworkListener]) -> List[MetricFinding]:
    findings: List[MetricFinding] = []
    sensitive = {3306: "database", 5432: "database", 6379: "redis", 9200: "search", 27017: "database"}
    for listener in listeners:
        exposed = listener.address.startswith("0.0.0.0:") or listener.address.startswith("[::]:") or listener.address.startswith("*:")
        if exposed and listener.port in sensitive:
            findings.append(MetricFinding(str(listener.port), "high", f"Public listener exposes {sensitive[listener.port]} service on {listener.address}.", "Bind to localhost/private interfaces or restrict with firewall rules."))
        elif exposed and listener.port in {21, 23}:
            findings.append(MetricFinding(str(listener.port), "medium", f"Legacy remote service is listening on {listener.address}.", "Disable legacy protocols or restrict access tightly."))
    return findings


def network_scanner(listeners: Optional[List[NetworkListener]] = None) -> str:
    current = listeners if listeners is not None else collect_network_listeners()
    findings = assess_network_listeners(current)
    lines = [
        "NETWORK SCANNER - PHASE 375",
        "",
        "Mode: read-only local listening-port review.",
        f"Listeners reviewed: {len(current)}",
        f"Status: {_status(findings)}",
        f"Review points: {len(findings)}",
    ]
    for listener in current[:40]:
        lines.append(f"- {listener.protocol} {listener.address} {listener.process}".rstrip())
    for finding in findings:
        lines.extend([f"- {finding.severity.upper()} port {finding.area}: {finding.detail}", f"  Recommendation: {finding.recommendation}"])
    if not findings:
        lines.append("No configured risky local listener indicators detected.")
    lines.append("Safety: no packets were sent and no ports or firewall rules were changed.")
    return "\n".join(lines)
