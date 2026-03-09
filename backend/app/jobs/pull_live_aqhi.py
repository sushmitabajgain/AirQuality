from app.services.geomet_client import GeoMetClient
from app.services.aqhi_normalizer import normalize_feature

def run():
    client = GeoMetClient()
    raw = client.get_latest_aqhi_observations(limit=500)
    features = raw.get("features", [])

    rows = []
    for feature in features:
        item = normalize_feature(feature)
        rows.append(item)

    # insert rows into PostgreSQL here
    # deduplicate on (station_id, observed_at)
    print(f"Prepared {len(rows)} live AQHI rows")