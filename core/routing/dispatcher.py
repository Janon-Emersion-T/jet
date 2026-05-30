from core.routing.route_registry import get_route_modules
from core.routing.nlp_route_selector import select_route


def dispatch_to_module(user_input: str, nlp):
    modules = get_route_modules()
    decision = select_route(user_input, nlp, modules)

    if decision.module is None:
        return None, decision

    text = getattr(nlp, "normalized_text", user_input)
    clean_text = getattr(nlp, "canonical_command", None) or getattr(nlp, "clean_text", user_input)
    intent = getattr(nlp, "intent", "")

    handler = decision.module.handler

    if decision.module.requires_intent_arg:
        response = handler(user_input, text, clean_text, intent)
    else:
        response = handler(user_input, text, clean_text)

    if response is not None:
        return response, decision

    # Important:
    # If the route selector confidently selected a specialist module,
    # do not silently fall back and hallucinate a generic answer.
    if decision.confidence >= 0.45:
        return (
            f"ROUTE SELECTED BUT ACTION NOT HANDLED\n"
            f"Selected module: {decision.module.name}\n"
            f"Routing confidence: {decision.confidence:.2f}\n"
            f"Reason: {decision.reason}\n\n"
            f"The correct module was selected, but that module does not yet support this natural-language action.\n"
            f"Add an action resolver inside the module instead of letting fallback guess.",
            decision,
        )

    return None, decision