import time
import html
import requests
from flask import Flask, render_template, request, jsonify
import config

app = Flask(__name__)
app.secret_key = config.FLASK_SECRET_KEY

# Simple in-memory cache: { cache_key: (timestamp, data) }
_cache = {}
CACHE_TTL = 300  # 5 minutes


def _get_headers():
    return {
        "x-rapidapi-key": config.RAPIDAPI_KEY,
        "x-rapidapi-host": config.JSEARCH_HOST,
    }


def _cache_key(endpoint, params):
    sorted_params = sorted(params.items())
    return f"{endpoint}:{sorted_params}"


def _api_request(endpoint, params):
    """Make a cached request to the JSearch API."""
    key = _cache_key(endpoint, params)

    # Check cache
    if key in _cache:
        cached_time, cached_data = _cache[key]
        if time.time() - cached_time < CACHE_TTL:
            return cached_data

    url = f"{config.JSEARCH_BASE_URL}/{endpoint}"
    try:
        resp = requests.get(url, headers=_get_headers(), params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        _cache[key] = (time.time(), data)
        return data
    except requests.exceptions.Timeout:
        return {"error": "The API request timed out. Please try again."}
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            return {"error": "API rate limit reached. Please wait a moment and try again."}
        if e.response.status_code == 403:
            return {"error": "API access denied. Please check the API key configuration."}
        return {"error": f"API error: {e.response.status_code}"}
    except requests.exceptions.RequestException:
        return {"error": "Could not connect to the job search API. Please try again later."}


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
