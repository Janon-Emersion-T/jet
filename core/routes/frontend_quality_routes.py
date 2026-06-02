from tools.frontend_quality_tools import (
    vite_chunk_analyzer,
    js_bundle_size_analyzer,
    frontend_performance_profiler,
    tailwind_class_optimizer,
    css_dead_class_detector,
    accessibility_checker,
    wcag_compliance_advisor,
    color_contrast_analyzer,
    responsive_layout_analyzer,
    mobile_first_audit,
    visual_hierarchy_audit,
    image_readiness_audit,
)


def handle_frontend_quality_routes(user_input: str, text: str, clean_text: str):
    if text == "vite chunk analyzer":
        return vite_chunk_analyzer()

    if text == "js bundle size analyzer":
        return js_bundle_size_analyzer()

    if text == "frontend performance profiler":
        return frontend_performance_profiler()

    if text == "tailwind class optimizer":
        return tailwind_class_optimizer()

    if text == "css dead class detector":
        return css_dead_class_detector()

    if text == "accessibility checker":
        return accessibility_checker()

    if text == "wcag compliance advisor":
        return wcag_compliance_advisor()

    if text == "color contrast analyzer":
        return color_contrast_analyzer()

    if text == "responsive layout analyzer":
        return responsive_layout_analyzer()

    if text == "mobile-first audit" or text == "mobile first audit":
        return mobile_first_audit()

    if text in ["visual hierarchy audit", "visual hierarchy"] or "visual hierarchy" in text:
        return visual_hierarchy_audit()

    if text in ["image readiness audit", "frontend image audit"] or (
        "image" in text and any(phrase in text for phrase in ["readiness", "frontend audit", "unsplash", "image audit"])
    ):
        return image_readiness_audit()

    return None
