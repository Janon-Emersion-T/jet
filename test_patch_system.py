import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.patches.safe_writer import SafeWriter


class PatchSystemTests(unittest.TestCase):
    def test_confirm_before_write_blocks_unconfirmed_apply(self):
        with tempfile.TemporaryDirectory() as directory:
            writer = SafeWriter(root=directory)
            result = writer.propose_write(
                "demo_test.txt",
                "Hello from safe Jarvis patch system\n",
                "Testing confirm-before-write mode",
            )

            self.assertEqual(result["status"], "proposal_created")
            proposal_id = result["proposal"]["id"]

            message = writer.apply_proposal(proposal_id, confirm=False)
            self.assertIn("Write blocked.", message)
            self.assertFalse((Path(directory) / "demo_test.txt").exists())

    def test_apply_and_rollback_restore_original_content(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "demo_test.txt"
            target.write_text("original\n", encoding="utf-8")

            writer = SafeWriter(root=directory)
            result = writer.propose_write(
                "demo_test.txt",
                "updated\n",
                "Testing confirmed patch flow",
            )

            proposal_id = result["proposal"]["id"]
            with patch("core.patches.proposal_manager.emit_event") as emit_event:
                self.assertIn("Applied proposal", writer.apply_proposal(proposal_id, confirm=True))
                self.assertEqual(target.read_text(encoding="utf-8"), "updated\n")

                self.assertIn("Rolled back proposal", writer.rollback_proposal(proposal_id))
                self.assertEqual(target.read_text(encoding="utf-8"), "original\n")
                self.assertEqual(emit_event.call_count, 2)


if __name__ == "__main__":
    unittest.main()
