import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import core.autonomous_learning as autonomous_learning


class AutonomousLearningOverviewTests(unittest.TestCase):
    def test_overview_returns_structured_state_and_recent_events(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_file = root / "state.json"
            log_file = root / "log.jsonl"

            state_file.write_text(
                json.dumps(
                    {
                        "enabled": True,
                        "started_at": "2026-06-03T00:00:00Z",
                        "last_cycle_at": "2026-06-03T00:05:00Z",
                        "cycle_interval_seconds": 180,
                        "active_domains": [],
                        "schedule": [],
                        "current_task_id": None,
                        "completed_topics": {"programming": ["Laravel"], "medicine": []},
                        "domain_stage_index": {"programming": 1, "medicine": 0},
                        "stats": {
                            "tasks_completed": 4,
                            "topics_learned": 1,
                            "reviews_completed": 1,
                            "syntheses_completed": 1,
                            "errors": 0,
                        },
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )

            log_file.write_text(
                json.dumps(
                    {
                        "type": "learning_task_error",
                        "error": "Example error",
                        "completed_at": "2026-06-03T00:06:00Z",
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            with patch.object(autonomous_learning, "STATE_FILE", state_file), patch.object(
                autonomous_learning, "LOG_FILE", log_file
            ):
                overview = autonomous_learning.get_autonomous_learning_overview(limit=4)

        self.assertTrue(overview["enabled"])
        self.assertEqual(overview["stats"]["topics_learned"], 1)
        self.assertEqual(len(overview["recent_events"]), 1)
        self.assertEqual(overview["recent_events"][0]["type"], "learning_task_error")
        self.assertIn("AUTONOMOUS LEARNING STATUS", overview["status_text"])


if __name__ == "__main__":
    unittest.main()
