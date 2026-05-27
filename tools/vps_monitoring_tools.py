from dataclasses import dataclass
import os
import shutil
import subprocess
from typing import List, Optional


@dataclass
class VPSMetricFinding:
    metric: str
    severity: str
    detail: str
    recommendation: str


@dataclass
class VPSSnapshot:
    load_1m: float
    cpu_count: int
    memory_percent: float
    disk_percent: float
    uptime_seconds: float


def collect_vps_snapshot() -> VPSSnapshot:
    cpu_count = max(os.cpu_count() or 1, 1)
    load_1m = os.getloadavg()[0] if hasattr(os, "getloadavg") else 0.0
    memory_percent = 0.0
    disk_percent = shutil.disk_usage("/").used / shutil.disk_usage("/").total * 100
    uptime_seconds = 0.0

    try:
        memory = subprocess.run(
            ["free", "-m"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        ).stdout.splitlines()
        values = memory[1].split() if len(memory) > 1 else []
        if len(values) >= 3 and int(values[1]) > 0:
            memory_percent = int(values[2]) / int(values[1]) * 100
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired, ValueError):
        memory_percent = 0.0

    try:
        with open("/proc/uptime", "r", encoding="ascii") as uptime_file:
            uptime_seconds = float(uptime_file.read().split()[0])
    except (OSError, ValueError, IndexError):
        uptime_seconds = 0.0

    return VPSSnapshot(load_1m, cpu_count, memory_percent, disk_percent, uptime_seconds)


def assess_vps_snapshot(snapshot: VPSSnapshot) -> List[VPSMetricFinding]:
    findings: List[VPSMetricFinding] = []
    normalized_load = snapshot.load_1m / max(snapshot.cpu_count, 1)
    if normalized_load >= 1.5:
        findings.append(VPSMetricFinding(
            "CPU load",
            "high",
            f"One-minute load {snapshot.load_1m:.2f} across {snapshot.cpu_count} CPUs is elevated.",
            "Inspect busy processes and application demand before changing capacity.",
        ))
    elif normalized_load >= 1.0:
        findings.append(VPSMetricFinding(
            "CPU load",
            "medium",
            f"One-minute load {snapshot.load_1m:.2f} is at or above available CPU count.",
            "Review sustained load trends and service response times.",
        ))
    if snapshot.memory_percent >= 90:
        findings.append(VPSMetricFinding(
            "Memory",
            "high",
            f"Memory use is {snapshot.memory_percent:.1f}%.",
            "Inspect memory-heavy services and swap activity before restarting anything.",
        ))
    elif snapshot.memory_percent >= 80:
        findings.append(VPSMetricFinding(
            "Memory",
            "medium",
            f"Memory use is {snapshot.memory_percent:.1f}%.",
            "Monitor memory pressure and investigate growth in resident processes.",
        ))
    if snapshot.disk_percent >= 90:
        findings.append(VPSMetricFinding(
            "Root disk",
            "high",
            f"Root filesystem use is {snapshot.disk_percent:.1f}%.",
            "Review logs, backups, and large files before considering cleanup.",
        ))
    elif snapshot.disk_percent >= 80:
        findings.append(VPSMetricFinding(
            "Root disk",
            "medium",
            f"Root filesystem use is {snapshot.disk_percent:.1f}%.",
            "Plan capacity or reviewed cleanup before space becomes critical.",
        ))
    if 0 < snapshot.uptime_seconds < 600:
        findings.append(VPSMetricFinding(
            "Uptime",
            "low",
            "The host appears to have restarted within the last ten minutes.",
            "Confirm whether this restart was expected and check affected services.",
        ))
    return findings


def vps_monitoring_engine(snapshot: Optional[VPSSnapshot] = None) -> str:
    current = snapshot or collect_vps_snapshot()
    findings = assess_vps_snapshot(current)
    status = "ATTENTION" if any(item.severity in {"high", "medium"} for item in findings) else "HEALTHY"
    lines = [
        "VPS MONITORING ENGINE - PHASE 367",
        "",
        "Mode: read-only host resource snapshot.",
        f"Status: {status}",
        "",
        "Metrics:",
        f"- One-minute load: {current.load_1m:.2f} across {current.cpu_count} CPUs",
        f"- Memory use: {current.memory_percent:.1f}%",
        f"- Root disk use: {current.disk_percent:.1f}%",
        f"- Uptime: {current.uptime_seconds / 3600:.1f} hours",
        "",
        f"Review points: {len(findings)}",
    ]
    for finding in findings:
        lines.extend([
            f"- {finding.severity.upper()} {finding.metric}: {finding.detail}",
            f"  Recommendation: {finding.recommendation}",
        ])
    if not findings:
        lines.append("No configured VPS monitoring thresholds were exceeded.")
    lines.extend([
        "",
        "Safety:",
        "- This command captures local read-only metrics; it does not restart services or delete data.",
        "- Use focused monitoring phases for deeper CPU/RAM and disk diagnostics.",
    ])
    return "\n".join(lines)
