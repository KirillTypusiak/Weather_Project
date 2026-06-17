# import requests

# _all_cities: list[str] = []


# def load_cities() -> None:
#     global _all_cities
#     try:
#         response = requests.get(
#             "https://countriesnow.space/api/v0.1/countries",
#             timeout=10
#         )
#         data = response.json()
#         for country in data["data"]:
#             _all_cities.extend(country["cities"])
#         # print(f"Завантажено {len(_all_cities)} міст")
#     except Exception as err:
#         print(f"Помилка завантаження міст: {err}")


# def request_cities(city_name: str) -> list[str]:
#     if len(city_name) < 2:
#         return []
#     return [
#         city for city in _all_cities
#         if city_name.lower() in city.lower()
#     ][:20]


import requests
import utils.translate as translate

def request_cities(city_name: str, country_code: str = None) -> list[str]:
    if len(city_name) < 2:
        return []
    try:
        params = {
            "q": city_name,
            "format": "json",
            "limit": 20,
            "featureType": "city",
            "accept-language": translate.current_language,
        }
        if country_code:
            params["countrycodes"] = country_code
            
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params=params,
            headers={"User-Agent": "CityFinderApp/1.0"},
            timeout=10
        )
        data = response.json()
        cities = []
        for item in data:
            name = item.get("name", "")
            if name and name not in cities:
                cities.append(name)
        return cities
    except Exception:
        return []
    
def get_english_city_name(city_name: str) -> str:
    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={
                "q": city_name,
                "format": "json",
                "limit": 1,
                "accept-language": "en",
            },
            headers={"User-Agent": "CityFinderApp/1.0"},
            timeout=10
        )
        data = response.json()
        if data:
            return data[0].get("name", city_name)
    except Exception:
        pass
    return city_name

def translate_city_name(api_name: str) -> str:
    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={
                "q": api_name,
                "format": "json",
                "limit": 1,
                "accept-language": translate.current_language,
            },
            headers={"User-Agent": "CityFinderApp/1.0"},
            timeout=10
        )
        data = response.json()
        if data:
            return data[0].get("name", api_name)
    except Exception:
        pass
    return api_name

def request_countries(query: str) -> list[dict]:
    if len(query) < 1:
        return []
    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={
                "q": query,
                "format": "json",
                "limit": 15,
                "featureType": "country",
                "addressdetails": 1,
                "accept-language": translate.current_language,
            },
            headers={"User-Agent": "CityFinderApp/1.0"},
            timeout=10
        )
        data = response.json()
        results = []
        seen = set()
        for item in data:
            name = item.get("name", "")
            code = item.get("address", {}).get("country_code", "")
            if name and name not in seen:
                seen.add(name)
                results.append({"name": name, "code": code})
        return results
    except Exception:
        return []