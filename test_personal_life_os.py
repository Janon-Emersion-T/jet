import json
import os
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.personal_life_os_tools import (
    fitness_assistant_integration,
    goal_execution_planner,
    habit_tracking_engine,
    nutrition_planning_assistant,
    personal_life_operating_system,
    sleep_work_pattern_analyzer,
    stress_detection_assistant,
)


class PersonalLifeOSTests(unittest.TestCase):
    def test_habits_goals_sleep_and_stress_render(self):
        with tempfile.TemporaryDirectory() as directory:
            life_os = Path(directory)
            today = date.today().isoformat()
            (life_os / "habits.json").write_text(
                json.dumps({"habits": [{"name": "walk", "active": True, "completed_dates": [today]}]}),
                encoding="utf-8",
            )
            (life_os / "goals.json").write_text(
                json.dumps({"goals": [{"title": "Ship phase batch", "status": "open"}]}),
                encoding="utf-8",
            )
            (life_os / "sleep_log.json").write_text(
                json.dumps({"entries": [{"sleep_hours": 7.5}, {"sleep_hours": 6.5}]}),
                encoding="utf-8",
            )
            (life_os / "wellness_signals.json").write_text(
                json.dumps({"stress_score": 8}),
                encoding="utf-8",
            )
            with patch("tools.personal_life_os_tools.LIFE_OS_DIR", life_os), \
                    patch("tools.personal_life_os_tools.HABITS_FILE", life_os / "habits.json"), \
                    patch("tools.personal_life_os_tools.GOALS_FILE", life_os / "goals.json"), \
                    patch("tools.personal_life_os_tools.SLEEP_FILE", life_os / "sleep_log.json"), \
                    patch("tools.personal_life_os_tools.WELLNESS_FILE", life_os / "wellness_signals.json"):
                personal = personal_life_operating_system()
                habits = habit_tracking_engine()
                goals = goal_execution_planner()
                sleep = sleep_work_pattern_analyzer()
                stress = stress_detection_assistant()
        self.assertIn("Habit entries: 1", personal)
        self.assertIn("Completed today: 1", habits)
        self.assertIn("Open goals: 1", goals)
        self.assertIn("Average sleep hours: 7.0", sleep)
        self.assertIn("Stress level: HIGH", stress)

    def test_fitness_nutrition_and_route_coverage(self):
        with tempfile.TemporaryDirectory() as directory:
            life_os = Path(directory)
            (life_os / "fitness.json").write_text(json.dumps({"steps_today": 8240}), encoding="utf-8")
            (life_os / "nutrition.json").write_text(json.dumps({"calories_today": 2150, "protein_g": 145}), encoding="utf-8")
            with patch("tools.personal_life_os_tools.LIFE_OS_DIR", life_os), \
                    patch("tools.personal_life_os_tools.FITNESS_FILE", life_os / "fitness.json"), \
                    patch("tools.personal_life_os_tools.NUTRITION_FILE", life_os / "nutrition.json"), \
                    patch.dict(os.environ, {"GOOGLE_FIT_CREDENTIALS": "configured"}, clear=False):
                fitness = fitness_assistant_integration()
                nutrition = nutrition_planning_assistant()
        self.assertIn("Provider: google_fit", fitness)
        self.assertIn("Steps today: 8240", fitness)
        self.assertIn("Calories today: 2150", nutrition)
        self.assertIn("Protein grams: 145", nutrition)
        for phase in range(443, 451):
            result = handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help")
            self.assertIsNotNone(result, f"missing route for {phase}")


if __name__ == "__main__":
    unittest.main()
