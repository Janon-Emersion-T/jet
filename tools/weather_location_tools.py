import json
import re
from pathlib import Path
from typing import Optional

import requests


BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
LOCATION_FILE = STORAGE_DIR / "current_location.json"

OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
OPEN_METEO_GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


WEATHER_CODE_MAP = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def _ensure_storage():
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)


def save_current_location(
    latitude: float,
    longitude: float,
    accuracy: Optional[float] = None,
    source: str = "browser",
):
    _ensure_storage()

    payload = {
        "latitude": latitude,
        "longitude": longitude,
        "accuracy": accuracy,
        "source": source,
    }

    LOCATION_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    return {
        "ok": True,
        "message": "Location saved successfully.",
        "location": payload,
    }


def get_saved_location():
    if not LOCATION_FILE.exists():
        return None

    try:
        return json.loads(LOCATION_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None


def format_saved_location():
    location = get_saved_location()

    if not location:
        return (
            "Location is not connected yet. "
            "Please allow location access from the Jarvis desktop app first, "
            "or use approximate IP-based location detection."
        )

    latitude = location.get("latitude")
    longitude = location.get("longitude")
    accuracy = location.get("accuracy")
    source = location.get("source", "unknown")

    city = location.get("city")
    region = location.get("region")
    country = location.get("country")

    place_parts = [city, region, country]
    place = ", ".join([part for part in place_parts if part])

    place_text = ""
    if place:
        place_text = f"\nApproximate place: {place}"

    accuracy_text = ""
    if accuracy is not None:
        accuracy_text = f"\nAccuracy: approximately {round(float(accuracy))} meters"

    if source == "ip":
        accuracy_text = "\nAccuracy: approximate only, based on public IP address"

    return (
        "Your saved location is:\n"
        f"Latitude: {latitude}\n"
        f"Longitude: {longitude}"
        f"{place_text}"
        f"{accuracy_text}\n"
        f"Source: {source}"
    )


def geocode_city(city_name: str):
    city_name = (city_name or "").strip()

    if not city_name:
        return None

    try:
        response = requests.get(
            OPEN_METEO_GEOCODING_URL,
            params={
                "name": city_name,
                "count": 1,
                "language": "en",
                "format": "json",
            },
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()
    except Exception:
        return None

    results = data.get("results") or []

    if not results:
        return None

    result = results[0]

    return {
        "name": result.get("name"),
        "country": result.get("country"),
        "admin1": result.get("admin1"),
        "latitude": result.get("latitude"),
        "longitude": result.get("longitude"),
        "timezone": result.get("timezone") or "auto",
    }


def fetch_weather(latitude: float, longitude: float, timezone: str = "auto"):
    try:
        response = requests.get(
            OPEN_METEO_FORECAST_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": ",".join(
                    [
                        "temperature_2m",
                        "relative_humidity_2m",
                        "apparent_temperature",
                        "precipitation",
                        "weather_code",
                        "cloud_cover",
                        "wind_speed_10m",
                        "wind_direction_10m",
                    ]
                ),
                "daily": ",".join(
                    [
                        "temperature_2m_max",
                        "temperature_2m_min",
                        "precipitation_sum",
                        "precipitation_probability_max",
                    ]
                ),
                "forecast_days": 1,
                "timezone": timezone,
            },
            timeout=20,
        )
        response.raise_for_status()
        return response.json()
    except Exception as error:
        return {"error": str(error)}


