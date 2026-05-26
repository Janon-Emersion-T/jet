import json
import urllib.parse
import urllib.request
from datetime import datetime


def _get_json(url: str, timeout: int = 10):
    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "JARVIS-local-assistant/1.0"},
        )
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as error:
        return {"error": str(error)}


def get_live_location():
    data = _get_json("https://ipapi.co/json/")

    if data.get("error"):
        return f"""LIVE LOCATION

Unable to detect live location.

Reason:
{data.get("error")}

Try:
live weather in <city>

Note:
Location is estimated using public IP, not GPS."""

    return f"""LIVE LOCATION

Estimated location:
City: {data.get("city", "Unknown")}
Region: {data.get("region", "Unknown")}
Country: {data.get("country_name", "Unknown")}
Latitude: {data.get("latitude")}
Longitude: {data.get("longitude")}
Timezone: {data.get("timezone", "Unknown")}
Public IP: {data.get("ip", "Hidden")}

Accuracy note:
This is IP-based location, not GPS. VPN, proxy, ISP routing, or mobile data can make it inaccurate.

Safety:
Read-only lookup. No location was stored."""


def get_live_weather(city: str = ""):
    location = _geocode_city(city) if city.strip() else _detect_location_for_weather()

    if location.get("error"):
        return f"""LIVE WEATHER

Unable to detect weather.

Reason:
{location.get("error")}

Try:
live weather in Jaffna
weather in London
current weather in Tokyo"""

    latitude = location["latitude"]
    longitude = location["longitude"]
    place = location["place"]

    params = urllib.parse.urlencode({
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,weather_code,wind_speed_10m",
        "timezone": "auto",
    })

    weather = _get_json(f"https://api.open-meteo.com/v1/forecast?{params}")

    if weather.get("error"):
        return f"""LIVE WEATHER

Unable to fetch weather.

Reason:
{weather.get("error")}

Location:
{place}"""

    current = weather.get("current", {})
    units = weather.get("current_units", {})
    description = _weather_code_description(current.get("weather_code"))

    return f"""LIVE WEATHER

Location:
{place}

Current weather:
Temperature: {current.get("temperature_2m")} {units.get("temperature_2m", "°C")}
Feels like: {current.get("apparent_temperature")} {units.get("apparent_temperature", "°C")}
Humidity: {current.get("relative_humidity_2m")} {units.get("relative_humidity_2m", "%")}
Rain: {current.get("rain")} {units.get("rain", "mm")}
Precipitation: {current.get("precipitation")} {units.get("precipitation", "mm")}
Wind speed: {current.get("wind_speed_10m")} {units.get("wind_speed_10m", "km/h")}
Condition: {description}
Updated at: {current.get("time", datetime.now().isoformat(timespec="seconds"))}

Safety:
Read-only live weather lookup. No weather data was stored."""


def _detect_location_for_weather():
    data = _get_json("https://ipapi.co/json/")

    if data.get("error"):
        return {"error": data.get("error")}

    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if latitude is None or longitude is None:
        return {"error": "Could not detect latitude and longitude from IP location."}

    place_parts = [
        data.get("city"),
        data.get("region"),
        data.get("country_name"),
    ]

    return {
        "latitude": latitude,
        "longitude": longitude,
        "place": ", ".join([part for part in place_parts if part]),
    }


def _geocode_city(city: str):
    city = city.strip()

    if not city:
        return {"error": "City name is required."}

    query = urllib.parse.urlencode({
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json",
    })

    data = _get_json(f"https://geocoding-api.open-meteo.com/v1/search?{query}")

    if data.get("error"):
        return {"error": data.get("error")}

    results = data.get("results", [])

    if not results:
        return {"error": f"No location found for: {city}"}

    item = results[0]

    place_parts = [
        item.get("name"),
        item.get("admin1"),
        item.get("country"),
    ]

    return {
        "latitude": item.get("latitude"),
        "longitude": item.get("longitude"),
        "place": ", ".join([part for part in place_parts if part]),
    }


def _weather_code_description(code):
    codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }

    return codes.get(code, f"Unknown weather code: {code}")


def live_environment_help():
    return """LIVE ENVIRONMENT COMMANDS

live location
my location
current location
where am i

live weather
weather
current weather
today weather

live weather in <city>
weather in <city>
current weather in <city>
forecast in <city>

Examples:
live weather in Jaffna
weather in London
current weather in Tokyo
forecast in Colombo

Note:
Location is IP-based, not GPS."""