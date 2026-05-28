from dataclasses import dataclass
import os
import shutil
import subprocess
from typing import List, Optional, Tuple

from tools.infrastructure_monitoring_tools import NetworkListener, collect_network_listeners


@dataclass
class PortExpectation:
    name: str
    port: int
    expected_open: bool = True


@dataclass
class AINode:
    name: str
    cpu_count: int
    ram_gb: float
    gpu_count: int
    role: str = "worker"


@dataclass
class GPUDevice:
    name: str
    utilization_percent: float
    memory_percent: float
    temperature_c: float


@dataclass
class CUDASnapshot:
    nvidia_smi_available: bool
    nvcc_available: bool
    driver_cuda_version: str = ""
    toolkit_version: str = ""


@dataclass
class OllamaSnapshot:
    installed: bool
    model_count: int
    largest_model_gb: float
    system_ram_gb: float
    gpu_available: bool


@dataclass
class InfraFinding:
    area: str
    severity: str
    detail: str
    recommendation: str


def _run(command: List[str], timeout: int = 5) -> str:
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        return ""
    return (result.stdout or result.stderr).strip()


def _status(findings: List[InfraFinding]) -> str:
    return "ATTENTION" if any(item.severity in {"high", "medium"} for item in findings) else "HEALTHY"


def assess_ports(
    listeners: List[NetworkListener],
    expectations: Optional[List[PortExpectation]] = None,
) -> List[InfraFinding]:
    expectations = expectations or [
        PortExpectation("SSH", 22, True),
        PortExpectation("HTTP", 80, False),
        PortExpectation("HTTPS", 443, False),
        PortExpectation("Ollama", 11434, False),
    ]
    open_ports = {listener.port for listener in listeners}
    findings: List[InfraFinding] = []
    for expected in expectations:
        is_open = expected.port in open_ports
        if expected.expected_open and not is_open:
            findings.append(InfraFinding(
                expected.name,
                "medium",
                f"Expected port {expected.port} is not listening.",
                "Confirm the service should be running before starting or restarting it.",
            ))
        if not expected.expected_open and is_open:
            findings.append(InfraFinding(
                expected.name,
                "low",
                f"Optional port {expected.port} is listening.",
                "Confirm this exposure is intentional and firewall-scoped.",
            ))
    exposed_sensitive = {3306: "MySQL", 5432: "PostgreSQL", 6379: "Redis", 11434: "Ollama"}
    for listener in listeners:
        public = listener.address.startswith("0.0.0.0:") or listener.address.startswith("[::]:") or listener.address.startswith("*:")
        if public and listener.port in exposed_sensitive:
            findings.append(InfraFinding(
                exposed_sensitive[listener.port],
                "high",
                f"{exposed_sensitive[listener.port]} is listening publicly on {listener.address}.",
                "Bind to localhost/private interfaces or restrict with firewall rules.",
            ))
    return findings


def port_monitoring_assistant(
    listeners: Optional[List[NetworkListener]] = None,
    expectations: Optional[List[PortExpectation]] = None,
) -> str:
    current = listeners if listeners is not None else collect_network_listeners()
    findings = assess_ports(current, expectations)
    lines = [
        "PORT MONITORING ASSISTANT - PHASE 376",
        "",
        "Mode: read-only local port expectation review.",
        f"Listeners reviewed: {len(current)}",
        f"Status: {_status(findings)}",
        f"Review points: {len(findings)}",
    ]
    for listener in current[:40]:
        lines.append(f"- {listener.protocol} {listener.address} {listener.process}".rstrip())
    for finding in findings:
        lines.extend([f"- {finding.severity.upper()} {finding.area}: {finding.detail}", f"  Recommendation: {finding.recommendation}"])
    if not findings:
        lines.append("No configured port monitoring expectations were violated.")
    lines.append("Safety: no packets were sent and no ports or firewall rules were changed.")
    return "\n".join(lines)


def collect_local_ai_nodes() -> List[AINode]:
    ram_gb = 0.0
    try:
        total = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
        ram_gb = total / (1024 ** 3)
    except (AttributeError, OSError, ValueError):
        pass
    gpu_count = 0
    output = _run(["bash", "-lc", "nvidia-smi -L 2>/dev/null"])
    if output:
        gpu_count = len([line for line in output.splitlines() if line.strip().startswith("GPU ")])
    return [AINode("local", max(os.cpu_count() or 1, 1), ram_gb, gpu_count, "single-node")]


