import os
import json
from pathlib import Path

# Twitter API Credentials - from environment variable
API_BEARER_TOKEN = os.getenv(
    "TWITTER_BEARER_TOKEN",
    "AAAAAAAAAAAAAAAAAAAAALNx6QEAAAAALuzMfBRbUi1AGrhZpS72GgkILHY%3DU1uJ2SSXdDEDeCmbvKwZqSzy5d9fyBrdfUcyNqBQP3NtcANO03"
)

# Database Path
DB_PATH = os.getenv("DB_PATH", "sentiment.db")

# Cache policy: when checking DB for cached tweets, how many hours back to consider fresh
CACHE_HOURS = int(os.getenv("CACHE_HOURS", "10"))

# Twitter API max is 100
MAX_TWEETS_PER_CALL = int(os.getenv("MAX_TWEETS_PER_CALL", "15"))

# Service Account Path or JSON string
SERVICE_ACCOUNT_PATH = os.getenv("SERVICE_ACCOUNT_PATH", "serviceAccountKey.json")

# Firebase credentials from environment (for Railway deployment)
# This can be either a file path or JSON string
FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS", None)

# Port for the application (Railway sets this automatically)
PORT = int(os.getenv("PORT", "8000"))

