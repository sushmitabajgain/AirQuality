from typing import Literal

RiskCategory = Literal["Low", "Moderate", "High", "Very High", "Unknown"]


def _category(aqhi: float) -> RiskCategory:
    # AQHI commonly reported 1-10 (and sometimes 10+). Be defensive.
    if aqhi <= 0:
        return "Unknown"
    if 1 <= aqhi <= 3:
        return "Low"
    if 4 <= aqhi <= 6:
        return "Moderate"
    if 7 <= aqhi <= 10:
        return "High"
    if aqhi > 10:
        return "Very High"
    return "Unknown"


def advice_for_aqhi(aqhi: float | None) -> dict:
    if aqhi is None:
        return {
            "category": "Unknown",
            "general": "No AQHI reading is available right now.",
            "at_risk": "No AQHI reading is available right now.",
        }

    cat = _category(aqhi)

    # Human-friendly guidance (tune later to match official wording exactly if desired)
    if cat == "Low":
        return {
            "category": cat,
            "general": "Air quality is good. Enjoy your usual outdoor activities.",
            "at_risk": "Air quality is good. Enjoy your usual outdoor activities.",
        }
    if cat == "Moderate":
        return {
            "category": cat,
            "general": "Air quality is acceptable. Consider reducing strenuous outdoor activity if you notice symptoms.",
            "at_risk": "Consider reducing or rescheduling strenuous outdoor activity if you notice symptoms (e.g., coughing, throat irritation).",
        }
    if cat == "High":
        return {
            "category": cat,
            "general": "Consider reducing or rescheduling strenuous outdoor activities if you notice symptoms.",
            "at_risk": "Reduce or reschedule strenuous outdoor activities, especially if you have heart/lung conditions, are older, pregnant, or have young children.",
        }
    if cat == "Very High":
        return {
            "category": cat,
            "general": "Reduce or avoid strenuous outdoor activity. Consider staying indoors if you have symptoms.",
            "at_risk": "Avoid strenuous outdoor activity and limit time outdoors. Consider staying indoors and keeping indoor air clean (e.g., HEPA filtration).",
        }

    return {
        "category": "Unknown",
        "general": "AQHI reading is outside expected range.",
        "at_risk": "AQHI reading is outside expected range.",
    }
