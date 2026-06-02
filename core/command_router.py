import re

from core.nlp.unified_orchestrator import orchestrate_command
from core.routing.dispatcher import dispatch_to_module
from core.routes.nlp_test_routes import handle_nlp_test_routes
from core.conversational import handle_conversational_fallback
from core.assistant_intent import plan_assistant_action
from core.clarify import ask_for_clarification
from core.system_modes import get_system_mode_state


def _strip_delegation_wrappers(raw_text: str) -> str:
    text = (raw_text or "").strip()
    if not text:
        return text

    lowered = text.lower().strip()
    patterns = [
        r"^(?:can you|could you)\s+(?:ask|tell)\s+[^ ]+(?:\s+and\s+[^ ]+)*\s+to\s+",
        r"^(?:can you|could you)\s+ask\s+the\s+website'?s\s+developer\s+to\s+",
        r"^(?:tony|peter|natasha|shuri|rocket)(?:\s+and\s+(?:tony|peter|natasha|shuri|rocket))*\s+can\s+you(?:\s+guys)?\s+",
        r"^(?:tony|peter|natasha|shuri|rocket)(?:,?\s*(?:and)?\s*(?:tony|peter|natasha|shuri|rocket))*[:,]?\s*",
    ]

    rewritten = lowered
    for pattern in patterns:
        rewritten = re.sub(pattern, "", rewritten, flags=re.I).strip()

    return rewritten or lowered


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

def route_command(
    user_input: str,
    chat_context: str | None = None,
    allow_clarify: bool = True,
    allow_assistant_plan: bool = True,
) -> str:
    raw_text = _strip_delegation_wrappers(user_input)

    if not raw_text:
        return "Please enter a command."
    
    external_guard_response = _guard_unconnected_external_tools(raw_text)
    if external_guard_response:
        return external_guard_response

    lower_text = raw_text.lower().strip()
    if lower_text in [
        "activate voice mode",
        "start voice mode",
        "voice mode",
        "activate offline voice mode",
    ]:
        from core.system_modes import set_voice_mode
        from voice.offline_voice_mode import start_offline_voice_mode

        set_voice_mode(True)
        try:
            start_offline_voice_mode()
        finally:
            set_voice_mode(False)

        return "Offline voice mode was activated and has now ended."

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

    if allow_assistant_plan:
        plan = plan_assistant_action(user_input, chat_context)

        if (
            plan.mode == "command"
            and plan.command
            and plan.confidence >= 0.55
            and plan.command.lower() != raw_text.lower()
        ):
            return route_command(
                plan.command,
                chat_context=chat_context,
                allow_clarify=allow_clarify,
                allow_assistant_plan=False,
            )

        if plan.mode in {"answer", "clarify"} and plan.answer and plan.confidence >= 0.55:
            return plan.answer

    # If both NLP and routing are low-confidence, try clarification first (if allowed).
    try:
        state = get_system_mode_state()
    except Exception:
        state = {"voice_mode": False}

    voice_mode_active = bool(state.get("voice_mode"))

    if nlp_confidence < 0.35 and route_confidence < 0.35:
        if allow_clarify:
            question = ask_for_clarification(user_input, nlp, decision, chat_context)

            if voice_mode_active:
                try:
                    from voice.text_to_speech import speak
                    from voice.speech_to_text import listen

                    speak(question)
                    follow = listen()
                    if follow:
                        combined = f"{user_input} CLARIFY: {follow}"
                        return route_command(
                            combined,
                            chat_context,
                            allow_clarify=False,
                            allow_assistant_plan=allow_assistant_plan,
                        )
                    else:
                        return question
                except Exception:
                    return question
            else:
                return question

    # If clarification not enabled or already attempted, fall back to conversational LLM.
    if nlp_confidence < 0.35 and route_confidence < 0.35:
        return handle_conversational_fallback(
            _format_low_confidence_fallback(user_input, nlp, decision, chat_context),
            chat_context=chat_context,
        )

    return handle_conversational_fallback(user_input, chat_context=chat_context)
