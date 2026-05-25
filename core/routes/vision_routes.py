from tools.vision_tools import (
    capture_screenshot,
    list_screenshots,
    camera_module_status,
    object_detection_status,
    local_vision_model_status,
    screen_reader_mode_status,
    vision_help,
)


def handle_vision_routes(user_input: str, text: str, clean_text: str):

    if text in ["vision help", "camera help"]:
        return vision_help()

    # ========================================================
    # Phase 191
    # ========================================================

    if text in ["capture screenshot", "take screenshot"]:
        return capture_screenshot()

    if text in ["list screenshots", "show screenshots"]:
        return list_screenshots()

    # ========================================================
    # Phase 192
    # ========================================================

    if text in ["camera module status", "camera status"]:
        return camera_module_status()

    # ========================================================
    # Phase 193
    # ========================================================

    if text in ["object detection status", "object detection module"]:
        return object_detection_status()

    # ========================================================
    # Phase 194
    # ========================================================

    if text in ["local vision model status", "vision model status"]:
        return local_vision_model_status()

    # ========================================================
    # Phase 195
    # ========================================================

    if text in ["screen reader mode status", "screen reader status"]:
        return screen_reader_mode_status()

    return None
