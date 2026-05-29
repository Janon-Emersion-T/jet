import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.metaverse_governance_tools import *


class MetaverseGovernanceTests(unittest.TestCase):
    def test_metaverse_governance_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "immersive_experience.json": {"experiences": [{"immersive": True, "unsafe": True}, {"immersive": False, "unsafe": False}]},
                "augmented_cognition.json": {"augmentations": [{"amplified": True, "overloaded": True}, {"amplified": False, "overloaded": False}]},
                "metaverse_governance.json": {"realms": [{"governed": True, "captured": True}, {"governed": False, "captured": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.metaverse_governance_tools.METAVERSE_GOVERNANCE_DIR", root):
                self.assertIn("Unsafe experiences: 1", autonomous_immersive_experience_substrate())
                self.assertIn("Overloaded augmentations: 1", infinite_scale_augmented_cognition_layer())
                self.assertIn("Captured realms: 1", recursive_metaverse_governance_ai())

    def test_routes_cover_1098_to_1100(self):
        for phase in range(1098, 1101):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
