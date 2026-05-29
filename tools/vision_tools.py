from __future__ import annotations

from pathlib import Path

from tools.vision_adapter_tools import (
    camera_status,
    capture_camera_image,
    detect_objects_opencv,
    latest_vision_image,
    screen_reader_latest_screenshot,
)


VISION_DIR = Path("storage/vision")
SCREENSHOT_DIR = VISION_DIR / "screenshots"
MAX_SCREENSHOTS = 50


def capture_screenshot() -> str:
    try:
        import pyautogui
    except Exception:
        return (
            "Screenshot capture requires pyautogui.\n\n"
            "Install with:\n"
            "pip install pyautogui pillow\n"
            "sudo apt install scrot -y"
        )

    try:
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        path = SCREENSHOT_DIR / "latest_screenshot.png"
        pyautogui.screenshot().save(path)
        return f"SCREENSHOT CAPTURED - PHASE 191\n\nSaved to:\n{path}"
    except Exception as exc:
        return f"Screenshot capture failed: {exc}"


def list_screenshots() -> str:
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    files = sorted(SCREENSHOT_DIR.glob("*.png"), key=lambda item: item.stat().st_mtime, reverse=True)
    if not files:
        return "No screenshots found."

    lines = ["SCREENSHOT HISTORY"]
    for file in files[:MAX_SCREENSHOTS]:
        lines.append(f"- {file.name}")
    return "\n".join(lines)


def camera_module_status() -> str:
    status = camera_status()
    if status.get("opencv_available"):
        return "CAMERA MODULE - PHASE 192\nStatus: ready, explicit capture required."
    return f"CAMERA MODULE - PHASE 192\nStatus: unavailable\nReason: {status.get('error', 'unknown')}"


def capture_camera_image_status(camera_index: int = 0) -> str:
    result = capture_camera_image(camera_index)
    if result.get("success"):
        return f"CAMERA IMAGE CAPTURED - PHASE 192\nSaved to:\n{result['path']}"
    return f"Camera capture failed: {result.get('error', 'unknown error')}"


def object_detection_status() -> str:
    return (
        "OBJECT DETECTION MODULE - PHASE 193\n"
        "Status: adapter ready.\n"
        "Safety: detection reads existing local images only unless capture is explicitly requested."
    )


def detect_objects_in_latest_image() -> str:
    result = detect_objects_opencv()
    if not result.get("success"):
        return f"Object detection failed: {result.get('error', 'unknown error')}"
    return "\n".join(
        [
            "OBJECT DETECTION RESULT - PHASE 193",
            f"Image: {result['image']}",
            f"Size: {result['width']}x{result['height']}",
            f"Objects detected: {len(result.get('objects', []))}",
            result.get("note", "Detector completed."),
        ]
    )


def local_vision_model_status() -> str:
    return (
        "LOCAL VISION MODEL - PHASE 194\n"
        "Status: local adapter ready.\n"
        "Recommended: connect a multimodal local model only through an explicit, permissioned command."
    )


def screen_reader_mode_status() -> str:
    return (
        "SCREEN READER MODE - PHASE 195\n"
        "Status: OCR adapter ready.\n"
        "Safety: this reads visible text only. It does not click, type, or control the desktop."
    )


def read_latest_screenshot() -> str:
    image = latest_vision_image()
    if image is None:
        return "No screenshot found. Run: capture screenshot"

    result = screen_reader_latest_screenshot()
    if not result.get("success"):
        return f"Screen reader OCR failed: {result.get('error', 'unknown error')}"
    text = result.get("text") or "No readable text detected."
    return f"SCREEN READER RESULT - PHASE 195\n\nFile: {Path(result['image']).name}\n\n{text}"


def capture_and_read_screen() -> str:
    capture_result = capture_screenshot()
    if not capture_result.startswith("SCREENSHOT CAPTURED"):
        return capture_result
    return read_latest_screenshot()


def vision_help() -> str:
    return """VISION COMMANDS - PHASES 191-195

191. capture screenshot
     list screenshots

192. camera module status
     capture camera image

193. object detection status
     detect objects in latest image

194. local vision model status

195. screen reader mode status
     read latest screenshot
     capture and read screen
"""
