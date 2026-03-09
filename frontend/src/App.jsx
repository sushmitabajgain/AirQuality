import { useState } from "react";
import { fetchAQHI } from "./services/api";

export default function App() {
  const [city, setCity] = useState("Edmonton");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSearch() {
    try {
      setLoading(true);
      setError("");
      const result = await fetchAQHI(city);
      setData(result);
    } catch (err) {
      setError(err.message || "Failed to fetch AQHI data");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}>
      <h1>Alberta Air Quality Explorer</h1>

      <div style={{ marginBottom: "1rem" }}>
        <input
          value={city}
          onChange={(e) => setCity(e.target.value)}
          placeholder="Enter city"
          style={{ padding: "0.5rem", marginRight: "0.5rem" }}
        />
        <button onClick={handleSearch} style={{ padding: "0.5rem 1rem" }}>
          Search
        </button>
      </div>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {data && (
        <div style={{ border: "1px solid #ccc", padding: "1rem", borderRadius: "8px" }}>
          <h2>{data.resolved?.location_name || data.query_city}</h2>
          <p><strong>AQHI:</strong> {data.observation?.aqhi ?? "N/A"}</p>
          <p><strong>Category:</strong> {data.advice?.category}</p>
          <p><strong>Observed at:</strong> {data.observation?.observed_at || "N/A"}</p>
          <p><strong>General advice:</strong> {data.advice?.general}</p>
          <p><strong>At-risk advice:</strong> {data.advice?.at_risk}</p>
          <p><strong>Source:</strong> {data.source}</p>
        </div>
      )}
    </div>
  );
}
