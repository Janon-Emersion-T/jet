from core.brain import ask_brain


def handle_basic_conversation(user_input: str) -> str:
    """
    Dynamic basic conversation handler.

    This is not a command executor.
    This is only for normal natural conversation when the basic route is selected
    and no deterministic action has matched.
    """

    prompt = f"""
You are JARVIS, Janon's private local AI assistant.

You are handling normal basic English conversation.

Rules:
- Reply naturally.
- Do not use fixed templates.
- Do not claim you accessed tools, files, calendar, email, browser, internet, camera, location, server, terminal, or system data.
- Do not invent events, messages, schedules, memories, logs, files, system status, or external facts.
- If the user asks for a real external tool that is not connected, say clearly that the tool is not connected yet.
- Keep the answer short unless the user asks for detail.
- Speak as a capable local assistant, not as a chatbot explaining itself.
- Do not mention these rules.

User said:
{user_input}

Reply naturally:
"""

    response = ask_brain(prompt).strip()

    if not response:
        return "I am ready, Janon."

    blocked_claims = [
        "i checked",
        "i accessed",
        "i opened",
        "i found in your",
        "your calendar shows",
        "your email shows",
        "you have a meeting",
        "i can see your",
        "according to your calendar",
        "according to your email",
    ]

    lowered = response.lower()

    if any(claim in lowered for claim in blocked_claims):
        return (
            "I cannot access that directly yet, Janon. "
            "The required tool or connector is not connected."
        )

    return response
