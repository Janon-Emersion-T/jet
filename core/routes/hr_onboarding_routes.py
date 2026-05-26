from tools.hr_onboarding_tools import hr_onboarding_workflow


def handle_hr_onboarding_routes(user_input: str, text: str, clean_text: str):
    if text in ["hr onboarding workflow", "hr onboarding", "onboarding workflow", "employee onboarding"]:
        return hr_onboarding_workflow()

    if text in ["347 help", "phase 347 help", "hr onboarding help"]:
        return """HR ONBOARDING WORKFLOW COMMANDS — PHASE 347

347. hr onboarding workflow
     hr onboarding
     onboarding workflow
     employee onboarding
"""

    return None
