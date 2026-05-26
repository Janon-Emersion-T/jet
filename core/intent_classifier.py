from core.nlp_engine import classify_intent_nlp


def classify_intent(user_input: str) -> str:
    return classify_intent_nlp(user_input)

def classify_intent(user_input: str) -> str:
    text = user_input.lower().strip()

    live_weather_words = ["weather", "rain", "temperature", "forecast"]
    location_words = ["where am i", "my location", "which country", "current location"]
    camera_words = ["camera", "see me", "look around", "scan room"]
    email_words = ["email", "inbox", "send mail", "gmail"]
    calendar_words = ["calendar", "schedule", "meeting", "appointment"]
    browser_words = ["open google", "open website", "browser", "search google", "visit website", "open youtube"]
    search_words = ["search google for", "google search", "search for"]

    if any(word in text for word in live_weather_words):
        return "weather"

    if any(word in text for word in location_words):
        return "location"

    if any(word in text for word in camera_words):
        return "camera"

    if any(word in text for word in email_words):
        return "email"

    if any(word in text for word in calendar_words):
        return "calendar"

    if any(word in text for word in browser_words):
        return "browser_control"
    
    if any(word in text for word in search_words):
        return "google_search"

    return "general"
