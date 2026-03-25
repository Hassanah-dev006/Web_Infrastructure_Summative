import os
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-in-production")
JSEARCH_HOST = "jsearch.p.rapidapi.com"
JSEARCH_BASE_URL = f"https://{JSEARCH_HOST}"
