Weather Web (FastAPI)

A simple, fast Python web app that fetches current weather and a daily forecast (1–16 days) using the free Open-Meteo APIs—no API key required.
Built with FastAPI, Jinja2 templates, Bootstrap 5 UI, and httpx for HTTP calls.

✨ Features

Search by city (geocoded via Open-Meteo Geocoding API)

Current conditions (temp, humidity, wind) + human-readable weather code → text + emoji

Daily forecast table (min/max temperature, precipitation)

Choose Units (metric °C/m/s or imperial °F/mph)

Choose Days (1–16)

Server-rendered UI with Bootstrap (dark/light ready)

Public JSON endpoint: GET /api/weather?city=…

🧱 Tech Stack

FastAPI — web framework & routing

Jinja2 — HTML templating

httpx — async HTTP client

Bootstrap 5 + Bootstrap Icons — styling

Open-Meteo — geocoding + weather data (no key)

📁 Project Structure
weather-web/
├─ app.py                     # FastAPI app & routes (HTML + JSON)
├─ utilities.py               # API helpers + WMO code mapping
├─ templates/
│  └─ index.html              # Main page (Bootstrap UI)
├─ static/
│  ├─ css/
│  │  └─ styles.css           # (optional) your custom styles
│  └─ js/
│     └─ main.js              # (optional) UI scripts
└─ README.md

🚀 Quick Start
1) Create a virtual environment

Windows (PowerShell)

python -m venv .venv
.\.venv\Scripts\Activate.ps1


If you get a policy error:
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

macOS/Linux

python3 -m venv .venv
source .venv/bin/activate

2) Install dependencies
pip install fastapi uvicorn[standard] httpx jinja2

3) Run the app
uvicorn app:app --reload


Open your browser: http://127.0.0.1:8000

🖥️ Usage
Web UI

Enter a city (e.g., Amman, London, Tokyo).

Choose Units (metric/imperial) and Days (1–16).

Click Search to see current + forecast.

JSON API

Public endpoint your frontend/scripts can call:

GET /api/weather?city=<name>&days=7&units=metric


Query parameters

city (required, str) — city name (e.g., Amman)

days (optional, int) — 1–16 (default: 7)

units (optional, str) — metric or imperial (default: metric)

Example

curl "http://127.0.0.1:8000/api/weather?city=Amman&days=3&units=metric"


Sample response (truncated)

{
  "city": "Amman",
  "coords": { "name": "Amman", "country_code": "JO", "latitude": 31.95522, "longitude": 35.94503 },
  "units": "metric",
  "days": 3,
  "current": {
    "temp": 27.0,
    "humidity": 20,
    "wind": 2.6,
    "code": 0,
    "text": "Clear sky",
    "emoji": "☀️"
  },
  "daily": {
    "dates": ["2025-11-01", "2025-11-02", "2025-11-03"],
    "tmin":  [17.5, 18.6, 18.8],
    "tmax":  [27.5, 28.4, 28.9],
    "prec":  [0.0, 0.0, 0.0],
    "code":  [0, 3, 2],
    "text":  ["Clear sky", "Overcast", "Partly cloudy"],
    "emoji": ["☀️", "☁️", "⛅"]
  }
}

🔧 How it Works (High Level)

Geocoding (utilities.get_city_coordinates)
Calls:
https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json
→ returns latitude & longitude for the city.

Weather (utilities.get_weather)
Calls:
https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=...&daily=...&forecast_days={days}&temperature_unit=...&wind_speed_unit=...
→ returns current conditions + daily arrays.

WMO mapping (utilities.wmo_to_text_emoji)
Convert Open-Meteo weather_code numbers → readable text + emoji for better UX.

Rendering (app.py → Jinja2)
The /search route collects data and passes a clean context into templates/index.html.

⚙️ Configuration Notes

No API keys needed (Open-Meteo is free & public).

Defaults: units=metric, days=7.

Valid ranges enforced in FastAPI route:

days: int = Query(7, ge=1, le=16)

units: str = Query("metric", pattern="^(metric|imperial)$")

🧪 Dev Tips

Auto-reload is enabled with --reload (saves re-run automatically).

Interactive docs at: http://127.0.0.1:8000/docs

If VS Code shows “Import ‘fastapi’ could not be resolved”:

Press Ctrl+Shift+P → Python: Select Interpreter → pick the one with .venv.

🐛 Troubleshooting

ModuleNotFoundError: fastapi → ensure venv is active and pip show fastapi shows it installed inside .venv.

PowerShell cannot activate venv → run:

Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned


API errors → Open-Meteo may be temporarily unavailable. The app returns friendly messages for geocoding/weather failures.