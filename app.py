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


@app.route("/search")
def search():
    query = request.args.get("query", "").strip()
    location = request.args.get("location", "").strip()
    employment_type = request.args.get("employment_type", "")
    date_posted = request.args.get("date_posted", "all")
    sort_by = request.args.get("sort_by", "relevance")
    remote_only = request.args.get("remote_only", "")
    page = request.args.get("page", "1")

    if not query:
        return render_template("results.html", jobs=[], query="",
                               error="Please enter a search query.")

    params = {
        "query": query,
        "page": page,
        "num_pages": "1",
        "date_posted": date_posted,
    }

    if location:
        params["query"] += f" in {location}"

    if employment_type:
        params["employment_types"] = employment_type

    if remote_only:
        params["remote_jobs_only"] = "true"

    data = _api_request("search", params)

    if "error" in data:
        return render_template("results.html", jobs=[], query=query,
                               error=data["error"])

    jobs = data.get("data", [])

    # Server-side sorting
    if sort_by == "date":
        jobs.sort(key=lambda j: j.get("job_posted_at_datetime_utc", ""), reverse=True)
    elif sort_by == "salary_desc":
        jobs.sort(key=lambda j: j.get("job_max_salary") or 0, reverse=True)

    return render_template(
        "results.html",
        jobs=jobs,
        query=query,
        location=location,
        employment_type=employment_type,
        date_posted=date_posted,
        sort_by=sort_by,
        remote_only=remote_only,
        page=int(page),
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
