from fastapi import FastAPI
from agent.tools import get_latest_aqhi
from agent.rules import aqhi_risk_level, health_advice

app = FastAPI(title="Alberta Air Quality Agent")

@app.get("/")
def root():
    return {"message": "Backend running"}

@app.get("/aqhi/{city}")
def aqhi(city: str):
    data = get_latest_aqhi(city)

    if not data:
        return {"error": "No AQHI data found for this city"}

    aqhi_value = data["aqhi"]

    return {
        "city": city,
        "aqhi": aqhi_value,
        "risk_level": aqhi_risk_level(aqhi_value),
        "health_advice": health_advice(aqhi_value),
        "observed_at": data["observed_at"],
        "source": "Government of Canada – AQHI (weather.gc.ca)"
    }
