import requests
from config import API_KEY

BASE_URL = "https://newsapi.org/v2"

def get_news(category="technology"):
    url = f"{BASE_URL}/top-headlines"

    params = {
        "country": "us",
        "category": category,
        "pageSize": 6,
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json().get("articles", [])

    return []


def search_news(query):
    url = f"{BASE_URL}/everything"

    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10,
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json().get("articles", [])

    return []