from pathlib import Path
This reads visible text only. It does not click, type, or control the desktop.
"""


def read_latest_screenshot() -> str:
    path = _latest_screenshot()
    if path is None:
        return "No screenshot found. Run: capture screenshot"
    return _ocr_image(path, "SCREEN READER RESULT — PHASE 195")


def capture_and_read_screen() -> str:
    capture_result = capture_screenshot()
    if not capture_result.startswith("SCREENSHOT CAPTURED"):
        return capture_result
    return read_latest_screenshot()


def _ocr_image(path: Path, title: str) -> str:
    try:
        from PIL import Image
        import pytesseract
    except Exception:
        return "Screen reader OCR requires dependencies:\npip install pytesseract pillow\nsudo apt install tesseract-ocr -y"

    try:
        image = Image.open(path)
        text = pytesseract.image_to_string(image)
        text = _limit_output(text)
        _record("screen_reader_ocr", f"OCR completed for {path.name}", {"path": str(path), "chars": len(text)})

        if not text:
            return f"{title}\n\nFile: {path.name}\nNo readable text detected."

        return f"{title}\n\nFile: {path.name}\n\n{text}"
    except Exception as e:
        return f"Screen reader OCR failed: {e}"


# Help

def vision_help() -> str:
    return """VISION COMMANDS — PHASES 191–195

191. capture screenshot
     list screenshots

192. camera module status
     capture camera image
     capture camera image <device_index>

193. object detection status
     detect objects in latest screenshot
     detect objects in latest camera image

194. local vision model status
     vision config status

195. screen reader mode status
     read latest screenshot
     capture and read screen
"""