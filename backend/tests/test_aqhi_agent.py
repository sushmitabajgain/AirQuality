from datetime import datetime, timezone

from app.agents.aqhi_agent.agent import AQHIAgent
from app.services.aqhi_client import AQHIClient, ResolvedStation, Observation


class FakeClient(AQHIClient):
    def __init__(self) -> None:
        # don't call super() to avoid real network client
        self.source_name = "Fake"

    def search_stations(self, city: str, limit_fetch: int = 500):
        if city.lower() == "edmonton":
            return [ResolvedStation("YEG", "Edmonton")]
        return []

    def latest_observation(self, location_id: str):
        return Observation(
            aqhi=3.0,
            aqhi_type="observed",
            observed_at=datetime(2026, 1, 28, tzinfo=timezone.utc),
            raw={},
        )


def test_agent_no_city_match():
    agent = AQHIAgent(client=FakeClient())
    res = agent.run("NoSuchCity")
    assert res.resolved is None
    assert res.advice.category == "Unknown"


def test_agent_happy_path_low():
    agent = AQHIAgent(client=FakeClient())
    res = agent.run("Edmonton")
    assert res.resolved is not None
    assert res.resolved.location_id == "YEG"
    assert res.observation is not None
    assert res.observation.aqhi == 3.0
    assert res.advice.category == "Low"
