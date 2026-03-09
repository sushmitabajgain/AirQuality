const API_BASE = import.meta.env.VITE_API_BASE;

async function request(path) {
  const response = await fetch(`${API_BASE}${path}`);

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return await response.json();
}

export async function fetchStations() {
  return request("/api/v1/stations");
}

export async function fetchAQHIByStation(stationId) {
  return request(`/api/v1/aqhi?station_id=${encodeURIComponent(stationId)}`);
}

export async function fetchObservations(stationId, hours = 24) {
  return request(
    `/api/v1/observations?station_id=${encodeURIComponent(stationId)}&hours=${hours}`
  );
}