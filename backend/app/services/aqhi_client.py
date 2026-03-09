from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional

import httpx
from cachetools import TTLCache

from app.core.config import settings
from app.utils.datetime import parse_iso_datetime


@dataclass(frozen=True)
class ResolvedStation:
    location_id: str
    location_name: str


@dataclass(frozen=True)
class Observation:
    aqhi: Optional[float]
    aqhi_type: Optional[str]
    observed_at: Optional[datetime]
    raw: dict[str, Any]


class GeoMetError(Exception):
    pass


class AQHIClient:
    """
    Minimal, robust GeoMet client.

    Notes:
    - GeoMet is OGC API Features; server-side filtering can vary.
    - This client uses a pragmatic strategy:
      - fetch stations with a larger limit, filter locally
      - fetch observations for a resolved location_id, prefer latest
    """

    source_name = "ECCC MSC GeoMet (AQHI)"

    def __init__(self) -> None:
        self._http = httpx.Client(
            base_url=settings.GEOMET_BASE_URL,
            timeout=settings.HTTP_TIMEOUT_S,
            headers={"Accept": "application/geo+json, application/json"},
        )
        self._station_cache: TTLCache[str, list[ResolvedStation]] = TTLCache(
            maxsize=512, ttl=settings.STATION_CACHE_TTL_S
        )
        self._obs_cache: TTLCache[str, Observation] = TTLCache(
            maxsize=2048, ttl=settings.OBS_CACHE_TTL_S
        )

    def close(self) -> None:
        self._http.close()

    def _get_json(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        r = self._http.get(path, params=params)
        if r.status_code >= 400:
            raise GeoMetError(f"GeoMet error {r.status_code}: {r.text[:200]}")
        return r.json()

    def search_stations(self, city: str, limit_fetch: int = 500) -> list[ResolvedStation]:
        """
        Resolve user city string to candidate station locations.

        - fetch station items (cached)
        - filter by substring match on location_name_en
        - rank: exact match > startswith > contains
        """
        city_clean = (city or "").strip()
        if not city_clean:
            return []

        cache_key = city_clean.lower()
        if cache_key in self._station_cache:
            return self._station_cache[cache_key]

        # Fetch a chunk of stations; GeoMet might paginate, but this is usually enough for AQHI.
        data = self._get_json(settings.AQHI_STATIONS_PATH, params={"limit": limit_fetch})
        feats = data.get("features") or []

        city_norm = city_clean.lower()

        candidates: list[ResolvedStation] = []
        for f in feats:
            props = f.get("properties") or {}
            name = (props.get("location_name_en") or "").strip()
            loc_id = (props.get("location_id") or "").strip()
            if not name or not loc_id:
                continue
            if city_norm in name.lower():
                candidates.append(ResolvedStation(location_id=loc_id, location_name=name))

        # Rank candidates
        def rank(s: ResolvedStation) -> tuple[int, int]:
            name_l = s.location_name.lower()
            if name_l == city_norm:
                return (0, len(name_l))
            if name_l.startswith(city_norm):
                return (1, len(name_l))
            return (2, len(name_l))

        candidates.sort(key=rank)
        self._station_cache[cache_key] = candidates
        return candidates

    def latest_observation(self, location_id: str) -> Observation:
        """
        Fetch latest realtime observation for a location_id.
        Uses caching and picks the best candidate (latest==true, then most recent datetime).
        """
        loc = (location_id or "").strip()
        if not loc:
            return Observation(aqhi=None, aqhi_type=None, observed_at=None, raw={})

        if loc in self._obs_cache:
            return self._obs_cache[loc]

        data = self._get_json(
            settings.AQHI_OBS_PATH,
            params={
                "limit": 25,
                "location_id": loc,
                "latest": "true",  # if supported upstream
            },
        )

        feats = data.get("features") or []
        if not feats:
            obs = Observation(aqhi=None, aqhi_type=None, observed_at=None, raw=data)
            self._obs_cache[loc] = obs
            return obs

        def score(f: dict[str, Any]) -> tuple[int, datetime]:
            props = f.get("properties") or {}
            is_latest = 1 if props.get("latest") is True else 0
            dt = (
                parse_iso_datetime(props.get("observation_datetime"))
                or parse_iso_datetime(props.get("datetime"))
                or datetime(1970, 1, 1, tzinfo=timezone.utc)
            )
            return (is_latest, dt)

        best = sorted(feats, key=score, reverse=True)[0]
        props = best.get("properties") or {}

        aqhi_raw = props.get("aqhi")
        try:
            aqhi_val = float(aqhi_raw) if aqhi_raw is not None else None
        except Exception:
            aqhi_val = None

        obs_dt = (
            parse_iso_datetime(props.get("observation_datetime"))
            or parse_iso_datetime(props.get("datetime"))
        )

        obs = Observation(
            aqhi=aqhi_val,
            aqhi_type=(props.get("aqhi_type") or None),
            observed_at=obs_dt,
            raw=props,
        )
        self._obs_cache[loc] = obs
        return obs
