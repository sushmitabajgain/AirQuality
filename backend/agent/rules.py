def aqhi_risk_level(aqhi: float) -> str:
    if aqhi <= 3:
        return "Low"
    elif aqhi <= 6:
        return "Moderate"
    elif aqhi <= 10:
        return "High"
    else:
        return "Very High"


def health_advice(aqhi: float) -> str:
    if aqhi <= 3:
        return "Ideal air quality. Enjoy outdoor activities."
    elif aqhi <= 6:
        return (
            "Moderate air quality. Sensitive individuals should "
            "consider reducing prolonged outdoor exertion."
        )
    elif aqhi <= 10:
        return (
            "High air pollution. Reduce or reschedule strenuous "
            "outdoor activities."
        )
    else:
        return (
            "Very high air pollution. Avoid outdoor activities and "
            "follow public health advice."
        )
