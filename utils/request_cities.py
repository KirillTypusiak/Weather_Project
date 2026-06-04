import requests

_all_cities: list[str] = []


def load_cities() -> None:
    global _all_cities
    try:
        response = requests.get(
            "https://countriesnow.space/api/v0.1/countries",
            timeout=10
        )
        data = response.json()
        for country in data["data"]:
            _all_cities.extend(country["cities"])
        print(f"Завантажено {len(_all_cities)} міст")
    except Exception as err:
        print(f"Помилка завантаження міст: {err}")


def request_cities(city_name: str) -> list[str]:
    if len(city_name) < 2:
        return []
    return [
        city for city in _all_cities
        if city_name.lower() in city.lower()
    ][:20]