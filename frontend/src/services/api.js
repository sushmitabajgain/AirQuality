const API_BASE = "http://localhost:8000";

export async function fetchAQHI(city) {
  const response = await fetch(
    `${API_BASE}/api/v1/aqhi?city=${encodeURIComponent(city)}`
  );

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return await response.json();
}
