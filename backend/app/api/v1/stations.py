from fastapi import APIRouter
from app.services.geomet_client import GeoMetClient

router = APIRouter(tags=["Stations"])

@router.get("/stations")
def get_stations():
    client = GeoMetClient()

    stations_raw = client.get_aqhi_stations(limit=500)
    obs_raw = client.get_latest_aqhi_observations(limit=500)

    station_features = stations_raw.get("features", [])
    obs_features = obs_raw.get("features", [])

    observed_ids = set()
    for feature in obs_features:
        props = feature.get("properties", {})
        station_id = (
            props.get("location_id")
            or props.get("station_id")
            or props.get("id")
        )
        aqhi_value = props.get("aqhi") or props.get("aqhi_value") or props.get("value")
        if station_id and aqhi_value is not None:
            observed_ids.add(station_id)

    stations = []
    for feature in station_features:
        props = feature.get("properties", {})
        geometry = feature.get("geometry", {})
        coords = geometry.get("coordinates", [None, None])

        station_id = (
            props.get("location_id")
            or props.get("station_id")
            or props.get("id")
        )

        station_name = (
            props.get("location_name")
            or props.get("station_name")
            or props.get("name")
            or station_id
        )

        if not station_id:
            continue

        if station_id not in observed_ids:
            continue

        stations.append({
            "station_id": station_id,
            "station_name": station_name,
            "latitude": coords[1] if len(coords) > 1 else None,
            "longitude": coords[0] if len(coords) > 0 else None,
        })

    return {"stations": stations}