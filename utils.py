import urllib.request
import urllib.parse
import urllib.error
import json
import time
from config import SLEEP_BETWEEN_REQUESTS

def api_get(url):
    """Performs a GET request to an API and returns the JSON data."""
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
            return json.loads(data)
    except Exception:
        return None

def fetch_bytes(url):
    """Downloads binary data from a URL."""
    try:
        with urllib.request.urlopen(url) as response:
            return response.read()
    except Exception:
        return None

def sleep_api():
    """Sleeps between requests to respect API rate limits."""
    time.sleep(SLEEP_BETWEEN_REQUESTS)
