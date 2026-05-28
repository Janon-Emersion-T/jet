import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.experimentation_ml_tools import *


class ExperimentationMLTests(unittest.TestCase):
    def test_experimentation_ml_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "experimentation_planner.json": {"experiments": [{"prioritized": True, "status": "approved"}, {"prioritized": False, "status": "draft"}]},
                "hypothesis_generation.json": {"hypotheses": [{"testable": True, "reviewed": True}, {"testable": False, "reviewed": False}]},
                "data_science_orchestration.json": {"workflows": [{"automated": True, "status": "blocked"}, {"automated": False, "status": "ready"}]},
                "ml_pipeline_manager.json": {"pipelines": [{"status": "healthy", "retraining": True}, {"status": "degraded", "retraining": False}]},
                "dataset_cleaner.json": {"datasets": [{"cleaned": True, "flagged": True}, {"cleaned": False, "flagged": False}]},
                "feature_engineering.json": {"features": [{"selected": True, "drift_sensitive": True}, {"selected": False, "drift_sensitive": False}]},
                "model_lifecycle.json": {"models": [{"stage": "deployed"}, {"stage": "archived"}]},
                "continuous_evaluation.json": {"evaluations": [{"status": "passing"}, {"status": "failing"}]},
                "drift_detection.json": {"monitors": [{"drift": "detected"}, {"drift": "stable"}]},
                "synthetic_data.json": {"datasets": [{"privacy_checked": True, "balanced": True}, {"privacy_checked": False, "balanced": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.experimentation_ml_tools.EXPERIMENTATION_DIR", root):
                self.assertIn("Approved experiments: 1", autonomous_experimentation_planner())
                self.assertIn("Reviewed hypotheses: 1", ai_hypothesis_generation())
                self.assertIn("Blocked workflows: 1", data_science_orchestration_layer())
                self.assertIn("Retraining pipelines: 1", automated_ml_pipeline_manager())
                self.assertIn("Flagged datasets: 1", ai_dataset_cleaner())
                self.assertIn("Selected features: 1", feature_engineering_assistant())
                self.assertIn("Archived models: 1", ai_model_lifecycle_manager())
                self.assertIn("Failing evaluations: 1", continuous_model_evaluation())
                self.assertIn("Detected drift monitors: 1", ai_drift_detection_system())
                self.assertIn("Balanced datasets: 1", synthetic_data_generator())

    def test_routes_cover_601_to_610(self):
        for phase in range(601, 611):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
