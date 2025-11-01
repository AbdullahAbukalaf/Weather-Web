<h1 align="center">🌤️ Weather Web (FastAPI)</h1>

<p align="center">
A fast, modern Python web app that fetches <b>current weather</b> and a <b>daily forecast (1–16 days)</b> using the free <a href="https://open-meteo.com/">Open-Meteo APIs</a> — no API key required.<br>
Built with <b>FastAPI</b>, <b>Jinja2</b>, <b>Bootstrap 5</b>, and <b>httpx</b>.
</p>

---

## ✨ Features

* 🔍 **Search by city** (geocoded via Open-Meteo Geocoding API)
* 🌡️ **Current conditions** (temperature, humidity, wind) + readable weather code → *text + emoji*
* 📅 **Daily forecast table** (min/max temperature, precipitation)
* ⚙️ **Choose Units** — metric (°C, m/s) or imperial (°F, mph)
* 📆 **Choose Days** — 1 to 16
* 🎨 **Responsive Bootstrap UI** with dark / light theme
* 💾 Public **JSON API** endpoint:
  `GET /api/weather?city=<name>&days=7&units=metric`

---

## 🧱 Tech Stack

| Layer       | Tool                    | Purpose                    |
| ----------- | ----------------------- | -------------------------- |
| Backend     | **FastAPI**             | Web framework & routing    |
| Templates   | **Jinja2**              | Server-side HTML rendering |
| HTTP Client | **httpx**               | Async API requests         |
| UI          | **Bootstrap 5 + Icons** | Styling & responsiveness   |
| Data        | **Open-Meteo**          | Geocoding + Weather data   |

---

## 📁 Project Structure

```
weather-web/
├─ app.py                     # FastAPI app & routes (HTML + JSON)
├─ utilities.py               # API helpers + WMO code mapping
├─ templates/
│  └─ index.html              # Main page (Bootstrap UI)
├─ static/
│  ├─ css/
│  │  └─ styles.css           # optional custom styles
│  └─ js/
│     └─ main.js              # optional UI scripts
└─ README.md
```

---

## 🚀 Quick Start

### 1️⃣ Create a virtual environment

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

> If blocked:
> `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 2️⃣ Install dependencies

```bash
pip install fastapi uvicorn[standard] httpx jinja2
```

---

### 3️⃣ Run the app

```bash
uvicorn app:app --reload
```

Then open 👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🖥️ Usage

### 🌐 Web UI

1. Enter a **city** (e.g. Amman, London, Tokyo).
2. Choose **Units** (metric / imperial) and **Days** (1–16).
3. Click **Search** to view current and forecast data.

### ⚡ JSON API

Public endpoint (no API key):

```
GET /api/weather?city=<name>&days=7&units=metric
```

#### Query parameters

| Name    | Type   | Default  | Description                   |
| ------- | ------ | -------- | ----------------------------- |
| `city`  | string | required | City name (e.g. Amman)        |
| `days`  | int    | 7        | Forecast length (1–16)        |
| `units` | string | metric   | Either `metric` or `imperial` |

#### Example

```bash
curl "http://127.0.0.1:8000/api/weather?city=Amman&days=3&units=metric"
```

#### Sample JSON response (trimmed)

```json
{
  "city": "Amman",
  "coords": { "name": "Amman", "country_code": "JO", "latitude": 31.9552, "longitude": 35.9450 },
  "units": "metric",
  "days": 3,
  "current": {
    "temp": 27.0,
    "humidity": 20,
    "wind": 2.6,
    "text": "Clear sky",
    "emoji": "☀️"
  },
  "daily": {
    "dates": ["2025-11-01","2025-11-02","2025-11-03"],
    "tmin": [17.5,18.6,18.8],
    "tmax": [27.5,28.4,28.9],
    "prec": [0.0,0.0,0.0],
    "text": ["Clear sky","Overcast","Partly cloudy"],
    "emoji": ["☀️","☁️","⛅"]
  }
}
```

---

## 🔧 How It Works

1. **Geocoding** → `utilities.get_city_coordinates()`
   Calls Open-Meteo Geocoding API to get `latitude` and `longitude`.
2. **Weather** → `utilities.get_weather()`
   Requests Open-Meteo Forecast API for current + daily data.
3. **Mapping** → `utilities.wmo_to_text_emoji()`
   Converts numeric `weather_code` to friendly text + emoji.
4. **Rendering** → `app.py` + Jinja2 template
   Combines everything into an elegant Bootstrap dashboard.

---

## ⚙️ Configuration

| Setting  | Default    | Range / Notes               |
| -------- | ---------- | --------------------------- |
| `days`   | `7`        | `1–16`                      |
| `units`  | `"metric"` | `"metric"` or `"imperial"`  |
| API Keys | ❌ none     | Open-Meteo is free & public |

---

## 🧪 Developer Tips

* Auto-reload is active with `--reload`.
* Docs UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* If VS Code shows `Import \"fastapi\" could not be resolved`:
  Press **Ctrl + Shift + P → “Python: Select Interpreter” →** pick `.venv`.

---

## 🐛 Troubleshooting

| Issue                          | Fix                                                   |
| ------------------------------ | ----------------------------------------------------- |
| `ModuleNotFoundError: fastapi` | Activate venv and reinstall: `pip install fastapi`    |
| PowerShell blocks activation   | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| “City not found”               | Check spelling or API outage                          |
| API timeout                    | Open-Meteo may be temporarily unreachable             |

---

## 🗺️ Roadmap

* ✅ WMO code → emoji mapping
* 🕓 Hourly forecast view
* 💾 Caching (API responses)
* 🌍 Arabic interface ( RTL )
* 📦 Dockerfile / Cloud deploy

---

## 📜 License

MIT — free for personal and commercial use.

---

<p align="center">
  <b>Developed with ❤️ by <a href="https://github.com/AbdullahAbukalaf">Abdullah Abukalaf</a></b><br>
  <sub>Built for learning and real-world FastAPI practice.</sub>
</p>