def format_weather_report(weather_data: dict, location_label: str = "your location"):
    if not weather_data or weather_data.get("error"):
        return (
            "Weather service is reachable only when internet is available. "
            f"Error: {weather_data.get('error', 'Unable to fetch weather data.')}"
        )

    current = weather_data.get("current") or {}
    current_units = weather_data.get("current_units") or {}
    daily = weather_data.get("daily") or {}
    daily_units = weather_data.get("daily_units") or {}

    weather_code = current.get("weather_code")
    condition = WEATHER_CODE_MAP.get(weather_code, "Unknown condition")

    temp = current.get("temperature_2m")
    apparent = current.get("apparent_temperature")
    humidity = current.get("relative_humidity_2m")
    precipitation = current.get("precipitation")
    cloud_cover = current.get("cloud_cover")
    wind_speed = current.get("wind_speed_10m")
    wind_direction = current.get("wind_direction_10m")

    max_temp = _first(daily.get("temperature_2m_max"))
    min_temp = _first(daily.get("temperature_2m_min"))
    rain_sum = _first(daily.get("precipitation_sum"))
    rain_probability = _first(daily.get("precipitation_probability_max"))

    return (
        f"Weather for {location_label}:\n"
        f"Condition: {condition}\n"
        f"Temperature: {temp} {current_units.get('temperature_2m', '°C')}\n"
        f"Feels like: {apparent} {current_units.get('apparent_temperature', '°C')}\n"
        f"Humidity: {humidity} {current_units.get('relative_humidity_2m', '%')}\n"
        f"Cloud cover: {cloud_cover} {current_units.get('cloud_cover', '%')}\n"
        f"Precipitation now: {precipitation} {current_units.get('precipitation', 'mm')}\n"
        f"Wind: {wind_speed} {current_units.get('wind_speed_10m', 'km/h')} "
        f"from {wind_direction}°\n"
        f"Today high/low: {max_temp} / {min_temp} {daily_units.get('temperature_2m_max', '°C')}\n"
        f"Rain today: {rain_sum} {daily_units.get('precipitation_sum', 'mm')}\n"
        f"Rain chance today: {rain_probability} {daily_units.get('precipitation_probability_max', '%')}"
    )


def _first(value):
    if isinstance(value, list) and value:
        return value[0]
    return value


def get_weather_for_saved_location():
    location = get_saved_location()

    if not location:
        return (
            "Location is not connected yet. "
            "Please allow location access first, then ask for the weather again."
        )

    latitude = location.get("latitude")
    longitude = location.get("longitude")

    if latitude is None or longitude is None:
        return "Saved location is invalid. Please allow location access again."

    weather_data = fetch_weather(latitude, longitude, "auto")
    return format_weather_report(weather_data, "your current location")


def get_weather_for_city(city_name: str):
    city = geocode_city(city_name)

    if not city:
        return f"I could not find a location named '{city_name}'. Try a clearer city name."

    weather_data = fetch_weather(
        city["latitude"],
        city["longitude"],
        city.get("timezone") or "auto",
    )

    label_parts = [
        city.get("name"),
        city.get("admin1"),
        city.get("country"),
    ]
    label = ", ".join([part for part in label_parts if part])

    return format_weather_report(weather_data, label)


def extract_weather_city(clean_text: str):
    patterns = [
        r"^weather in (.+)$",
        r"^weather at (.+)$",
        r"^weather for (.+)$",
        r"^what is the weather in (.+)$",
        r"^what's the weather in (.+)$",
        r"^check weather in (.+)$",
        r"^check the weather in (.+)$",
    ]

    for pattern in patterns:
        match = re.match(pattern, clean_text)
        if match:
            return match.group(1).strip()

    return None
def detect_location_by_ip():
    """
    Free approximate location fallback using public IP.

    This is less accurate than browser GPS/location permission,
    but it works when Electron/browser geolocation is blocked.
    """

    try:
        response = requests.get(
            "http://ip-api.com/json/",
            params={
                "fields": "status,message,country,regionName,city,lat,lon,query,timezone"
            },
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()
    except Exception as error:
        return {
            "ok": False,
            "message": f"IP location detection failed: {error}",
        }

    if data.get("status") != "success":
        return {
            "ok": False,
            "message": data.get("message", "IP location detection failed."),
        }

    latitude = data.get("lat")
    longitude = data.get("lon")

    if latitude is None or longitude is None:
        return {
            "ok": False,
            "message": "IP location service did not return coordinates.",
        }

    saved = save_current_location(
        latitude=latitude,
        longitude=longitude,
        accuracy=None,
        source="ip",
    )

    saved["location"]["city"] = data.get("city")
    saved["location"]["region"] = data.get("regionName")
    saved["location"]["country"] = data.get("country")
    saved["location"]["ip"] = data.get("query")
    saved["location"]["timezone"] = data.get("timezone")

    LOCATION_FILE.write_text(
        json.dumps(saved["location"], indent=2),
        encoding="utf-8",
    )

    return {
        "ok": True,
        "message": "Approximate location detected using IP address.",
        "location": saved["location"],
    }
