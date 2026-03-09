import requests
from datetime import datetime

AQHI_URL = "https://api.weather.gc.ca/collections/aqhi-observations-realtime/items"

def get_latest_aqhi(city: str):
    params = {
        "limit": 200,
        "f": "json"
    }

    response = requests.get(AQHI_URL, params=params, timeout=10)
    response.raise_for_status()

    features = response.json()["features"]

    matches = []

    for item in features:
        props = item["properties"]
        if props["location_name_en"].lower() == city.lower():
            matches.append({
                "aqhi": props["aqhi"],
                "observed_at": props["observation_datetime"],
                "location_id": props["location_id"]
            })

    if not matches:
        return None

    latest = max(
        matches,
        key=lambda x: datetime.fromisoformat(x["observed_at"].replace("Z", ""))
    )

    return latest
