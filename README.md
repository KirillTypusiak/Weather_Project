# 🌤️ Weather App

> **EN** | [УКР](#укр)

---

## Table of Contents

- [Project Goal](#project-goal)
- [Team](#team)
- [Technologies & Modules](#technologies--modules)
- [How to Run](#how-to-run)
- [Project Overview](#project-overview)
- [Conclusion](#conclusion)

---

## Project Goal

This project was created as a practical exercise in building a real desktop application from scratch using Python. It is especially useful for beginners because it demonstrates how to:

- Structure a mid-size PyQt6 project with multiple modules
- Work with external REST APIs (OpenWeatherMap, Nominatim)
- Build a custom frameless window with a settings panel, modals, and signal/slot architecture
- Manage persistent state with QSettings
- Implement multi-language UI support without any third-party i18n library

---

## Team

| Role | Name | GitHub |
|------|------|--------|
| Team Lead / Lead Developer | Kyrylo Typusiak | [@KirillTypusiak](https://github.com/KirillTypusiak) |
| Developer | Maksym Gergel | [@MaksymGergel](https://github.com/MaksymGergel/-Weather_Project) |
| Developer | Yehor Voitov | *(link)* |

---

## Technologies & Modules

### External Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| PyQt6 | 6.11.0 | UI framework |
| PyQt6-WebEngine | 6.11.0 | Embedded map rendering |
| folium | 0.20.0 | Interactive map generation |
| requests | 2.34.2 | HTTP requests to APIs |
| python-dotenv | 1.2.2 | API key management via .env |

### APIs

| Service | Purpose |
|---------|---------|
| [OpenWeatherMap](https://openweathermap.org/api) | Current weather and 5-day forecast |
| [Nominatim (OpenStreetMap)](https://nominatim.org) | City/country search, geocoding, reverse geocoding |

### Project Modules

```
Weather Project/
├── main.py                      # Entry point
├── config.py                    # API key config
├── modules/
│   ├── app.py                   # QApplication instance
│   ├── window.py                # MainWindow — root layout, signal wiring
│   ├── header.py                # Custom title bar
│   ├── left_container.py        # City list panel with scroll area
│   ├── right_container.py       # Main weather view
│   ├── top_frame.py             # Search bar and settings button
│   ├── weather_content.py       # Individual city card in left panel
│   ├── modal.py                 # Settings modal with tab navigation
│   ├── modal_city_finder.py     # City search tab (country/city/coordinates + map)
│   ├── modal_language_change.py # Language selection tab
│   ├── Horizontal_bar_card.py   # Hourly forecast scroll widget
│   └── temperature_chart.py     # 12-hour temperature bar chart
├── utils/
│   ├── request.py               # OpenWeatherMap current weather
│   ├── request_forecast_2.py    # OpenWeatherMap 5-day forecast
│   ├── request_cities.py        # Nominatim city/country search + translation
│   └── translate.py             # TRANSLATIONS dict and language state
└── media/                       # Icons and SVG assets
```

---

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/KirillTypusiak/Weather_Project.git
cd Weather_Project
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

Get a free API key at [openweathermap.org](https://openweathermap.org/api).

### 4. Run

```bash
python main.py
```

---

## Project Overview

The app is split into two main panels:

**Left panel** — city list with real-time local time and current weather for each saved city. Cities are added via the Settings modal and persist between app launches.

**Right panel** — detailed weather view for the selected city: current temperature, weather condition, min/max, local clock, hourly forecast with sunrise/sunset cards, and a 12-hour temperature bar chart.

### Screenshots

![Main view](https://raw.githubusercontent.com/KirillTypusiak/Weather_Project/master/screenshot_main.png)

![Settings panel](https://raw.githubusercontent.com/KirillTypusiak/Weather_Project/master/screenshot_settings.png)

---

## Conclusion

Working on this project gave the team hands-on experience with:

- **PyQt6 signal/slot architecture** — managing communication between decoupled UI components without direct references
- **REST API integration** — fetching, parsing, and displaying live data from multiple sources
- **State management** — persisting user preferences and city lists across sessions using QSettings
- **Internationalization** — building a translation system from scratch without external libraries
- **Custom UI design** — frameless windows, gradient backgrounds, scroll areas, animated charts

### Future development ideas

- Add weather alerts and notifications
- Geolocation to auto-detect the user's city on launch
- Dark/light theme toggle
- Weather map overlay (precipitation, wind, temperature)
- Widget mode — a compact always-on-top window

---

---

<a name="укр"></a>

# 🌤️ Weather App

> [EN](#-weather-app) | **УКР**

---

## Зміст

- [Мета проєкту](#мета-проєкту)
- [Склад команди](#склад-команди)
- [Технології та модулі](#технології-та-модулі)
- [Як запустити](#як-запустити)
- [Зміст проєкту](#зміст-проєкту)
- [Висновок](#висновок)

---

## Мета проєкту

Цей проєкт створено як практичне завдання для побудови повноцінного десктопного застосунку на Python з нуля. Він буде особливо корисний початківцям, оскільки демонструє:

- Як структурувати середній PyQt6-проєкт із кількома модулями
- Як працювати із зовнішніми REST API (OpenWeatherMap, Nominatim)
- Як будувати кастомне вікно без рамки з модальними панелями налаштувань і архітектурою сигналів/слотів
- Як зберігати стан між запусками через QSettings
- Як реалізувати підтримку кількох мов у UI без сторонніх бібліотек

---

## Склад команди

| Роль | Ім'я | GitHub |
|------|------|--------|
| Тімлід / Головний розробник | Кирило Типусяк | [@KirillTypusiak](https://github.com/KirillTypusiak) |
| Розробник | Максим Гергель | [@MaksymGergel](https://github.com/MaksymGergel/-Weather_Project) |
| Розробник | Єгор Войтов | *(посилання)* |

---

## Технології та модулі

### Зовнішні бібліотеки

| Бібліотека | Версія | Призначення |
|------------|--------|-------------|
| PyQt6 | 6.11.0 | UI-фреймворк |
| PyQt6-WebEngine | 6.11.0 | Вбудований рендеринг карти |
| folium | 0.20.0 | Генерація інтерактивної карти |
| requests | 2.34.2 | HTTP-запити до API |
| python-dotenv | 1.2.2 | Зберігання API-ключа через .env |

### API

| Сервіс | Призначення |
|--------|-------------|
| [OpenWeatherMap](https://openweathermap.org/api) | Поточна погода та прогноз на 5 днів |
| [Nominatim (OpenStreetMap)](https://nominatim.org) | Пошук міст і країн, геокодування |

### Модулі проєкту

```
Weather Project/
├── main.py                      # Точка входу
├── config.py                    # Конфіг з API-ключем
├── modules/
│   ├── app.py                   # Екземпляр QApplication
│   ├── window.py                # MainWindow — розмітка, підключення сигналів
│   ├── header.py                # Кастомна панель заголовка
│   ├── left_container.py        # Панель зі списком міст
│   ├── right_container.py       # Головний вигляд погоди
│   ├── top_frame.py             # Рядок пошуку та кнопка налаштувань
│   ├── weather_content.py       # Картка міста в лівій панелі
│   ├── modal.py                 # Модальне вікно налаштувань з вкладками
│   ├── modal_city_finder.py     # Вкладка пошуку міста (країна/місто/координати + карта)
│   ├── modal_language_change.py # Вкладка вибору мови
│   ├── Horizontal_bar_card.py   # Погодинний прогноз зі скролом
│   └── temperature_chart.py     # Графік температури на 12 годин
├── utils/
│   ├── request.py               # Поточна погода з OpenWeatherMap
│   ├── request_forecast_2.py    # Прогноз на 5 днів
│   ├── request_cities.py        # Пошук міст і країн через Nominatim
│   └── translate.py             # Словник перекладів і стан мови
└── media/                       # Іконки та SVG-ресурси
```

---

## Як запустити

### 1. Клонуй репозиторій

```bash
git clone https://github.com/KirillTypusiak/Weather_Project.git
cd Weather_Project
```

### 2. Встанови залежності

```bash
pip install -r requirements.txt
```

### 3. Налаштуй API-ключ

Створи файл `.env` у корені проєкту:

```
API_KEY=твій_ключ_openweathermap
```

Безкоштовний ключ можна отримати на [openweathermap.org](https://openweathermap.org/api).

### 4. Запусти

```bash
python main.py
```

---

## Зміст проєкту

Застосунок поділено на дві головні панелі:

**Ліва панель** — список міст із реальним місцевим часом і поточною погодою для кожного збереженого міста. Міста додаються через модальне вікно налаштувань і зберігаються між запусками.

**Права панель** — детальний вигляд погоди для обраного міста: поточна температура, стан погоди, мін/макс, місцевий годинник, погодинний прогноз із картками сходу/заходу сонця та графік температури на 12 годин.

### Скріншоти

![Головний вигляд](https://raw.githubusercontent.com/KirillTypusiak/Weather_Project/master/screenshot_main.png)

![Панель налаштувань](https://raw.githubusercontent.com/KirillTypusiak/Weather_Project/master/screenshot_settings.png)

---

## Висновок

Робота над цим проєктом дала команді практичний досвід у:

- **Архітектурі сигналів/слотів PyQt6** — керування зв'язком між ізольованими UI-компонентами без прямих посилань
- **Інтеграції з REST API** — отримання, парсинг і відображення живих даних із кількох джерел
- **Управлінні станом** — збереження налаштувань і списку міст між сесіями через QSettings
- **Інтернаціоналізації** — побудова власної системи перекладів без зовнішніх бібліотек
- **Кастомному UI-дизайні** — вікна без рамок, градієнтні фони, скролабельні зони, анімовані графіки

### Ідеї для подальшого розвитку

- Погодні сповіщення та нотифікації
- Геолокація для автоматичного визначення міста при запуску
- Перемикання темної/світлої теми
- Накладення погодної карти (опади, вітер, температура)
- Режим віджета — компактне вікно поверх усіх вікон
