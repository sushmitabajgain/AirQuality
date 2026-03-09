from dataclasses import dataclass
from typing import Optional, Literal

RiskCategory = Literal["Low", "Moderate", "High", "Very High", "Unknown"]

@dataclass
class AgentLocation:
    location_id: str
    location_name: str

@dataclass
class AgentObservation:
    aqhi: Optional[float]
    aqhi_type: Optional[str]
    observed_at: Optional[str]

@dataclass
class AgentAdvice:
    category: RiskCategory
    general: str
    at_risk: str

@dataclass
class AgentResult:
    city: str
    resolved: Optional[AgentLocation]
    observation: Optional[AgentObservation]
    advice: AgentAdvice
    alternates: list[AgentLocation]
    source: str