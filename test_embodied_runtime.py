import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.embodied_runtime_tools import (
    drone_command_interface,
    iot_device_controller,
    real_world_mapping_engine,
    robotics_control_bridge,
    vision_guided_automation,
)


class EmbodiedRuntimeTests(unittest.TestCase):
    def test_iot_and_mapping_inventory_render(self):
        with tempfile.TemporaryDirectory() as directory:
            storage = Path(directory)
            iot_dir = storage / "iot"
            mapping_dir = storage / "mapping"
            iot_dir.mkdir()
            mapping_dir.mkdir()
            (iot_dir / "devices.json").write_text(json.dumps({"devices": [{"name": "desk-lamp"}]}), encoding="utf-8")
            (mapping_dir / "office.json").write_text(json.dumps({"rooms": ["office"]}), encoding="utf-8")
            with patch("tools.embodied_runtime_tools.IOT_DIR", iot_dir), \
                    patch("tools.embodied_runtime_tools.MAPPING_DIR", mapping_dir):
                iot = iot_device_controller()
                mapping = real_world_mapping_engine()
        self.assertIn("Registered devices: 1", iot)
        self.assertIn("desk-lamp", iot)
        self.assertIn("Map files discovered: 1", mapping)
        self.assertIn("office.json", mapping)

    def test_drone_robotics_and_vision_render(self):
        with tempfile.TemporaryDirectory() as directory:
            storage = Path(directory)
            iot_dir = storage / "iot"
            iot_dir.mkdir()
            (iot_dir / "drones.json").write_text(json.dumps({"drones": [{"name": "quad-1"}]}), encoding="utf-8")
            (iot_dir / "robots.json").write_text(json.dumps({"robots": [{"name": "arm-1"}]}), encoding="utf-8")
            with patch("tools.embodied_runtime_tools.IOT_DIR", iot_dir), patch.dict(
                os.environ,
                {
                    "DRONE_AUTOPILOT_ENDPOINT": "udp://127.0.0.1:14550",
                    "ROS_MASTER_URI": "http://127.0.0.1:11311",
                    "VISION_CAMERA_SOURCE": "/dev/video0",
                    "VISION_MODEL": "yolo-small",
                },
                clear=False,
            ):
                drone = drone_command_interface()
                robotics = robotics_control_bridge()
                vision = vision_guided_automation()
        self.assertIn("Registered drones: 1", drone)
        self.assertIn("Autopilot endpoint configured: YES", drone)
        self.assertIn("Registered robots: 1", robotics)
        self.assertIn("ROS master configured: YES", robotics)
        self.assertIn("/dev/video0", vision)
        self.assertIn("yolo-small", vision)

    def test_routes_cover_431_to_435(self):
        for phase in range(431, 436):
            result = handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help")
            self.assertIsNotNone(result, f"missing route for {phase}")


if __name__ == "__main__":
    unittest.main()
