import requests
from config import API_KEY

def request_forecast(city_name):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}"
    try:
        response = requests.get(url)
        return response.json()
    except:
        return {"cod": "404"}