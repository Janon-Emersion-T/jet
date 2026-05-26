from pathlib import Path
from datetime import datetime

VISION_DIR = Path("storage/vision")
VISION_DIR.mkdir(parents=True, exist_ok=True)


def _timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def camera_status():
    try:
        import cv2
        return {"opencv_available": True, "camera_module": "ready_requires_explicit_capture"}
    except Exception as e:
        return {"opencv_available": False, "error": str(e)}


def capture_camera_image(camera_index=0):
    import cv2

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        return {"success": False, "error": "Camera could not be opened."}

    ok, frame = cap.read()
    cap.release()

    if not ok:
        return {"success": False, "error": "Camera opened but capture failed."}

    path = VISION_DIR / f"camera_capture_{_timestamp()}.jpg"
    cv2.imwrite(str(path), frame)

    return {"success": True, "path": str(path)}


def latest_vision_image():
    images = sorted(
        list(VISION_DIR.glob("*.png")) + list(VISION_DIR.glob("*.jpg")) + list(VISION_DIR.glob("*.jpeg")),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return str(images[0]) if images else None


def detect_objects_opencv(image_path=None):
    image_path = image_path or latest_vision_image()
    if not image_path:
        return {"success": False, "error": "No image found in storage/vision."}

    # Safe MVP placeholder: image metadata + future detector adapter point.
    # Later: plug YOLO/OpenCV DNN here.
    try:
        from PIL import Image
        img = Image.open(image_path)
        return {
            "success": True,
            "image": image_path,
            "width": img.width,
            "height": img.height,
            "detector": "opencv_safe_mvp",
            "objects": [],
            "note": "Detector adapter ready. YOLO/OpenCV DNN can be connected later.",
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def screen_reader_latest_screenshot():
    image_path = latest_vision_image()
    if not image_path:
        return {"success": False, "error": "No screenshot/image found in storage/vision."}

    try:
        import pytesseract
        from PIL import Image

        text = pytesseract.image_to_string(Image.open(image_path))
        return {
            "success": True,
            "image": image_path,
            "text": text.strip(),
            "mode": "ocr_screen_reader",
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
