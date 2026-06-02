from core.brain import ask_brain


def handle_conversational_fallback(user_input: str, chat_context: str | None = None) -> str:
    prompt = f"""
You are JARVIS, Janon's private local AI assistant. Speak naturally and helpfully like a modern conversational assistant.

Current chat context:
{chat_context if chat_context else 'No active chat context provided.'}

Rules:
- Answer concisely but thoroughly.
- If this is a follow-up (yes/no/continue), infer meaning from the chat context.
- If the user asked for an action requiring external tools and those tools are not connected, respond: "That tool is not connected yet."
- Never invent external data or pretend to have access to services that are not connected.

User request:
{user_input}
"""

    try:
        reply = ask_brain(
            prompt,
            route_hint="general",
            max_tokens=700,
        )
    except Exception:
        reply = None

    if not reply or (isinstance(reply, str) and reply.lower().startswith("brain error")):
        # Safe generic fallback when LLM is unavailable
        return "I couldn't access the local model. Can you rephrase or try a simpler request?"

    return reply