def assess_ai_cluster(nodes: List[AINode]) -> List[InfraFinding]:
    findings: List[InfraFinding] = []
    if not nodes:
        findings.append(InfraFinding("Cluster", "high", "No AI nodes were supplied.", "Register at least one local or remote worker node."))
        return findings
    total_ram = sum(node.ram_gb for node in nodes)
    total_gpus = sum(node.gpu_count for node in nodes)
    if len(nodes) == 1:
        findings.append(InfraFinding("Resilience", "low", "Only one AI node is planned.", "Add a second node for failover if this will serve production traffic."))
    if total_ram < 16:
        findings.append(InfraFinding("Memory", "medium", f"Cluster RAM is {total_ram:.1f} GB.", "Use smaller quantized models or add memory before serving larger models."))
    if total_gpus == 0:
        findings.append(InfraFinding("GPU", "medium", "No GPUs are available in the planned cluster.", "Plan CPU-friendly quantized models or add GPU workers."))
    return findings


def local_ai_cluster_planner(nodes: Optional[List[AINode]] = None) -> str:
    current = nodes if nodes is not None else collect_local_ai_nodes()
    findings = assess_ai_cluster(current)
    lines = [
        "LOCAL AI CLUSTER PLANNER - PHASE 377",
        "",
        "Mode: read-only local AI capacity planning.",
        f"Nodes reviewed: {len(current)}",
        f"Status: {_status(findings)}",
        f"Review points: {len(findings)}",
    ]
    for node in current:
        lines.append(f"- {node.name}: {node.cpu_count} CPU, {node.ram_gb:.1f} GB RAM, {node.gpu_count} GPU, role={node.role}")
    for finding in findings:
        lines.extend([f"- {finding.severity.upper()} {finding.area}: {finding.detail}", f"  Recommendation: {finding.recommendation}"])
    if not findings:
        lines.append("No configured local AI cluster planning gaps detected.")
    lines.append("Safety: no model server, container, or worker process was started.")
    return "\n".join(lines)


def collect_gpu_devices() -> List[GPUDevice]:
    query = "nvidia-smi --query-gpu=name,utilization.gpu,memory.used,memory.total,temperature.gpu --format=csv,noheader,nounits"
    output = _run(["bash", "-lc", query])
    devices: List[GPUDevice] = []
    for line in output.splitlines():
        parts = [part.strip() for part in line.split(",")]
        if len(parts) != 5:
            continue
        try:
            used = float(parts[2])
            total = float(parts[3])
            devices.append(GPUDevice(parts[0], float(parts[1]), used / total * 100 if total else 0.0, float(parts[4])))
        except ValueError:
            continue
    return devices


def assess_gpu_utilization(devices: List[GPUDevice]) -> List[InfraFinding]:
    findings: List[InfraFinding] = []
    if not devices:
        findings.append(InfraFinding("GPU", "medium", "No NVIDIA GPU telemetry was detected.", "Use CPU profiles or install/check NVIDIA tooling if GPU acceleration is expected."))
        return findings
    for device in devices:
        if device.temperature_c >= 85:
            findings.append(InfraFinding(device.name, "high", f"GPU temperature is {device.temperature_c:.0f}C.", "Check cooling and reduce sustained workload if needed."))
        if device.memory_percent >= 90:
            findings.append(InfraFinding(device.name, "high", f"GPU memory use is {device.memory_percent:.1f}%.", "Unload unused models or reduce context/batch size."))
        elif device.utilization_percent < 10 and device.memory_percent > 70:
            findings.append(InfraFinding(device.name, "low", "GPU memory is occupied while utilization is low.", "Check for idle model processes holding VRAM."))
    return findings


def gpu_utilization_assistant(devices: Optional[List[GPUDevice]] = None) -> str:
    current = devices if devices is not None else collect_gpu_devices()
    findings = assess_gpu_utilization(current)
    lines = [
        "GPU UTILIZATION ASSISTANT - PHASE 378",
        "",
        "Mode: read-only GPU telemetry review.",
        f"GPUs reviewed: {len(current)}",
        f"Status: {_status(findings)}",
        f"Review points: {len(findings)}",
    ]
    for device in current:
        lines.append(f"- {device.name}: util {device.utilization_percent:.1f}%, memory {device.memory_percent:.1f}%, temp {device.temperature_c:.0f}C")
    for finding in findings:
        lines.extend([f"- {finding.severity.upper()} {finding.area}: {finding.detail}", f"  Recommendation: {finding.recommendation}"])
    if not findings:
        lines.append("No configured GPU utilization thresholds were exceeded.")
    lines.append("Safety: no GPU process was terminated or changed.")
    return "\n".join(lines)


def collect_cuda_snapshot() -> CUDASnapshot:
    smi = _run(["bash", "-lc", "nvidia-smi 2>/dev/null | head -3"])
    nvcc = _run(["bash", "-lc", "nvcc --version 2>/dev/null | tail -1"])
    driver_cuda = ""
    if "CUDA Version:" in smi:
        driver_cuda = smi.split("CUDA Version:", 1)[1].split()[0]
    toolkit = ""
    if "release" in nvcc:
        toolkit = nvcc.split("release", 1)[1].split(",", 1)[0].strip()
    return CUDASnapshot(bool(smi), bool(nvcc), driver_cuda, toolkit)


