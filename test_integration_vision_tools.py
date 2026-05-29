import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import tools.integration_status_tools as integration_status_tools
from tools import integration_tools, vision_tools


class IntegrationVisionCompatibilityTests(unittest.TestCase):
    def test_integration_tools_help_and_draft_use_temp_storage(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.object(integration_status_tools, "BASE_DIR", root), \
                patch.object(integration_status_tools, "STATUS_FILE", root / "status.json"), \
                patch.object(integration_status_tools, "DRAFTS_FILE", root / "drafts.json"), \
                patch.object(integration_status_tools, "CONTACTS_FILE", root / "contacts.json"), \
                patch.object(integration_status_tools, "CALENDAR_PROPOSALS_FILE", root / "calendar_proposals.json"):
                self.assertIn("PHASES 182-185", integration_tools.integration_help())
                self.assertIn("PHASE 183", integration_tools.gmail_integration_help())
                self.assertIn("GMAIL DRAFT ASSISTANT", integration_tools.gmail_draft_assistant("a@example.com", "Hello", "Body"))
                self.assertIn("INTEGRATION DRAFTS", integration_tools.list_integration_drafts())

    def test_vision_tools_help_and_safe_status_import(self):
        self.assertIn("PHASES 191-195", vision_tools.vision_help())
        self.assertIn("PHASE 193", vision_tools.object_detection_status())
        self.assertIn("PHASE 194", vision_tools.local_vision_model_status())
        self.assertIn("PHASE 195", vision_tools.screen_reader_mode_status())


if __name__ == "__main__":
    unittest.main()
