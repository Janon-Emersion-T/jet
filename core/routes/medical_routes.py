from core.ai_fallback import handle_ai_fallback


EMERGENCY_KEYWORDS = [
    "chest pain",
    "difficulty breathing",
    "shortness of breath",
    "severe bleeding",
    "unconscious",
    "stroke",
    "heart attack",
    "seizure",
    "suicide",
    "kill myself",
    "poison",
    "overdose",
    "severe allergic",
    "anaphylaxis",
    "blue lips",
    "cannot breathe",
    "worst headache",
]


def _is_emergency(text: str) -> bool:
    lowered = (text or "").lower()
    return any(keyword in lowered for keyword in EMERGENCY_KEYWORDS)


def handle_medical_routes(user_input: str, text: str, clean_text: str):
    lowered = (text or "").lower()

    medical_terms = [
        "medical",
        "health",
        "doctor",
        "symptom",
        "pain",
        "fever",
        "injury",
        "medicine",
        "treatment",
        "hospital",
        "clinic",
        "blood",
        "infection",
        "ankle",
        "fissure",
        "stomach",
        "headache",
        "cough",
        "rash",
        "wound",
        "swelling",
        "burning",
        "dizzy",
        "vomit",
        "diarrhea",
        "constipation",
    ]

    if not any(term in lowered for term in medical_terms):
        return None

    if _is_emergency(lowered):
        return (
            "This may be urgent. Please contact local emergency medical services or go to the nearest hospital now. "
            "Do not wait for an AI answer if breathing, consciousness, heavy bleeding, stroke-like symptoms, severe allergic reaction, "
            "poisoning, overdose, or severe chest pain is involved."
        )

    prompt = f"""
You are Christine, the medical guidance specialist inside Janon's private Jarvis system.

Important medical rules:
- Give general educational guidance only.
- Do not claim to diagnose.
- Do not prescribe restricted medication.
- Do not replace a licensed doctor.
- Explain possible common causes, warning signs, and practical next steps.
- Clearly tell the user when they should see a doctor.
- For emergency symptoms, advise urgent medical care.
- Keep the answer practical, calm, and direct.

User medical question:
{user_input}
"""

    return handle_ai_fallback(prompt)
