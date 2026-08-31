import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path


load_dotenv()


def fetch_flights(limit=10, offset=0, timeout=10):
    access_key = os.getenv("AVIATIONSTACK_ACCESS_KEY")
    if not access_key:
        raise RuntimeError("AVIATIONSTACK_ACCESS_KEY not set in environment")

    url = "https://api.aviationstack.com/v1/flights"
    params = {
        "access_key": access_key,
        "limit": limit,
        "offset": offset,
    }

    response = requests.get(url, params=params, timeout=timeout)
    response.raise_for_status()
    data = response.json()

    if "error" in data:
        raise RuntimeError(f"API error: {data['error']}")

    return data


def save_raw_payload(data, raw_dir="data/raw"):
    Path(raw_dir).mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"{raw_dir}/flights_{timestamp}.json"

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    return filepath

