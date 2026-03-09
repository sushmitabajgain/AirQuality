def normalize_feature(feature: dict) -> dict:
    props = feature.get("properties", {})
    geometry = feature.get("geometry", {})
    coords = geometry.get("coordinates", [None, None])

    station_id = (
        props.get("location_id")
        or props.get("station_identifier")
        or props.get("station_id")
        or props.get("id")
        or props.get("code")
    )

    station_name = (
        props.get("location_name")
        or props.get("station_name")
        or props.get("name")
        or props.get("english_name")
        or props.get("label_en")
        or station_id
        or "Unknown Station"
    )

    observed_at = (
        props.get("publication_datetime")
        or props.get("observed_at")
        or props.get("datetime")
        or props.get("reference_datetime")
    )

    aqhi_value = (
        props.get("aqhi")
        or props.get("aqhi_value")
        or props.get("value")
    )

    return {
        "station_id": station_id,
        "station_name": station_name,
        "city": station_name,
        "aqhi": aqhi_value,
        "aqhi_type": props.get("aqhi_type"),
        "observed_at": observed_at,
        "latitude": coords[1] if len(coords) > 1 else None,
        "longitude": coords[0] if len(coords) > 0 else None,
    }