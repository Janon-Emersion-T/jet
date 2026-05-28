import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.human_support_accessibility_tools import *


class HumanSupportAccessibilityTests(unittest.TestCase):
    def test_human_support_accessibility_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "archaeology.json": {"sites": [{"modeled": True, "risk": "fragile"}, {"modeled": False, "risk": "stable"}]},
                "language_revival.json": {"languages": [{"status": "active", "community_led": True}, {"status": "paused", "community_led": False}]},
                "education_civilization.json": {"systems": [{"adaptive": True, "equitable": True}, {"adaptive": False, "equitable": False}]},
                "lifelong_learning.json": {"learners": [{"status": "active", "personalized": True}, {"status": "idle", "personalized": False}]},
                "childhood_education.json": {"cohorts": [{"supervised": True, "age_appropriate": True}, {"supervised": False, "age_appropriate": False}]},
                "cognitive_development.json": {"profiles": [{"supported": True, "reviewed": True}, {"supported": False, "reviewed": False}]},
                "elderly_care.json": {"care_plans": [{"assisted": True, "priority": "urgent"}, {"assisted": False, "priority": "normal"}]},
                "accessibility_framework.json": {"services": [{"accessible": True, "gap": True}, {"accessible": False, "gap": False}]},
                "sign_language.json": {"sessions": [{"translated": True, "reviewed": True}, {"translated": False, "reviewed": False}]},
                "visual_impairment.json": {"supports": [{"status": "active", "high_confidence": True}, {"status": "idle", "high_confidence": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.human_support_accessibility_tools.HUMAN_SUPPORT_DIR", root):
                self.assertIn("Fragile sites: 1", archaeological_simulation_assistant())
                self.assertIn("Community-led programs: 1", language_revival_framework())
                self.assertIn("Equity-aware systems: 1", autonomous_education_civilization_model())
                self.assertIn("Personalized paths: 1", personalized_lifelong_learning_ai())
                self.assertIn("Age-appropriate cohorts: 1", ai_guided_childhood_education())
                self.assertIn("Reviewed profiles: 1", cognitive_development_assistant())
                self.assertIn("Urgent care plans: 1", elderly_care_ai_ecosystem())
                self.assertIn("Accessibility gaps: 1", accessibility_first_ai_framework())
                self.assertIn("Reviewed sessions: 1", ai_sign_language_interpreter())
                self.assertIn("High-confidence sessions: 1", visual_impairment_assistant())

    def test_routes_cover_711_to_720(self):
        for phase in range(711, 721):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
