from tools.live_environment_tools import (
    get_live_location,
    get_live_weather,
    live_environment_help,
)


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

    if text in [
        "live location",
        "my location",
        "current location",
        "where am i",
        "where am i now",
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
    ]:
        return get_live_weather()

    return None