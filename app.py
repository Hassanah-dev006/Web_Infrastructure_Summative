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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
