import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.policy_training_tools import *


class PolicyTrainingToolsTests(unittest.TestCase):
    def test_policy_training_tools_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "policy_to_action_mapper.json": {"policy_mappings": [{"actionable": True, "ambiguous": True}, {"actionable": False, "ambiguous": False}]},
                "sop_compliance_checker.json": {"sop_checks": [{"compliant": True, "gapped": True}, {"compliant": False, "gapped": False}]},
                "staff_handbook_assistant.json": {"handbook_sections": [{"clear": True, "outdated": True}, {"clear": False, "outdated": False}]},
                "training_module_generator.json": {"training_modules": [{"ready": True, "thin": True}, {"ready": False, "thin": False}]},
                "quiz_exam_generator.json": {"assessment_items": [{"usable": True, "ambiguous": True}, {"usable": False, "ambiguous": False}]},
                "teach_back_evaluator.json": {"teach_back_responses": [{"understood": True, "unclear": True}, {"understood": False, "unclear": False}]},
                "ai_tutor_personality_modes.json": {"tutor_modes": [{"matched": True, "mismatched": True}, {"matched": False, "mismatched": False}]},
                "skill_progression_tracker.json": {"progress_markers": [{"advancing": True, "stalled": True}, {"advancing": False, "stalled": False}]},
                "learning_retention_engine.json": {"retention_cycles": [{"retained": True, "fading": True}, {"retained": False, "fading": False}]},
                "company_knowledge_academy.json": {"academy_tracks": [{"organized": True, "fragmented": True}, {"organized": False, "fragmented": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.policy_training_tools.POLICY_TRAINING_DIR", root):
                self.assertIn("Ambiguous mappings: 1", policy_to_action_mapper())
                self.assertIn("Gapped checks: 1", sop_compliance_checker())
                self.assertIn("Outdated sections: 1", staff_handbook_assistant())
                self.assertIn("Thin modules: 1", training_module_generator())
                self.assertIn("Ambiguous items: 1", quiz_and_exam_generator())
                self.assertIn("Unclear responses: 1", teach_back_evaluator())
                self.assertIn("Mismatched modes: 1", ai_tutor_personality_modes())
                self.assertIn("Stalled markers: 1", skill_progression_tracker())
                self.assertIn("Fading cycles: 1", learning_retention_engine())
                self.assertIn("Fragmented tracks: 1", company_knowledge_academy())

    def test_routes_cover_1741_to_1750(self):
        for phase in range(1741, 1751):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
