# Weather App

A desktop weather application built with PyQt6, featuring a clean UI with city search, hourly forecasts, temperature charts, and multi-language support.

---

## Features

- Real-time weather data via OpenWeatherMap API
- City search with autocomplete powered by Nominatim (OpenStreetMap)
- Hourly forecast with weather icons and temperature chart
- Sunrise and sunset times
- Multi-city support — add and manage cities from the settings panel
- Interactive map showing city location (Folium + OpenStreetMap)
- UI language support: Ukrainian and English
- Persistent city list saved between sessions via QSettings
- Frameless custom window with header controls

---

## Project Structure

```
Weather Project/
├── main.py                        # Entry point
├── config.py                      # API key config
├── modules/
│   ├── app.py                     # QApplication instance
│   ├── window.py                  # MainWindow — root layout, signal wiring
│   ├── header.py                  # Custom title bar (close, minimize, maximize)
│   ├── left_container.py          # City list panel with scroll area
│   ├── right_container.py         # Main weather view (build_ui / build_empty_ui)
│   ├── top_frame.py               # Search bar and settings button
│   ├── weather_content.py         # Individual city card in left panel
│   ├── modal.py                   # Settings modal with tab navigation
│   ├── modal_city_finder.py       # City search tab (country/city/coordinates + map)
│   ├── modal_language_change.py   # Language selection tab
│   ├── Horizontal_bar_card.py     # Hourly forecast scroll widget with sun cards
│   └── temperature_chart.py       # 12-hour temperature bar chart
├── utils/
│   ├── __init__.py                # Re-exports all utils
│   ├── request.py                 # OpenWeatherMap current weather
│   ├── request_forecast_2.py      # OpenWeatherMap 5-day forecast
│   ├── request_cities.py          # Nominatim city/country search + translation helpers
│   ├── translate.py               # TRANSLATIONS dict, t() and tw() functions, language state
│   └── json_write.py              # JSON utility helpers
└── media/                         # Icons and SVG assets
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/weather-project.git
cd weather-project
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API key

Create a `.env` file in the project root:

```
API_KEY=your_openweathermap_api_key
```

Or set it directly in `config.py`.

### 4. Run

```bash
python main.py
```

---

## APIs Used

| Service | Purpose | Docs |
|---|---|---|
| OpenWeatherMap | Current weather and 5-day forecast | https://openweathermap.org/api |
| Nominatim (OpenStreetMap) | City/country search, geocoding, reverse geocoding | https://nominatim.org |
| Folium | Interactive map rendering | https://python-visualization.github.io/folium |

---

## Language Support

The app supports Ukrainian and English. Language is selected in Settings → App Language and persists between sessions. All UI strings are managed through `utils/translate.py` using a central `TRANSLATIONS` dictionary.