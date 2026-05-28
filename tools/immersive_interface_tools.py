from __future__ import annotations

import json
import os
from pathlib import Path

from tools.embodied_runtime_tools import IOT_DIR, MAPPING_DIR
from tools.vision_adapter_tools import VISION_DIR, latest_vision_image


IMMERSIVE_DIR = Path("storage/immersive")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _mapping_files():
    if not MAPPING_DIR.exists():
        return []
    return sorted(MAPPING_DIR.glob("*.json"))


def indoor_navigation_assistant() -> str:
    maps = _mapping_files()
    beacons = _safe_json(IMMERSIVE_DIR / "beacons.json", {"beacons": []})
    beacon_count = len(beacons.get("beacons", [])) if isinstance(beacons, dict) else 0
    return "\n".join(
        [
            "INDOOR NAVIGATION ASSISTANT - PHASE 436",
            "Mode: local map and beacon readiness review.",
            f"Map files available: {len(maps)}",
            f"Beacon definitions: {beacon_count}",
            "Recommended layers: rooms, hallways, doors, stairs, charger points, and trust zones.",
        ]
    )


def ar_overlay_assistant() -> str:
    latest_image = latest_vision_image()
    anchor_data = _safe_json(IMMERSIVE_DIR / "anchors.json", {"anchors": []})
    anchor_count = len(anchor_data.get("anchors", [])) if isinstance(anchor_data, dict) else 0
    return "\n".join(
        [
            "AR OVERLAY ASSISTANT - PHASE 437",
            "Mode: overlay planning preview.",
            f"Latest visual frame: {latest_image or 'none'}",
            f"Overlay anchors: {anchor_count}",
            "Suggested overlays: navigation arrows, device labels, safety zones, and task hints.",
        ]
    )


def virtual_avatar_interface() -> str:
    profile = _safe_json(IMMERSIVE_DIR / "avatar_profile.json", {})
    persona = profile.get("persona", "Alfred") if isinstance(profile, dict) else "Alfred"
    style = profile.get("style", "calm assistant") if isinstance(profile, dict) else "calm assistant"
    return "\n".join(
        [
            "VIRTUAL AVATAR INTERFACE - PHASE 438",
            "Mode: avatar persona configuration preview.",
            f"Persona: {persona}",
            f"Style: {style}",
            "Recommended channels: voice, expression presets, proactive alerts, and approval-state feedback.",
        ]
    )


def holographic_ui_prototype_mode() -> str:
    headset = os.getenv("XR_DEVICE_PROFILE", "").strip() or "generic_spatial_display"
    return "\n".join(
        [
            "HOLOGRAPHIC UI PROTOTYPE MODE - PHASE 439",
            "Mode: spatial UI planning.",
            f"Target display profile: {headset}",
            "Prototype surfaces: floating status cards, command ribbon, room map, and attention alerts.",
            "Safety: prototype-only; no hardware control or privileged execution is enabled here.",
        ]
    )


def gesture_control_interface() -> str:
    model = os.getenv("GESTURE_MODEL", "").strip() or "not configured"
    latest_image = latest_vision_image()
    return "\n".join(
        [
            "GESTURE CONTROL INTERFACE - PHASE 440",
            "Mode: gesture pipeline readiness review.",
            f"Gesture model: {model}",
            f"Latest frame source: {latest_image or 'none'}",
            "Recommended gesture set: confirm, cancel, scroll, highlight, and emergency stop.",
        ]
    )


def brain_computer_interface_research_layer() -> str:
    backend = os.getenv("BCI_BACKEND", "").strip() or "research_only"
    stream = os.getenv("BCI_STREAM_ENDPOINT", "").strip()
    return "\n".join(
        [
            "BRAIN-COMPUTER INTERFACE RESEARCH LAYER - PHASE 441",
            "Mode: research readiness review.",
            f"Backend: {backend}",
            f"Stream endpoint configured: {'YES' if stream else 'NO'}",
            "Policy: treat BCI signals as experimental advisory input until consent, calibration, and safety rules are defined.",
        ]
    )


def digital_twin_system() -> str:
    maps = _mapping_files()
    devices = _safe_json(IOT_DIR / "devices.json", {"devices": []})
    avatar = _safe_json(IMMERSIVE_DIR / "avatar_profile.json", {})
    device_count = len(devices.get("devices", [])) if isinstance(devices, dict) else 0
    return "\n".join(
        [
            "DIGITAL TWIN SYSTEM - PHASE 442",
            "Mode: twin inventory summary.",
            f"Spatial maps: {len(maps)}",
            f"Connected device entries: {device_count}",
            f"Avatar profile present: {'YES' if bool(avatar) else 'NO'}",
            "Recommended twin domains: environment, devices, routines, goals, and system health.",
        ]
    )
