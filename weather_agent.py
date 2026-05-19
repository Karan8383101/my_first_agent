import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def build_query_url(city: str, api_key: str, units: str = "metric") -> str:
    params = {
        "q": city,
        "appid": api_key,
        "units": units,
    }
    return f"{API_BASE_URL}?{urlencode(params)}"


def fetch_weather(city: str, api_key: str, units: str = "metric") -> dict:
    url = build_query_url(city, api_key, units)
    request = Request(url, headers={"User-Agent": "WeatherAgent/1.0"})
    try:
        with urlopen(request, timeout=10) as response:
            data = response.read().decode("utf-8")
            return json.loads(data)
    except HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(
            f"Weather API HTTP error {exc.code}: {exc.reason}\n{error_body}"
        )
    except URLError as exc:
        raise RuntimeError(f"Network error: {exc.reason}")


def format_weather(data: dict, units: str = "metric") -> str:
    if data.get("cod") != 200:
        message = data.get("message", "Unknown error")
        raise ValueError(f"API error: {message}")

    weather = data["weather"][0]
    details = data["main"]
    wind = data.get("wind", {})
    unit_temp = "°C" if units == "metric" else "°F"
    unit_speed = "m/s" if units == "metric" else "mph"

    return (
        f"Weather for {data['name']}, {data['sys'].get('country', '')}:\n"
        f"  Condition: {weather['main']} - {weather['description']}\n"
        f"  Temperature: {details['temp']}{unit_temp} (feels like {details['feels_like']}{unit_temp})\n"
        f"  Humidity: {details['humidity']}%\n"
        f"  Pressure: {details['pressure']} hPa\n"
        f"  Wind speed: {wind.get('speed', 'N/A')} {unit_speed}\n"
    )


def get_api_key() -> str:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if api_key:
        return api_key.strip()
    return input("Enter OpenWeatherMap API key: ").strip()


def print_help() -> None:
    print("Weather Agent")
    print("Enter a city name to get current weather.")
    print("Examples: London, New York, Tokyo")
    print("Type 'exit' or 'quit' to stop.")
    print("Set OPENWEATHER_API_KEY in your environment for faster startup.")


def main() -> None:
    api_key = get_api_key()
    if not api_key:
        print("API key is required to query OpenWeatherMap.")
        return

    units = "metric"
    choice = input("Use Fahrenheit? (y/N): ").strip().lower()
    if choice == "y":
        units = "imperial"

    print_help()
    while True:
        city = input("city> ").strip()
        if not city:
            continue
        if city.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        try:
            weather_data = fetch_weather(city, api_key, units)
            print(format_weather(weather_data, units))
        except Exception as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
