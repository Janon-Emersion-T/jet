from tools.frontend_platform_tools import (
    ui_consistency_checker,
    component_reuse_analyzer,
    framer_motion_assistant,
    react_state_analyzer,
    zustand_redux_analyzer,
    vue_component_analyzer,
    astro_project_analyzer,
    nextjs_analyzer,
    electron_packaging_assistant,
    cross_platform_build_helper,
)


def handle_frontend_platform_routes(user_input: str, text: str, clean_text: str):
    if text in ["ui consistency checker", "check ui consistency"]:
        return ui_consistency_checker()

    if text in ["component reuse analyzer", "analyze component reuse"]:
        return component_reuse_analyzer()

    if text in ["framer motion assistant", "motion assistant"]:
        return framer_motion_assistant()

    if text in ["react state analyzer", "analyze react state"]:
        return react_state_analyzer()

    if text in ["zustand redux analyzer", "redux analyzer", "zustand analyzer"]:
        return zustand_redux_analyzer()

    if text in ["vue component analyzer", "analyze vue components"]:
        return vue_component_analyzer()

    if text in ["astro project analyzer", "analyze astro project"]:
        return astro_project_analyzer()

    if text in ["nextjs analyzer", "next.js analyzer", "next analyzer"]:
        return nextjs_analyzer()

    if text in ["electron packaging assistant", "electron packaging"]:
        return electron_packaging_assistant()

    if text in ["cross platform build helper", "cross-platform build helper"]:
        return cross_platform_build_helper()

    if text in ["frontend platform help", "281 290 help", "phases 281 290"]:
        return """FRONTEND / PLATFORM COMMANDS — PHASES 281–290

281. ui consistency checker
282. component reuse analyzer
283. framer motion assistant
284. react state analyzer
285. zustand redux analyzer
286. vue component analyzer
287. astro project analyzer
288. nextjs analyzer
289. electron packaging assistant
290. cross platform build helper"""

    return None
