import requests

class GeoMetClient:
    BASE_URL = "https://api.weather.gc.ca"
    source_name = "ECCC MSC GeoMet AQHI observations"

    def __init__(self, timeout: int = 20):
        self.timeout = timeout

    def _get_json(self, path: str, params: dict | None = None):
        url = f"{self.BASE_URL}{path}"
        response = requests.get(
            url,
            params=params,
            headers={"Accept": "application/geo+json, application/json"},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def get_latest_aqhi_observations(self, limit: int = 500):
        return self._get_json(
            "/collections/aqhi-observations-realtime/items",
            params={"limit": limit},
        )

    def get_aqhi_stations(self, limit: int = 500):
        return self._get_json(
            "/collections/aqhi-stations/items",
            params={"limit": limit},
        )