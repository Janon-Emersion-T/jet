from core.nlp_engine import classify_intent_nlp


def classify_intent(user_input: str) -> str:
    return classify_intent_nlp(user_input)