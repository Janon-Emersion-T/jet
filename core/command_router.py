from core.ai_fallback import handle_ai_fallback
from core.nlp.unified_orchestrator import orchestrate_command
from core.routing.dispatcher import dispatch_to_module
from core.routes.nlp_test_routes import handle_nlp_test_routes


def _format_blocked_response(nlp) -> str:
    lines = ["COMMAND BLOCKED"]
    lines.extend(f"- {reason}" for reason in nlp.safety.reasons)
    lines.extend(f"- Safe alternative: {alternative}" for alternative in nlp.safety.alternatives)
    return "\n".join(lines)


def _format_low_confidence_fallback(user_input: str, nlp, decision=None, chat_context: str | None = None) -> str:
    intent = getattr(nlp, "intent", "")
    clean_text = getattr(nlp, "canonical_command", None) or getattr(nlp, "clean_text", "")

    routing_note = ""

    if decision is not None:
        routing_note = f"""

Routing confidence:
{decision.confidence}

Routing reason:
{decision.reason}
"""

    return f"""The user entered a low-confidence natural language command.

Current chat context:
{chat_context if chat_context else "No active chat context provided."}

Original command:
{user_input}

Detected intent:
{intent}

Clean routing text:
{clean_text}
{routing_note}

Please respond naturally. If this is a follow-up like yes, no, continue, explain more, or do it, infer the meaning from the current chat context."""

def _guard_unconnected_external_tools(raw_text: str) -> str | None:
    text = " ".join((raw_text or "").lower().strip().split())

    blocked_terms = {
        "calendar",
        "calender",
        "my calendar",
        "my calender",
        "schedule",
        "my schedule",
        "today schedule",
        "email",
        "gmail",
        "inbox",
        "my email",
        "my mail",
    }

    if text in blocked_terms:
        if "calendar" in text or "calender" in text or "schedule" in text:
            return (
                "Calendar access is not connected yet. "
                "I cannot read your real calendar until a calendar connector is added. "
                "I will not invent events."
            )

        if "email" in text or "gmail" in text or "mail" in text or "inbox" in text:
            return (
                "Email access is not connected yet. "
                "I cannot read your real email until an email connector is added. "
                "I will not invent email content."
            )

    return None

def route_command(user_input: str, chat_context: str | None = None) -> str:
    raw_text = (user_input or "").strip()

    if not raw_text:
        return "Please enter a command."
    
    external_guard_response = _guard_unconnected_external_tools(raw_text)
    if external_guard_response:
        return external_guard_response

    # Everything passes through NLP first.
    nlp = orchestrate_command(user_input)

    # Safety must run before any module action.
    if nlp.safety.safety_level == "dangerous" and not nlp.safety.allowed:
        return _format_blocked_response(nlp)

    # Diagnostics can still be handled, but after NLP has processed the input.
    diagnostic_response = handle_nlp_test_routes(
        user_input,
        getattr(nlp, "normalized_text", user_input),
        getattr(nlp, "canonical_command", None) or getattr(nlp, "clean_text", user_input),
    )

    if diagnostic_response is not None:
        return diagnostic_response
    
    if raw_text.lower().startswith("debug route "):
        from core.routes.route_debug_routes import debug_route_command
        query = raw_text[12:].strip()
        return debug_route_command(query)

    # NLP-driven modular dispatcher.
    response, decision = dispatch_to_module(user_input, nlp)

    if response is not None:
        return response

    nlp_confidence = getattr(nlp, "confidence", 0.0)
    route_confidence = decision.confidence if decision else 0.0

    if nlp_confidence < 0.35 and route_confidence < 0.35:
        return handle_ai_fallback(
            _format_low_confidence_fallback(user_input, nlp, decision, chat_context),
            chat_context=chat_context,
        )

    return handle_ai_fallback(user_input, chat_context=chat_context)