def assess_cuda_setup(snapshot: CUDASnapshot) -> List[InfraFinding]:
    findings: List[InfraFinding] = []
    if not snapshot.nvidia_smi_available:
        findings.append(InfraFinding("Driver", "medium", "nvidia-smi is not available.", "Install or repair NVIDIA drivers if CUDA acceleration is expected."))
    if snapshot.nvidia_smi_available and not snapshot.nvcc_available:
        findings.append(InfraFinding("Toolkit", "low", "CUDA driver is visible but nvcc toolkit is not.", "Install CUDA toolkit only if local compilation is required."))
    if snapshot.driver_cuda_version and snapshot.toolkit_version and snapshot.driver_cuda_version.split(".")[0] != snapshot.toolkit_version.split(".")[0]:
        findings.append(InfraFinding("Version", "medium", f"Driver CUDA {snapshot.driver_cuda_version} and toolkit {snapshot.toolkit_version} major versions differ.", "Align toolkit/runtime versions with driver compatibility."))
    return findings


def cuda_setup_advisor(snapshot: Optional[CUDASnapshot] = None) -> str:
    current = snapshot or collect_cuda_snapshot()
    findings = assess_cuda_setup(current)
    lines = [
        "CUDA SETUP ADVISOR - PHASE 379",
        "",
        "Mode: read-only CUDA environment review.",
        f"nvidia-smi available: {current.nvidia_smi_available}",
        f"nvcc available: {current.nvcc_available}",
        f"Driver CUDA: {current.driver_cuda_version or 'unknown'}",
        f"Toolkit CUDA: {current.toolkit_version or 'unknown'}",
        f"Status: {_status(findings)}",
        f"Review points: {len(findings)}",
    ]
    for finding in findings:
        lines.extend([f"- {finding.severity.upper()} {finding.area}: {finding.detail}", f"  Recommendation: {finding.recommendation}"])
    if not findings:
        lines.append("No configured CUDA setup gaps detected.")
    lines.append("Safety: no drivers, packages, or CUDA settings were installed or changed.")
    return "\n".join(lines)


def collect_ollama_snapshot() -> OllamaSnapshot:
    installed = shutil.which("ollama") is not None
    model_count = 0
    largest = 0.0
    if installed:
        output = _run(["ollama", "list"])
        for line in output.splitlines()[1:]:
            parts = line.split()
            if parts:
                model_count += 1
    ram_gb = 0.0
    try:
        ram_gb = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / (1024 ** 3)
    except (AttributeError, OSError, ValueError):
        pass
    gpu_available = bool(collect_gpu_devices())
    return OllamaSnapshot(installed, model_count, largest, ram_gb, gpu_available)


def assess_ollama(snapshot: OllamaSnapshot) -> List[InfraFinding]:
    findings: List[InfraFinding] = []
    if not snapshot.installed:
        findings.append(InfraFinding("Ollama", "medium", "Ollama is not installed or not in PATH.", "Install Ollama before planning local model serving."))
        return findings
    if snapshot.model_count == 0:
        findings.append(InfraFinding("Models", "low", "No local Ollama models are listed.", "Pull a small baseline model before configuring routing."))
    if snapshot.system_ram_gb < 16:
        findings.append(InfraFinding("Memory", "medium", f"System RAM is {snapshot.system_ram_gb:.1f} GB.", "Prefer small quantized models and modest context sizes."))
    if not snapshot.gpu_available:
        findings.append(InfraFinding("GPU", "low", "No GPU acceleration detected.", "Use CPU-optimized quantized models or add GPU capacity for heavier workloads."))
    return findings


def ollama_optimization_assistant(snapshot: Optional[OllamaSnapshot] = None) -> str:
    current = snapshot or collect_ollama_snapshot()
    findings = assess_ollama(current)
    lines = [
        "OLLAMA OPTIMIZATION ASSISTANT - PHASE 380",
        "",
        "Mode: read-only Ollama local model serving review.",
        f"Installed: {current.installed}",
        f"Models listed: {current.model_count}",
        f"System RAM: {current.system_ram_gb:.1f} GB",
        f"GPU available: {current.gpu_available}",
        f"Status: {_status(findings)}",
        f"Review points: {len(findings)}",
    ]
    for finding in findings:
        lines.extend([f"- {finding.severity.upper()} {finding.area}: {finding.detail}", f"  Recommendation: {finding.recommendation}"])
    if not findings:
        lines.append("No configured Ollama optimization gaps detected.")
    lines.extend([
        "Suggestions:",
        "- Keep one small fast model for routing and one larger model for deep work.",
        "- Tune context size and concurrent requests before adding more models.",
        "Safety: no models were pulled, removed, loaded, or benchmarked.",
    ])
    return "\n".join(lines)
