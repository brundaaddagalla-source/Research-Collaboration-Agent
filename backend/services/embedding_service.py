import os
from pathlib import Path

import requests
from dotenv import load_dotenv


# Load .env from backend folder
BACKEND_DIR = Path(__file__).resolve().parents[1]
ENV_PATH = BACKEND_DIR / ".env"

load_dotenv(ENV_PATH)


API_KEY = os.getenv("FREELLMAPI_API_KEY")

BASE_URL = os.getenv(
    "FREELLMAPI_BASE_URL",
    "http://127.0.0.1:31415/v1"
)

MODEL = "bge-m3"


def get_embedding(text):
    """
    Generate an embedding using bge-m3.
    """

    if not API_KEY:
        raise ValueError("FREELLMAPI_API_KEY is not set")

    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    response = requests.post(
        f"{BASE_URL}/embeddings",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "input": text,
        },
        timeout=300,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Embedding API failed: "
            f"{response.status_code} - {response.text}"
        )

    result = response.json()

    embedding = result["data"][0]["embedding"]

    return embedding