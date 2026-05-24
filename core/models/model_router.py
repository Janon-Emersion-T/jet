from core.models.model_config import load_model_settings


CODING_KEYWORDS = [
    "code", "bug", "error", "traceback", "laravel", "python",
    "javascript", "react", "php", "sql", "function", "class",
    "git", "terminal", "exception"
]

LONG_CONTEXT_KEYWORDS = [
    "analyze this project", "deep check", "summarize repo",
    "long document", "full file", "entire project", "large codebase"
]

FAST_KEYWORDS = [
    "quick", "short", "fast", "summarize", "what is", "define"
]


def detect_model_route(message: str):
    settings = load_model_settings()
    text = message.lower()

    if any(keyword in text for keyword in CODING_KEYWORDS):
        route = "coding"
        model = settings["coding_model"]
    elif any(keyword in text for keyword in LONG_CONTEXT_KEYWORDS):
        route = "long_context"
        model = settings["long_context_model"]
    elif any(keyword in text for keyword in FAST_KEYWORDS):
        route = "fast"
        model = settings["fast_model"]
    else:
        route = "general"
        model = settings["general_model"]

    return {
        "route": route,
        "model": model,
        "fallback_model": settings["fallback_model"],
        "settings": settings,
    }


def explain_model_route(message: str):
    decision = detect_model_route(message)

    return (
        f"Model route: {decision['route']}\n"
        f"Primary model: {decision['model']}\n"
        f"Fallback model: {decision['fallback_model']}"
    )

def get_model_with_fallback(message: str):
    decision = detect_model_route(message)

    return {
        "route": decision["route"],
        "primary_model": decision["model"],
        "fallback_model": decision["fallback_model"],
        "models_in_order": [
            decision["model"],
            decision["fallback_model"],
        ],
    }
