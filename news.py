import logging

import requests

from config import API_KEY

logger = logging.getLogger(__name__)

BASE_URL = "https://newsapi.org/v2"
REQUEST_TIMEOUT = 10


def _api_error_message(response):
    try:
        data = response.json()
        message = data.get("message")
        if message:
            return message
    except ValueError:
        pass

    if response.status_code == 401:
        return "Invalid News API key. Set NEWS_API_KEY in your environment or .env file."
    if response.status_code == 429:
        return "News API rate limit exceeded. Please try again later."

    return f"News API returned an error ({response.status_code})."


def _fetch_articles(url, params):
    if not API_KEY:
        return [], "News API key is not configured. Set NEWS_API_KEY in your environment or .env file."

    try:
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.Timeout:
        logger.error("News API request timed out for %s", url)
        return [], "News service timed out. Please try again."
    except requests.exceptions.RequestException as exc:
        logger.error("News API request failed: %s", exc)
        return [], "Unable to reach the news service. Please try again later."

    if response.status_code == 200:
        return response.json().get("articles", []), None

    message = _api_error_message(response)
    logger.error("News API error %s: %s", response.status_code, message)
    return [], message


def get_news(category="technology"):
    url = f"{BASE_URL}/top-headlines"

    params = {
        "country": "us",
        "category": category,
        "pageSize": 6,
        "apiKey": API_KEY,
    }

    return _fetch_articles(url, params)


def search_news(query):
    url = f"{BASE_URL}/everything"

    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10,
        "apiKey": API_KEY,
    }

    return _fetch_articles(url, params)
