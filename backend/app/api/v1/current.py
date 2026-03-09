from fastapi import APIRouter, Query, HTTPException
from app.services.geomet_client import GeoMetClient
from app.services.aqhi_normalizer import normalize_feature

router = APIRouter(tags=["Current AQHI"])

@router.get("/current")
def get_current_aqhi(station_id: str = Query(...)):
    client = GeoMetClient()
    raw = client.get_latest_aqhi_observations(limit=500)
    features = raw.get("features", [])

    for feature in features:
        item = normalize_feature(feature)
        if item.get("station_id") == station_id:
            aqhi = item.get("aqhi")
            category = "Unknown"
            if aqhi is not None:
                if aqhi <= 3:
                    category = "Low"
                elif aqhi <= 6:
                    category = "Moderate"
                elif aqhi <= 10:
                    category = "High"
                else:
                    category = "Very High"

            return {
                "resolved": {
                    "location_id": item["station_id"],
                    "location_name": item["station_name"],
                },
                "observation": {
                    "aqhi": item.get("aqhi"),
                    "aqhi_type": item.get("aqhi_type"),
                    "observed_at": item.get("observed_at"),
                },
                "advice": {
                    "category": category,
                    "general": "Reduce or reschedule strenuous activities outdoors if symptoms occur.",
                    "at_risk": "Consider reducing or rescheduling strenuous outdoor activities if symptoms occur.",
                },
                "source": "ECCC MSC GeoMet AQHI observations",
            }

    raise HTTPException(status_code=404, detail="Station not found")