from fastapi import APIRouter, Query

router = APIRouter(tags=["Observations"])

@router.get("/observations")
def get_observations(
    station_id: str = Query(...),
    hours: int = Query(24, ge=1, le=168),
):
    # Query PostgreSQL here for the last N hours
    # SELECT observed_at, aqhi, pm25, o3, no2 ...
    return {
        "station_id": station_id,
        "series": [
            # rows from DB
        ],
    }