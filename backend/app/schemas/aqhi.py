from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, Field

from app.agents.aqhi_agent.types import AgentResult, RiskCategory


class ResolvedLocation(BaseModel):
    location_id: str
    location_name: str


class Observation(BaseModel):
    aqhi: Optional[float] = None
    aqhi_type: Optional[str] = None
    observed_at: Optional[datetime] = None


class Advice(BaseModel):
    category: RiskCategory
    general: str
    at_risk: str


class AQHIResponse(BaseModel):
    query_city: str
    resolved: Optional[ResolvedLocation] = None
    observation: Optional[Observation] = None
    advice: Advice
    alternates: list[ResolvedLocation] = Field(default_factory=list)
    source: str

    @staticmethod
    def from_agent(result: AgentResult) -> "AQHIResponse":
        return AQHIResponse(
            query_city=result.city,
            resolved=(
                ResolvedLocation(
                    location_id=result.resolved.location_id,
                    location_name=result.resolved.location_name,
                )
                if result.resolved
                else None
            ),
            observation=(
                Observation(
                    aqhi=result.observation.aqhi,
                    aqhi_type=result.observation.aqhi_type,
                    observed_at=result.observation.observed_at,
                )
                if result.observation
                else None
            ),
            advice=Advice(
                category=result.advice.category,
                general=result.advice.general,
                at_risk=result.advice.at_risk,
            ),
            alternates=[
                ResolvedLocation(location_id=a.location_id, location_name=a.location_name)
                for a in result.alternates
            ],
            source=result.source,
        )
