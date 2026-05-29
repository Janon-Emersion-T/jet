from tools.live_environment_tools import (
    get_live_location,
    get_live_weather,
    live_environment_help,
    set_saved_location,
)
from tools.environment_config import environment_status, save_environment_settings


def _extract_after_prefix(user_input: str, text: str, prefixes: list[str]) -> str:
    for prefix in prefixes:
        if text.startswith(prefix):
            return user_input[len(prefix):].strip()
    return ""


def handle_live_environment_routes(user_input: str, text: str, clean_text: str):
    weather_prefixes = [
        "live weather in ",
        "live whether in ",
        "weather in ",
        "whether in ",
        "current weather in ",
        "current whether in ",
        "today weather in ",
        "today whether in ",
        "forecast in ",
    ]

    if text in [
        "live environment help",
        "weather help",
        "whether help",
        "location help",
    ]:
        return live_environment_help()

    if text in ["environment status", "live environment status", "weather settings", "location settings"]:
        return environment_status()

    if text.startswith("set weather city "):
        city = user_input[len("set weather city "):].strip()
        if not city:
            return "A city is required. Example: set weather city Colombo"
        save_environment_settings({"default_weather_city": city})
        return f"Default weather city set to: {city}"

    if text in ["clear weather city", "use automatic weather location"]:
        save_environment_settings({"default_weather_city": ""})
        return "Default weather city cleared. Weather will use the configured location source."

    if text.startswith("set saved location "):
        return set_saved_location(user_input[len("set saved location "):].strip())

    if text in ["use ip location", "enable ip location"]:
        save_environment_settings({"use_ip_location": True})
        return "IP-based approximate location lookup enabled."

    if text in ["disable ip location", "do not use ip location"]:
        save_environment_settings({"use_ip_location": False})
        return "IP-based location lookup disabled. Saved locations can still be used."

    if text in [
        "live location",
        "my location",
        "current location",
        "where am i",
        "where am i now",
        "where do you think i am",
    ]:
        return get_live_location()

    if any(text.startswith(prefix) for prefix in weather_prefixes):
        city = _extract_after_prefix(user_input, text, weather_prefixes)
        return get_live_weather(city)

    if text in [
        "live weather",
        "live whether",
        "weather",
        "whether",
        "current weather",
        "current whether",
        "today weather",
        "today whether",
        "forecast",
        "what is the weather like",
        "whats the weather like",
        "how is the weather",
        "do i need an umbrella",
        "is it raining",
    ]:
        return get_live_weather()

    return None
