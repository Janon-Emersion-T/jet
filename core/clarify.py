from core.brain import ask_brain


def ask_for_clarification(user_input: str, nlp, decision=None, chat_context: str | None = None) -> str:
    # Keep clarifying prompts short so they can be spoken and answered quickly.
    prompt = f"""
You are JARVIS. The NLP pipeline produced a low-confidence intent for the following user input.

User input:
{user_input}

NLP intent: {getattr(nlp, 'intent', 'unknown')}
NLP confidence: {getattr(nlp, 'confidence', 0.0)}
Routing decision confidence: {getattr(decision, 'confidence', 0.0) if decision else 'N/A'}

Produce one short, clear clarifying question (10-20 words) that will let the assistant resolve the user's intent. Do not include any extra explanation. Examples: "Do you want me to open the project file or run tests?"
"""

    try:
        question = ask_brain(prompt, route_hint="fast", max_tokens=80)
    except Exception:
        question = None

    # If the LLM failed or returned an error string, fall back to a safe concise question.
    if not question or (isinstance(question, str) and question.lower().startswith("brain error")):
        return "Can you clarify what you'd like me to do?"

    # Ensure it's concise even if model returns longer text.
    return question.strip()
