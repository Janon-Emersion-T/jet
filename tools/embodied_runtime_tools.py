from __future__ import annotations

import json
import os
from pathlib import Path


STORAGE_DIR = Path("storage")
IOT_DIR = STORAGE_DIR / "iot"
MAPPING_DIR = STORAGE_DIR / "mapping"


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _device_entries(filename: str):
    payload = _safe_json(IOT_DIR / filename, {"devices": []})
    if isinstance(payload, dict):
        for key in ("devices", "drones", "robots"):
            if isinstance(payload.get(key), list):
                return payload[key]
    if isinstance(payload, list):
        return payload
    return []


def iot_device_controller() -> str:
    devices = _device_entries("devices.json")
    names = [str(device.get("name", "unnamed")) for device in devices[:5] if isinstance(device, dict)]
    lines = [
        "IOT DEVICE CONTROLLER - PHASE 431",
        "Mode: read-only device registry review.",
        f"Registered devices: {len(devices)}",
        f"Preview: {', '.join(names) if names else 'none'}",
        "Safety: no device command was sent.",
    ]
    return "\n".join(lines)


def drone_command_interface() -> str:
    drones = _device_entries("drones.json")
    autopilot = os.getenv("DRONE_AUTOPILOT_ENDPOINT", "").strip()
    lines = [
        "DRONE COMMAND INTERFACE - PHASE 432",
        "Mode: command-planning only.",
        f"Registered drones: {len(drones)}",
        f"Autopilot endpoint configured: {'YES' if autopilot else 'NO'}",
        "Safety: launch, navigation, and payload commands remain disabled in this phase.",
    ]
    return "\n".join(lines)


def robotics_control_bridge() -> str:
    robots = _device_entries("robots.json")
    ros_master = os.getenv("ROS_MASTER_URI", "").strip()
    lines = [
        "ROBOTICS CONTROL BRIDGE - PHASE 433",
        "Mode: integration readiness review.",
        f"Registered robots: {len(robots)}",
        f"ROS master configured: {'YES' if ros_master else 'NO'}",
        "Recommended bridge: high-level intents -> safety filter -> robot middleware adapter.",
    ]
    return "\n".join(lines)


def vision_guided_automation() -> str:
    camera = os.getenv("VISION_CAMERA_SOURCE", "").strip() or "not configured"
    model = os.getenv("VISION_MODEL", "").strip() or "generic detector"
    return "\n".join(
        [
            "VISION-GUIDED AUTOMATION - PHASE 434",
            "Mode: perception pipeline preview.",
            f"Camera source: {camera}",
            f"Vision model: {model}",
            "Safety: detections should inform plans and confirmations before any physical-world actuation.",
        ]
    )


def real_world_mapping_engine() -> str:
    maps = sorted(MAPPING_DIR.glob("*.json")) if MAPPING_DIR.exists() else []
    map_names = [path.name for path in maps[:5]]
    return "\n".join(
        [
            "REAL-WORLD MAPPING ENGINE - PHASE 435",
            "Mode: map inventory and planning review.",
            f"Map files discovered: {len(maps)}",
            f"Preview: {', '.join(map_names) if map_names else 'none'}",
            "Recommended layers: rooms, obstacles, beacons, charging docks, and trust zones.",
        ]
    )
