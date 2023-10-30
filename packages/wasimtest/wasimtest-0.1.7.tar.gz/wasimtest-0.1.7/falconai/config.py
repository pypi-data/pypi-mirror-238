import os

BASE_URL = os.getenv("FALCONAI_BASE_URL", "http://localhost:8000")
API_KEY = os.getenv("FALCONAI_AUTH_TOKEN")