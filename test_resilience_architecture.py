import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.resilience_architecture_tools import (
    ai_decision_replay_engine,
    autonomous_retry_engine,
    event_sourcing_architecture,
    failure_recovery_orchestration,
    immutable_operational_audit_log,
)


class ResilienceArchitectureTests(unittest.TestCase):
    def test_retry_recovery_sourcing_audit_and_replay_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "retries.json").write_text(
                json.dumps({"jobs": [{"retries": 2, "cap_reached": False}, {"retries": 5, "cap_reached": True}]}),
                encoding="utf-8",
            )
            (root / "recovery.json").write_text(
                json.dumps({"incidents": [{"recoverable": True, "runbook": "rb-1"}, {"recoverable": False}]}),
                encoding="utf-8",
            )
            (root / "event_sourcing.json").write_text(
                json.dumps({"aggregates": [1, 2], "streams": [1], "snapshots": [1, 2, 3]}),
                encoding="utf-8",
            )
            (root / "audit_log.json").write_text(
                json.dumps({"append_only": True, "entries": [{"signed": True}, {"signed": False}]}),
                encoding="utf-8",
            )
            (root / "decision_replay.json").write_text(
                json.dumps({"decisions": [{"replayable": True, "diverged": False}, {"replayable": True, "diverged": True}]}),
                encoding="utf-8",
            )
            with patch("tools.resilience_architecture_tools.RESILIENCE_DIR", root):
                retry = autonomous_retry_engine()
                recovery = failure_recovery_orchestration()
                sourcing = event_sourcing_architecture()
                audit = immutable_operational_audit_log()
                replay = ai_decision_replay_engine()
        self.assertIn("Jobs with retries: 2", retry)
        self.assertIn("Jobs at retry cap: 1", retry)
        self.assertIn("Recoverable incidents: 1", recovery)
        self.assertIn("Runbook-linked incidents: 1", recovery)
        self.assertIn("Aggregates tracked: 2", sourcing)
        self.assertIn("Snapshots configured: 3", sourcing)
        self.assertIn("Append-only flag: YES", audit)
        self.assertIn("Signed entries: 1", audit)
        self.assertIn("Replayable decisions: 2", replay)
        self.assertIn("Divergent replays: 1", replay)

    def test_routes_cover_511_to_515(self):
        for phase in range(511, 516):
            result = handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help")
            self.assertIsNotNone(result, f"missing route for {phase}")


if __name__ == "__main__":
    unittest.main()
