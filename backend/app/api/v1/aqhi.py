from fastapi import APIRouter, Query

from app.agents.aqhi_agent.agent import AQHIAgent
from app.schemas.aqhi import AQHIResponse

router = APIRouter(tags=["AQHI"])
agent = AQHIAgent()

@router.get("/aqhi", response_model=AQHIResponse)
def get_aqhi(city: str = Query(..., min_length=2, max_length=64)):
    result = agent.run(city)
    return AQHIResponse.from_agent(result)
