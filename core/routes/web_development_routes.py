import re

from tools.web_development_tools import (
    build_web_development_plan,
    create_laravel_app_from_request,
    generate_laravel_module,
    format_web_development_plan,
)


def handle_web_development_routes(user_input: str, text: str, clean_text: str):
    combined = f"{user_input}\n{clean_text}".lower()

    if re.search(r"\b(create|build|make|scaffold).{0,60}\blaravel\b", combined) or "web application" in combined:
        return create_laravel_app_from_request(user_input)

    if any(term in combined for term in ["plan", "break down", "task breakdown", "roadmap", "architecture", "readme", "module"]):
        plan = build_web_development_plan(user_input)
        return format_web_development_plan(plan)

    if any(term in combined for term in ["generate migration", "generate controller", "generate model", "generate view", "generate readme"]):
        return generate_laravel_module(user_input)

    return None
