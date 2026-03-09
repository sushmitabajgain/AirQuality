from app.agents.aqhi_agent.types import (
    AgentAdvice,
    AgentLocation,
    AgentObservation,
    AgentResult,
)
from app.services.aqhi_client import AQHIClient
from app.services.advice_engine import advice_for_aqhi


class AQHIAgent:
    """
    AQHI Agent
    - resolve city -> station location_id
    - fetch latest realtime AQHI
    - interpret AQHI -> category + advice
    """

    def __init__(self, client: AQHIClient | None = None) -> None:
        self._client = client or AQHIClient()

    def run(self, city: str) -> AgentResult:
        city_clean = (city or "").strip()

        candidates = self._client.search_stations(city_clean)
        if not candidates:
            advice = advice_for_aqhi(None)
            return AgentResult(
                city=city_clean,
                resolved=None,
                observation=None,
                advice=AgentAdvice(**advice),
                alternates=[],
                source=self._client.source_name,
            )

        resolved = candidates[0]
        alternates = candidates[1:6]

        obs = self._client.latest_observation(resolved.location_id)

        advice_dict = advice_for_aqhi(obs.aqhi)

        return AgentResult(
            city=city_clean,
            resolved=AgentLocation(resolved.location_id, resolved.location_name),
            observation=AgentObservation(obs.aqhi, obs.aqhi_type, obs.observed_at),
            advice=AgentAdvice(**advice_dict),
            alternates=[AgentLocation(a.location_id, a.location_name) for a in alternates],
            source=self._client.source_name,
        )
