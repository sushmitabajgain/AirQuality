from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    GEOMET_BASE_URL: str = "https://api.weather.gc.ca"

    AQHI_OBS_PATH: str = "/collections/aqhi-observations-realtime/items"
    AQHI_STATIONS_PATH: str = "/collections/aqhi-stations/items"

    HTTP_TIMEOUT_S: float = 10.0

    # caching
    STATION_CACHE_TTL_S: int = 24 * 60 * 60
    OBS_CACHE_TTL_S: int = 120


settings = Settings()
