from fastapi import APIRouter, Query
from app.agents.aqhi_agent.agent import AQHIAgent
from app.services.geomet_client import GeoMetClient

router = APIRouter(tags=["AQHI"])

@router.get("/aqhi")
def get_aqhi(station_id: str = Query(...)):
    client = GeoMetClient()
    agent = AQHIAgent(client)
    result = agent.run(station_id=station_id)
    return result