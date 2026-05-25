from pathlib import Path
from datetime import datetime
import json

VISION_DIR = Path("storage/vision")
SCREENSHOT_DIR = VISION_DIR / "screenshots"
VISION_LOG = VISION_DIR / "vision_requests.json"

MAX_SCREENSHOTS = 50


# ============================================================
# Storage Helpers
# ============================================================

def _ensure():
    VISION_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    if not VISION_LOG.exists():
        VISION_LOG.write_text(json.dumps([], indent=4), encoding="utf-8")


def _load_log():
    _ensure()

    try:
        return json.loads(VISION_LOG.read_text(encoding="utf-8"))
    except Exception:
        return []


def _save_log(items):
    _ensure()
    VISION_LOG.write_text(json.dumps(items, indent=4), encoding="utf-8")


def _record(kind: str, note: str):
    items = _load_log()

    item = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "kind": kind,
        "note": note,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    items.append(item)

    items = items[-200:]

    _save_log(items)

    return item


# ============================================================
# Phase 191 — Screenshot Capture
# ============================================================

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
        _ensure()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"

        path = SCREENSHOT_DIR / filename

        screenshot = pyautogui.screenshot()
        screenshot.save(path)

        _record(
            "screenshot_capture",
            f"Captured screenshot: {filename}"
        )

        return (
            "SCREENSHOT CAPTURED — PHASE 191\n\n"
            f"Saved to:\n{path}"
        )

    except Exception as e:
        return f"Screenshot capture failed: {e}"


def list_screenshots() -> str:
    _ensure()

    files = sorted(
        SCREENSHOT_DIR.glob("*.png"),
        reverse=True
    )

    if not files:
        return "No screenshots found."

    lines = ["SCREENSHOT HISTORY"]

    for file in files[:MAX_SCREENSHOTS]:
        lines.append(f"- {file.name}")

    return "\n".join(lines)


# ============================================================
# Phase 192 — Camera Module
# ============================================================

def camera_module_status() -> str:
    _record("camera_status", "Camera module checked.")

    return """CAMERA MODULE — PHASE 192

Current Mode:
Camera infrastructure ready.

Next step:
Implement OpenCV live capture safely.

Recommended:
- Ask before opening camera
- Never record silently
- Save locally only
"""


# ============================================================
# Phase 193 — Object Detection
# ============================================================

def object_detection_status() -> str:
    _record("object_detection_status", "Object detection checked.")

    return """OBJECT DETECTION MODULE — PHASE 193

Current Mode:
Architecture ready.

Recommended Next Stack:
- OpenCV
- YOLOv8
- ONNX Runtime

Future Features:
- Person detection
- Object labeling
- Real-time analysis
"""


# ============================================================
# Phase 194 — Local Vision
# ============================================================

def local_vision_model_status() -> str:
    _record(
        "local_vision_model_status",
        "Local vision model checked."
    )

    return """LOCAL VISION MODEL — PHASE 194

Current Mode:
Planning infrastructure ready.

Recommended Future:
- Ollama multimodal models
- LLaVA
- Local screenshot reasoning
- UI understanding
"""


# ============================================================
# Phase 195 — Screen Reader
# ============================================================

def screen_reader_mode_status() -> str:
    _record(
        "screen_reader_status",
        "Screen reader checked."
    )

    return """SCREEN READER MODE — PHASE 195

Current Mode:
Screenshot + OCR infrastructure active.

Current Capability:
- Screenshot capture
- OCR text extraction

Future Capability:
- Button detection
- Window understanding
- UI reasoning
- Guided desktop automation
"""


# ============================================================
# Help
# ============================================================

def vision_help() -> str:
    return """VISION COMMANDS — PHASES 191–195

191. capture screenshot
     list screenshots

192. camera module status

193. object detection status

194. local vision model status

195. screen reader mode status
"""
