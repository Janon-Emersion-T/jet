import string

from core.intent_classifier import classify_intent
from core.ai_fallback import handle_ai_fallback

from core.routes.basic_routes import handle_basic_routes
from core.routes.memory_routes import handle_memory_routes
from core.routes.project_context_routes import handle_project_context_routes
from core.routes.project_analyzer_routes import handle_project_analyzer_routes
from core.routes.dev_ops_routes import handle_dev_ops_routes
from core.routes.framework_routes import handle_framework_routes
from core.routes.patch_routes import handle_patch_routes


def route_command(user_input: str) -> str:
    text = user_input.lower().strip()

    clean_text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    intent = classify_intent(user_input)

    route_handlers = [
        handle_basic_routes,
        handle_memory_routes,
        handle_framework_routes,
        handle_dev_ops_routes,
        handle_project_analyzer_routes,
        handle_project_context_routes,
        handle_patch_routes,
    ]

    for handler in route_handlers:
        if handler == handle_basic_routes:
            response = handler(user_input, text, clean_text, intent)
        else:
            response = handler(user_input, text, clean_text)

        if response is not None:
            return response

    return handle_ai_fallback(user_input)