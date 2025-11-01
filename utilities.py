import httpx


async def get_city_coordinates(city: str):
    url = (
        "https://geocoding-api.open-meteo.com/v1/search"
        f"?name={city}&count=1&language=en&format=json"
    )
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()

    if not data or "results" not in data or not data["results"]:
        return None

    top = data["results"][0]
    return {
        "name": top.get("name"),
        "country_code": top.get("country_code"),
        "latitude": top.get("latitude"),
        "longitude": top.get("longitude"),
    }


async def get_weather(lang: float, long: float, days: int = 7, units: str = "metric"):
    days = max(1, min(days, 16))
    temp_unit = "celsius" if units == "metric" else "fahrenheit"
    wind_unit = "ms" if units == "metric" else "mph"

    url= ( "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lang}&longitude={long}"
        f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
        f"&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum"
        f"&temperature_unit={temp_unit}&wind_speed_unit={wind_unit}"
        f"&precipitation_unit=mm&timezone=auto&forecast_days={days}")
    
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()

    return data


# WMO weather codes to human text and emoji
_WMO_MAP = {
    0: ("Clear sky", "☀️"),
    1: ("Mainly clear", "🌤️"),
    2: ("Partly cloudy", "⛅"),
    3: ("Overcast", "☁️"),
    45: ("Fog", "🌫️"),
    48: ("Depositing rime fog", "🌫️"),
    51: ("Light drizzle", "🌦️"),
    53: ("Moderate drizzle", "🌦️"),
    55: ("Dense drizzle", "🌧️"),
    56: ("Light freezing drizzle", "🌧️"),
    57: ("Dense freezing drizzle", "🌧️"),
    61: ("Slight rain", "🌦️"),
    63: ("Moderate rain", "🌧️"),
    65: ("Heavy rain", "🌧️"),
    66: ("Light freezing rain", "🌧️"),
    67: ("Heavy freezing rain", "🌧️"),
    71: ("Slight snow fall", "🌨️"),
    73: ("Moderate snow fall", "🌨️"),
    75: ("Heavy snow fall", "❄️"),
    77: ("Snow grains", "🌨️"),
    80: ("Slight rain showers", "🌦️"),
    81: ("Moderate rain showers", "🌦️"),
    82: ("Violent rain showers", "🌧️"),
    85: ("Slight snow showers", "🌨️"),
    86: ("Heavy snow showers", "❄️"),
    95: ("Thunderstorm", "⛈️"),
    96: ("Thunderstorm with slight hail", "⛈️"),
    99: ("Thunderstorm with heavy hail", "⛈️"),
}


def wmo_to_text_emoji(code: int | None) -> tuple[str, str]:
    if code is None:
        return ("Unknown", "❓")
    return _WMO_MAP.get(int(code), ("Unknown", "❓"))
