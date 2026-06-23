from PyQt6.QtCore import QSettings

TRANSLATIONS = {
    "modal": {
        "uk": {
            "settings_title": "Налаштування",
            "tab_search": "Пошук міста",
            "tab_size": "Розмір додатку",
            "tab_language": "Мова додатку",
            "tab_images": "Списки зображень",
            "tab_size_wip": "Розмір додатку — в розробці",
            "tab_images_wip": "Списки зображень — в розробці",
        },
        "en": {
            "settings_title": "Settings",
            "tab_search": "City search",
            "tab_size": "App size",
            "tab_language": "App language",
            "tab_images": "Image lists",
            "tab_size_wip": "App size — in development",
            "tab_images_wip": "Image lists — in development",
        }
    },
    "modal_city_finder": {
        "uk": {
            "search_city_title": "Пошук міста",
            "country": "Країна",
            "select_country": "Виберіть країну",
            "city": "Місто",
            "select_city": "Виберіть місто",
            "coordinates": "Координати",
            "save": "Зберегти",
            "added_cities": "Додані міста",
        },
        "en": {
            "search_city_title": "City search",
            "country": "Country",
            "select_country": "Select country",
            "city": "City",
            "select_city": "Select city",
            "coordinates": "Coordinates",
            "save": "Save",
            "added_cities": "Added cities",
        }
    },
    "modal_language_change": {
        "uk": {
            "title": "Оберіть мову додатку",
            "lang_label": "Мова додатку",
            "option_uk": "Українська",
            "option_en": "English",
            "save": "Зберегти",
            "reopen_warn": "Додаток буде перезапущено для зміни мови",
        },
        "en": {
            "title": "Select app language",
            "lang_label": "App language",
            "option_uk": "Ukrainian",
            "option_en": "English",
            "save": "Save",
            "reopen_warn": "App will be reopened for language changing",
        }
    },
    "modal_size_change": {
        "uk": {
            "title": "Оберіть розмір додатку",
            "accept_button": "Зберегти"
        },
        "en": {
            "title": "Choose the app size",
            "accept_button": "Save"
        }
    },
    "modal_image_lists": {
        "uk": {
            "title": "Списки зображень",
            "add_button": " Додати",
            "accept_button": "Зберегти"
        },
        "en": {
            "title": "Image lists",
            "add_button": " Add",
            "accept_button": "Save"
        }
    },
    "top_frame": {
        "uk": {
            "settings": "Налаштування",
            "search_placeholder": "Пошук",
            "search_results": "Результати пошуку",
        },
        "en": {
            "settings": "Settings",
            "search_placeholder": "Search",
            "search_results": "Search results",
        }
    },
    "right_container": {
        "uk": {
            "select_city": "Виберіть місто",
            "current_position": "Поточна позиція",
            "today": "Сьогодні",
            "weather_today": "Погода до кінця дня",
            "forecast_12h": "Прогноз на 12 годин",
            "max": "Макс.",
            "min": "Мін.",
            "days": {
                0: "Понеділок", 1: "Вівторок", 2: "Середа",
                3: "Четвер", 4: "П'ятниця", 5: "Субота", 6: "Неділя"
            },
        },
        "en": {
            "select_city": "Select city",
            "current_position": "Current position",
            "today": "Today",
            "weather_today": "Weather for the rest of the day",
            "forecast_12h": "12-hour forecast",
            "max": "Max.",
            "min": "Min.",
            "days": {
                0: "Monday", 1: "Tuesday", 2: "Wednesday",
                3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"
            },
        }
    },
    "weather_content": {
        "uk": {
            "max": "Макс.",
            "min": "Мін.",
        },
        "en": {
            "max": "Max.",
            "min": "Min.",
        }
    },
    "horizontal_bar_card": {
        "uk": {
            "forecast_error": "Не вдалося завантажити прогноз",
            "sunrise": "Схід",
            "sunset": "Захід",
        },
        "en": {
            "forecast_error": "Failed to load forecast",
            "sunrise": "Sunrise",
            "sunset": "Sunset",
        }
    },
    "temperature_chart": {
        "uk": {
            "forecast_error": "Не вдалося завантажити прогноз",
        },
        "en": {
            "forecast_error": "Failed to load forecast",
        }
    },
    "weather_types": {
        "uk": {
            "Clear": "Ясно",
            "Clouds": "Хмарно",
            "Rain": "Дощ",
            "Snow": "Сніг",
            "Thunderstorm": "Гроза",
            "Drizzle": "Мряка",
            "Mist": "Туман",
            "Fog": "Густий туман",
            "Haze": "Димка",
            "Dust": "Пилова буря",
            "Sand": "Піщана буря",
            "Ash": "Попіл",
            "Squall": "Шквал",
            "Tornado": "Торнадо",
        },
        "en": {
            "Clear": "Clear",
            "Clouds": "Cloudy",
            "Rain": "Rain",
            "Snow": "Snow",
            "Thunderstorm": "Thunderstorm",
            "Drizzle": "Drizzle",
            "Mist": "Mist",
            "Fog": "Fog",
            "Haze": "Haze",
            "Dust": "Dust storm",
            "Sand": "Sandstorm",
            "Ash": "Volcanic ash",
            "Squall": "Squall",
            "Tornado": "Tornado",
        }
},
}

_settings = QSettings("MyApp", "WeatherApp")
current_language = _settings.value("language", "uk")

def translater(module: str, key: str) -> str:
    return TRANSLATIONS.get(module, {}).get(current_language, {}).get(key, key)

def weather_translater(weather_key: str) -> str:
    return TRANSLATIONS["weather_types"].get(current_language, {}).get(weather_key, weather_key)

def set_language(lang: str):
    global current_language
    current_language = lang
    _settings.setValue("language", lang)