from tools.vision_adapter_tools import (
    camera_status,
    capture_camera_image,
    detect_objects_opencv,
    screen_reader_latest_screenshot,
)


def handle_vision_routes(user_input: str, text: str = None, clean_text: str = None):
    cmd = user_input.strip()

    if cmd == "vision help":
        return (
            "VISION COMMANDS\n"
            "- camera status\n"
            "- camera capture\n"
            "- detect objects latest image\n"
            "- screen reader analyze latest screenshot\n\n"
            "Safety: Camera capture requires explicit command. No silent camera opening."
        )

    if cmd == "camera status":
        return camera_status()

    if cmd == "camera capture":
        return capture_camera_image()

    if cmd == "detect objects latest image":
        return detect_objects_opencv()

    if cmd == "screen reader analyze latest screenshot":
        return screen_reader_latest_screenshot()

    return None
