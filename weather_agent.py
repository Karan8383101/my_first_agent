import argparse
import json
from urllib.parse import urlencode
from urllib.request import urlopen
from typing import Tuple


def get_coordinates(city: str):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    data = json.loads(urlopen(geo_url).read().decode())

    if "results" not in data:
        raise ValueError("City not found")

    result = data["results"][0]
    return result["latitude"], result["longitude"], result["name"]


def fetch_weather(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True
    }

    url = "https://api.open-meteo.com/v1/forecast?" + urlencode(params)
    data = json.loads(urlopen(url).read().decode())

    return data["current_weather"]


def c_to_f(c: float) -> float:
    return c * 9.0 / 5.0 + 32.0


def kmh_to_mph(kmh: float) -> float:
    return kmh * 0.621371


def format_weather_output(name: str, weather: dict, units: str = "metric", pretty: bool = False) -> str:
    temp = weather["temperature"]
    wind = weather["windspeed"]

    if units == "imperial":
        temp = c_to_f(temp)
        wind = kmh_to_mph(wind)

    temp_unit = "C" if units == "metric" else "F"
    wind_unit = "km/h" if units == "metric" else "mph"

    if pretty:
        lines = [f"Weather for {name}:"]
        lines.append(f"- Temperature: {temp:.1f} {temp_unit}")
        lines.append(f"- Windspeed: {wind:.1f} {wind_unit}")
        # include additional fields if available
        if "winddirection" in weather:
            lines.append(f"- Wind direction: {int(weather['winddirection'])} deg")
        if "is_day" in weather:
            lines.append(f"- Daytime: {'Yes' if weather['is_day'] == 1 else 'No'}")
        return "\n".join(lines) + "\n"

    # compact output
    return (
        f"Weather for {name}:\n"
        f"  Temperature: {temp} {temp_unit}\n"
        f"  Windspeed: {wind} {wind_unit}\n"
    )


def main():
    print("🌤 Weather Agent (NO API KEY REQUIRED)")

    parser = argparse.ArgumentParser(description="Weather Agent (Open-Meteo, no API key required)")
    parser.add_argument("--city", help="City name to query (non-interactive)")
    parser.add_argument("--units", choices=["metric", "imperial"], default="metric", help="Units: metric (C, km/h) or imperial (F, mph)")
    parser.add_argument("--pretty", action="store_true", help="Pretty-format the output")
    args, remaining = parser.parse_known_args()

    # Non-interactive single-city mode
    if args.city:
        try:
            lat, lon, name = get_coordinates(args.city)
            weather = fetch_weather(lat, lon)
            print(format_weather_output(name, weather, units=args.units, pretty=args.pretty))
        except Exception as e:
            print("Error:", e)
        return

    # Interactive mode
    while True:
        city = input("city> ").strip()

        if city.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        try:
            lat, lon, name = get_coordinates(city)
            weather = fetch_weather(lat, lon)
            print(format_weather_output(name, weather, units=args.units, pretty=args.pretty))

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()