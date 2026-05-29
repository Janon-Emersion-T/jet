import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.local_model_runtime_tools import *


class LocalModelRuntimeTests(unittest.TestCase):
    def test_local_model_runtime_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "local_model_benchmark_lab.json": {"benchmark_runs": [{"usable": True, "noisy": True}, {"usable": False, "noisy": False}]},
                "model_quantization_advisor.json": {"quantization_profiles": [{"balanced": True, "degraded": True}, {"balanced": False, "degraded": False}]},
                "ollama_model_router.json": {"routing_paths": [{"matched": True, "misrouted": True}, {"matched": False, "misrouted": False}]},
                "hardware_aware_inference_planner.json": {"inference_plans": [{"fit": True, "overloaded": True}, {"fit": False, "overloaded": False}]},
                "cpu_gpu_load_balancer.json": {"load_paths": [{"balanced": True, "saturated": True}, {"balanced": False, "saturated": False}]},
                "context_window_budgeter.json": {"context_budgets": [{"efficient": True, "overflowing": True}, {"efficient": False, "overflowing": False}]},
                "prompt_compression_engine.json": {"compression_runs": [{"faithful": True, "distorted": True}, {"faithful": False, "distorted": False}]},
                "multi_model_debate_mode.json": {"debate_rounds": [{"useful": True, "circular": True}, {"useful": False, "circular": False}]},
                "critic_verifier_architecture.json": {"verification_paths": [{"checked": True, "unverified": True}, {"checked": False, "unverified": False}]},
                "answer_confidence_scorer.json": {"answer_scores": [{"calibrated": True, "overconfident": True}, {"calibrated": False, "overconfident": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.local_model_runtime_tools.LOCAL_MODEL_RUNTIME_DIR", root):
                self.assertIn("Noisy runs: 1", local_model_benchmark_lab())
                self.assertIn("Degraded profiles: 1", model_quantization_advisor())
                self.assertIn("Misrouted paths: 1", ollama_model_router())
                self.assertIn("Overloaded plans: 1", hardware_aware_inference_planner())
                self.assertIn("Saturated paths: 1", cpu_gpu_load_balancer())
                self.assertIn("Overflowing budgets: 1", context_window_budgeter())
                self.assertIn("Distorted runs: 1", prompt_compression_engine())
                self.assertIn("Circular rounds: 1", multi_model_debate_mode())
                self.assertIn("Unverified paths: 1", critic_verifier_architecture())
                self.assertIn("Overconfident scores: 1", answer_confidence_scorer())

    def test_routes_cover_1701_to_1710(self):
        for phase in range(1701, 1711):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
