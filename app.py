from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from utilities import get_city_coordinates, get_weather, wmo_to_text_emoji

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "units": "metric", "days": 7}
    )


@app.get("/search", response_class=HTMLResponse)
async def search(
    request: Request,
    city: str | None = Query(None),
    days: int = Query(7, ge=1, le=16),
    units: str = Query("metric", pattern="^(metric|imperial)$"),
):
    if not city or len(city.strip()) < 2:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": "Please enter at least 2 characters.",
                "city": city or "",
                "units": units,
                "days": days,
            },
        )

    try:
        coords = await get_city_coordinates(city)
    except Exception:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": "Could not reach geocoding service.",
                "city": city,
                "units": units,
                "days": days,
            },
        )
    if not coords:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": f"City '{city}' not found.",
                "city": city,
                "units": units,
                "days": days,
            },
        )

    try:
        wx = await get_weather(coords["latitude"], coords["longitude"], days, units)
    except Exception:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": "Weather service is unavailable. Please try again.",
                "city": city,
                "units": units,
                "days": days,
            },
        )

    current = wx.get("current", {})
    daily = wx.get("daily", {})

    c_text, c_emoji = wmo_to_text_emoji(current.get("weather_code"))
    daily_codes = daily.get("weather_code", []) or []
    daily_text = []
    daily_emoji = []
    for code in daily_codes:
        t, emj = wmo_to_text_emoji(code)
        daily_text.append(t)
        daily_emoji.append(emj)

    ctx = {
        "city": city,
        "coords": coords,
        "units": units,
        "unit_temp": "°C" if units == "metric" else "°F",
        "unit_wind": "m/s" if units == "metric" else "mph",
        "current": {
            "temp": current.get("temperature_2m"),
            "humidity": current.get("relative_humidity_2m"),
            "wind": current.get("wind_speed_10m"),
        },
        "daily": {
            "dates": daily.get("time", []),
            "tmin": daily.get("temperature_2m_min", []),
            "tmax": daily.get("temperature_2m_max", []),
            "prec": daily.get("precipitation_sum", []),
        },
        "error": None,
    }

    # Finalize context with selections and human-readable weather
    ctx["days"] = days
    ctx["unit_temp"] = "°C" if units == "metric" else "°F"
    ctx["current"].update({
        "code": current.get("weather_code"),
        "text": c_text,
        "emoji": c_emoji,
    })
    ctx["daily"].update({
        "code": daily_codes,
        "text": daily_text,
        "emoji": daily_emoji,
    })
    ctx["unit_temp"] = "°C" if units == "metric" else "°F"

    return templates.TemplateResponse("index.html", {"request": request, **ctx})


@app.get("/api/weather")
async def api_weather(
    city: str,
    days: int = Query(7, ge=1, le=16),
    units: str = Query("metric", pattern="^(metric|imperial)$"),
):
    coords = await get_city_coordinates(city)
    if not coords:
        return JSONResponse({"error": f"City '{city}' not found."}, status_code=404)

    wx = await get_weather(coords["latitude"], coords["longitude"], days, units)
    current = wx.get("current", {})
    daily = wx.get("daily", {})

    c_text, c_emoji = wmo_to_text_emoji(current.get("weather_code"))
    daily_codes = daily.get("weather_code", []) or []
    daily_text = []
    daily_emoji = []
    for code in daily_codes:
        t, emj = wmo_to_text_emoji(code)
        daily_text.append(t)
        daily_emoji.append(emj)

    return {
        "city": city,
        "coords": coords,
        "units": units,
        "days": days,
        "current": {
            "temp": current.get("temperature_2m"),
            "humidity": current.get("relative_humidity_2m"),
            "wind": current.get("wind_speed_10m"),
            "code": current.get("weather_code"),
            "text": c_text,
            "emoji": c_emoji,
        },
        "daily": {
            "dates": daily.get("time", []),
            "tmin": daily.get("temperature_2m_min", []),
            "tmax": daily.get("temperature_2m_max", []),
            "prec": daily.get("precipitation_sum", []),
            "code": daily_codes,
            "text": daily_text,
            "emoji": daily_emoji,
        },
    }
