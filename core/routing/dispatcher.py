from core.routing.route_registry import get_route_modules
from core.routing.nlp_route_selector import select_route
from core.agents.agent_registry import resolve_agent, format_agent_response

MIN_MODULE_CONFIDENCE = 0.60
FORCED_MODULE_ERROR_CONFIDENCE = 0.80


def dispatch_to_module(user_input: str, nlp):
    modules = get_route_modules()
    decision = select_route(user_input, nlp, modules)

    if decision.module is None or decision.confidence < MIN_MODULE_CONFIDENCE:
        return None, decision

    text = getattr(nlp, "normalized_text", user_input)
    clean_text = getattr(nlp, "canonical_command", None) or getattr(nlp, "clean_text", user_input)
    intent = getattr(nlp, "intent", "")
    domain = getattr(getattr(nlp, "domain", None), "domain", "")

    selected_agent = resolve_agent(
        route_name=decision.module.name,
        domain=domain,
        intent=intent,
        text=user_input,
    )

    decision.metadata["agent_key"] = selected_agent.key
    decision.metadata["agent_name"] = selected_agent.name
    decision.metadata["agent_title"] = selected_agent.title
    decision.metadata["agent_department"] = selected_agent.department

    handler = decision.module.handler

    if decision.module.requires_intent_arg:
        response = handler(user_input, text, clean_text, intent)
    else:
        response = handler(user_input, text, clean_text)

    if response is not None:
        return format_agent_response(selected_agent, response), decision

    # If the selected module did not actually handle the request, allow
    # the conversational fallback to answer unless the route was extremely strong.
    if decision.confidence >= FORCED_MODULE_ERROR_CONFIDENCE:
        return (
            f"[{selected_agent.name} | {selected_agent.title}]\n"
            f"ROUTE SELECTED BUT ACTION NOT HANDLED\n"
            f"Selected module: {decision.module.name}\n"
            f"Selected agent: {selected_agent.name}\n"
            f"Routing confidence: {decision.confidence:.2f}\n"
            f"Reason: {decision.reason}\n\n"
            f"The correct module was selected, but that module does not yet support this natural-language action.\n"
            f"Add an action resolver inside the module instead of letting fallback guess.",
            decision,
        )

    return None, decision
