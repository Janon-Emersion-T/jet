import unittest

from core.routes.linux_admin_routes import handle_linux_admin_routes
from tools.ai_infrastructure_tools import (
    AINode,
    CUDASnapshot,
    GPUDevice,
    OllamaSnapshot,
    PortExpectation,
    assess_ai_cluster,
    assess_cuda_setup,
    assess_gpu_utilization,
    assess_ollama,
    assess_ports,
    cuda_setup_advisor,
    gpu_utilization_assistant,
    local_ai_cluster_planner,
    ollama_optimization_assistant,
    port_monitoring_assistant,
)
from tools.infrastructure_monitoring_tools import NetworkListener


class AIInfrastructureTests(unittest.TestCase):
    def test_port_monitoring_reports_missing_required_and_public_sensitive_ports(self):
        listeners = [NetworkListener("tcp", "0.0.0.0:3306", 3306, "mysql")]
        findings = assess_ports(listeners, [PortExpectation("SSH", 22, True)])
        report = port_monitoring_assistant(listeners, [PortExpectation("SSH", 22, True)])
        self.assertEqual(len(findings), 2)
        self.assertIn("MEDIUM SSH", report)
        self.assertIn("HIGH MySQL", report)

    def test_local_ai_cluster_planner_reports_small_cpu_only_node(self):
        nodes = [AINode("local", 4, 8.0, 0)]
        self.assertEqual(len(assess_ai_cluster(nodes)), 3)
        self.assertIn("MEDIUM Memory", local_ai_cluster_planner(nodes))

    def test_gpu_utilization_reports_hot_full_gpu(self):
        devices = [GPUDevice("RTX", 98.0, 95.0, 88.0)]
        self.assertEqual(len(assess_gpu_utilization(devices)), 2)
        self.assertIn("HIGH RTX", gpu_utilization_assistant(devices))

    def test_cuda_setup_reports_missing_nvcc_with_driver(self):
        snapshot = CUDASnapshot(True, False, "12.4", "")
        self.assertEqual(len(assess_cuda_setup(snapshot)), 1)
        self.assertIn("LOW Toolkit", cuda_setup_advisor(snapshot))

    def test_ollama_optimization_reports_missing_install(self):
        snapshot = OllamaSnapshot(False, 0, 0.0, 32.0, False)
        self.assertEqual(len(assess_ollama(snapshot)), 1)
        self.assertIn("MEDIUM Ollama", ollama_optimization_assistant(snapshot))

    def test_routes_expose_phase_help(self):
        for phase, expected in [
            ("376 help", "PORT MONITORING ASSISTANT COMMANDS - PHASE 376"),
            ("377 help", "LOCAL AI CLUSTER PLANNER COMMANDS - PHASE 377"),
            ("378 help", "GPU UTILIZATION ASSISTANT COMMANDS - PHASE 378"),
            ("379 help", "CUDA SETUP ADVISOR COMMANDS - PHASE 379"),
            ("380 help", "OLLAMA OPTIMIZATION ASSISTANT COMMANDS - PHASE 380"),
        ]:
            self.assertIn(expected, handle_linux_admin_routes(phase, phase, ""))


if __name__ == "__main__":
    unittest.main()
