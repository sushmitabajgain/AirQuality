from app.agents.aqhi_agent.models import (
    AgentAdvice,
    AgentLocation,
    AgentObservation,
    AgentResult,
)

class AQHIAgent:
    def __init__(self, client):
        self._client = client

    def run(self, station_id: str) -> AgentResult:
        obs_raw = self._client.get_latest_aqhi_observations(limit=500)
        obs_features = obs_raw.get("features", [])

        station_raw = self._client.get_aqhi_stations(limit=500)
        station_features = station_raw.get("features", [])

        station_name = station_id
        for feature in station_features:
            props = feature.get("properties", {})
            current_id = (
                props.get("location_id")
                or props.get("station_id")
                or props.get("id")
            )
            if current_id == station_id:
                station_name = (
                    props.get("location_name")
                    or props.get("station_name")
                    or props.get("name")
                    or station_id
                )
                break

        match = None
        for feature in obs_features:
            props = feature.get("properties", {})
            current_id = (
                props.get("location_id")
                or props.get("station_id")
                or props.get("id")
            )
            if current_id == station_id:
                match = feature
                break

        if match is None:
            return AgentResult(
                city=station_name,
                resolved=AgentLocation(
                    location_id=station_id,
                    location_name=station_name,
                ),
                observation=None,
                advice=AgentAdvice(
                    category="Unknown",
                    general="No matching observation was found.",
                    at_risk="No matching observation was found.",
                ),
                alternates=[],
                source=self._client.source_name,
            )

        props = match.get("properties", {})
        aqhi_value = props.get("aqhi") or props.get("aqhi_value")

        observed_at = (
            props.get("publication_datetime")
            or props.get("datetime")
            or props.get("reference_datetime")
            or props.get("LOCAL_DATE")
        )

        aqhi_float = None
        category = "Unknown"
        if aqhi_value is not None:
            try:
                aqhi_float = float(aqhi_value)
                if aqhi_float <= 3:
                    category = "Low"
                elif aqhi_float <= 6:
                    category = "Moderate"
                elif aqhi_float <= 10:
                    category = "High"
                else:
                    category = "Very High"
            except (TypeError, ValueError):
                pass

        return AgentResult(
            city=station_name,
            resolved=AgentLocation(
                location_id=station_id,
                location_name=station_name,
            ),
            observation=AgentObservation(
                aqhi=aqhi_float,
                aqhi_type=props.get("aqhi_type"),
                observed_at=observed_at,
            ),
            advice=AgentAdvice(
                category=category,
                general="Reduce or reschedule strenuous outdoor activities if symptoms occur.",
                at_risk="Consider reducing or rescheduling strenuous outdoor activities if symptoms occur.",
            ),
            alternates=[],
            source=self._client.source_name,
        )