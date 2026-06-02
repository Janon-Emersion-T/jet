import re

from tools.web_development_tools import (
    build_web_development_plan,
    create_laravel_app_from_request,
    infer_web_development_action,
    generate_laravel_module,
    format_web_development_plan,
)


def handle_web_development_routes(user_input: str, text: str, clean_text: str):
    combined = f"{user_input}\n{clean_text}".lower()
    action = infer_web_development_action(user_input)

    if action["action"] == "create":
        return create_laravel_app_from_request(user_input)

    if action["action"] == "module":
        return generate_laravel_module(user_input)

    if action["action"] == "plan":
        plan = build_web_development_plan(user_input)
        return format_web_development_plan(plan)

    # Natural-language fallback: if the module was selected, always return a
    # concrete answer rather than leaving dispatch to emit a forced error.
    if re.search(r"\b(laravel|blade|tailwind|alpine|vite|web app|web application|saas|project)\b", combined):
        if any(term in combined for term in ["create", "build", "make", "scaffold", "install", "generate"]):
            return create_laravel_app_from_request(user_input)

        return format_web_development_plan(build_web_development_plan(user_input))

    return None
