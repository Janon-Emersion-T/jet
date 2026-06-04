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
            manifest_dir = root / "manifests"
            programming_log_file = root / "programming_learning_log.jsonl"
            programming_manifest_dir = root / "programming_manifests"
            manifest_dir.mkdir(parents=True, exist_ok=True)
            programming_manifest_dir.mkdir(parents=True, exist_ok=True)

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
            ), patch.object(
                autonomous_learning, "MANIFEST_DIR", manifest_dir
            ), patch.object(
                autonomous_learning, "PROGRAMMING_LOG_FILE", programming_log_file
            ), patch.object(
                autonomous_learning, "PROGRAMMING_KNOWLEDGE_MANIFEST_DIR", programming_manifest_dir
            ):
                overview = autonomous_learning.get_autonomous_learning_overview(limit=4)

        self.assertTrue(overview["enabled"])
        self.assertEqual(overview["stats"]["topics_learned"], 1)
        self.assertEqual(len(overview["recent_events"]), 1)
        self.assertEqual(overview["recent_events"][0]["type"], "learning_task_error")
        self.assertIn("AUTONOMOUS LEARNING STATUS", overview["status_text"])

    def test_burst_returns_multiple_cycles_and_overview(self):
        with patch.object(
            autonomous_learning,
            "run_autonomous_learning_cycle",
            side_effect=[{"task": "one"}, {"task": "two"}, None],
        ) as cycle_mock, patch.object(
            autonomous_learning,
            "get_autonomous_learning_overview",
            return_value={"queue_depth": 0},
        ) as overview_mock, patch.object(
            autonomous_learning,
            "autonomous_learning_status",
            return_value="burst-status",
        ):
            result = autonomous_learning.run_autonomous_learning_burst(max_cycles=4)

        self.assertEqual(cycle_mock.call_count, 3)
        self.assertEqual(overview_mock.call_count, 1)
        self.assertEqual(result["completed_cycles"], 2)
        self.assertEqual(result["status"], "burst-status")

    def test_load_state_recovers_completed_topics_from_logs_and_manifests(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_file = root / "state.json"
            log_file = root / "log.jsonl"
            manifest_dir = root / "manifests"
            programming_log_file = root / "programming_learning_log.jsonl"
            programming_manifest_dir = root / "programming_manifests"
            manifest_dir.mkdir(parents=True, exist_ok=True)
            programming_manifest_dir.mkdir(parents=True, exist_ok=True)

            state_file.write_text(
                json.dumps(
                    {
                        "enabled": True,
                        "started_at": "2026-06-03T00:00:00Z",
                        "active_domains": ["programming", "medicine"],
                        "schedule": [
                            {
                                "id": "task-1",
                                "domain": "programming",
                                "topic": "Laravel",
                                "kind": "learn",
                                "stage": "Manual",
                                "status": "pending",
                                "created_at": "2026-06-03T00:00:00Z",
                                "started_at": None,
                                "completed_at": None,
                                "metadata": {},
                            }
                        ],
                        "current_task_id": None,
                        "completed_topics": {"programming": [], "medicine": []},
                        "domain_stage_index": {"programming": 0, "medicine": 0},
                        "stats": {
                            "tasks_completed": 0,
                            "topics_learned": 0,
                            "reviews_completed": 0,
                            "syntheses_completed": 0,
                            "errors": 0,
                        },
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )

            log_file.write_text(
                "\n".join(
                    [
                        json.dumps(
                            {
                                "type": "generic_topic_learning",
                                "domain": "programming",
                                "topic": "Laravel",
                                "started_at": "2026-06-03T00:00:00Z",
                                "completed_at": "2026-06-03T00:10:00Z",
                            }
                        ),
                        json.dumps(
                            {
                                "type": "generic_topic_learning",
                                "domain": "medicine",
                                "topic": "Cardiology",
                                "started_at": "2026-06-03T01:00:00Z",
                                "completed_at": "2026-06-03T01:10:00Z",
                            }
                        ),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            (manifest_dir / "programming_python.json").write_text(
                json.dumps(
                    {
                        "domain": "programming",
                        "topic": "Python",
                        "updated_at": "2026-06-03T02:00:00Z",
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
            programming_log_file.write_text(
                json.dumps(
                    {
                        "topic": "Go",
                        "started_at": "2026-06-03T03:00:00Z",
                        "completed_at": "2026-06-03T03:10:00Z",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            (programming_manifest_dir / "rust_knowledge_manifest.json").write_text(
                json.dumps(
                    {
                        "topic": "Rust",
                        "updated_at": "2026-06-03T04:00:00Z",
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )

            with patch.object(autonomous_learning, "STATE_FILE", state_file), patch.object(
                autonomous_learning, "LOG_FILE", log_file
            ), patch.object(
                autonomous_learning, "MANIFEST_DIR", manifest_dir
            ), patch.object(
                autonomous_learning, "PROGRAMMING_LOG_FILE", programming_log_file
            ), patch.object(
                autonomous_learning, "PROGRAMMING_KNOWLEDGE_MANIFEST_DIR", programming_manifest_dir
            ):
                state = autonomous_learning._load_state()

        self.assertEqual(state["completed_topics"]["programming"], ["Laravel", "Python", "Go", "Rust"])
        self.assertEqual(state["completed_topics"]["medicine"], ["Cardiology"])
        self.assertEqual(state["stats"]["topics_learned"], 5)
        self.assertEqual(state["schedule"][0]["status"], "completed")


if __name__ == "__main__":
    unittest.main()
