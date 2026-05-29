import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.immersive_interface_tools import (
    ar_overlay_assistant,
    digital_twin_system,
    indoor_navigation_assistant,
    virtual_avatar_interface,
)


class ImmersiveInterfaceTests(unittest.TestCase):
    def test_navigation_overlay_and_avatar_render(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            mapping_dir = base / "mapping"
            immersive_dir = base / "immersive"
            vision_dir = base / "vision"
            mapping_dir.mkdir()
            immersive_dir.mkdir()
            vision_dir.mkdir()
            (mapping_dir / "floor1.json").write_text(json.dumps({"rooms": ["lab"]}), encoding="utf-8")
            (immersive_dir / "beacons.json").write_text(json.dumps({"beacons": [{"id": "A1"}]}), encoding="utf-8")
            (immersive_dir / "anchors.json").write_text(json.dumps({"anchors": [{"id": "desk"}]}), encoding="utf-8")
            (immersive_dir / "avatar_profile.json").write_text(json.dumps({"persona": "Alfred", "style": "calm butler"}), encoding="utf-8")
            (vision_dir / "frame.jpg").write_text("placeholder", encoding="utf-8")
            with patch("tools.immersive_interface_tools.MAPPING_DIR", mapping_dir), \
                    patch("tools.immersive_interface_tools.IMMERSIVE_DIR", immersive_dir), \
                    patch("tools.vision_adapter_tools.VISION_DIR", vision_dir):
                navigation = indoor_navigation_assistant()
                overlay = ar_overlay_assistant()
                avatar = virtual_avatar_interface()
        self.assertIn("Map files available: 1", navigation)
        self.assertIn("Beacon definitions: 1", navigation)
        self.assertIn("Overlay anchors: 1", overlay)
        self.assertIn("frame.jpg", overlay)
        self.assertIn("Persona: Alfred", avatar)
        self.assertIn("Style: calm butler", avatar)

    def test_digital_twin_and_route_coverage(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            mapping_dir = base / "mapping"
            immersive_dir = base / "immersive"
            iot_dir = base / "iot"
            mapping_dir.mkdir()
            immersive_dir.mkdir()
            iot_dir.mkdir()
            (mapping_dir / "office.json").write_text(json.dumps({"rooms": ["office"]}), encoding="utf-8")
            (immersive_dir / "avatar_profile.json").write_text(json.dumps({"persona": "Ada"}), encoding="utf-8")
            (iot_dir / "devices.json").write_text(json.dumps({"devices": [{"name": "lamp"}]}), encoding="utf-8")
            with patch("tools.immersive_interface_tools.MAPPING_DIR", mapping_dir), \
                    patch("tools.immersive_interface_tools.IMMERSIVE_DIR", immersive_dir), \
                    patch("tools.immersive_interface_tools.IOT_DIR", iot_dir), \
                    patch.dict(os.environ, {"XR_DEVICE_PROFILE": "vision-pro", "GESTURE_MODEL": "mediapipe", "BCI_BACKEND": "openbci"}, clear=False):
                twin = digital_twin_system()
        self.assertIn("Spatial maps: 1", twin)
        self.assertIn("Connected device entries: 1", twin)
        for phase in range(436, 443):
            result = handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help")
            self.assertIsNotNone(result, f"missing route for {phase}")


if __name__ == "__main__":
    unittest.main()
