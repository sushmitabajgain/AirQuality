import { useEffect, useState } from "react";
import {
  fetchStations,
  fetchAQHIByStation,
  fetchObservations,
} from "./services/api";
import StationSelector from "./components/StationSelector";
import AQHILineChart from "./components/AQHILineChart";
import PollutantChart from "./components/PollutantChart";
import "./App.css";

export default function App() {
  const [stations, setStations] = useState([]);
  const [selectedStationId, setSelectedStationId] = useState("");
  const [aqhiData, setAqhiData] = useState(null);
  const [series, setSeries] = useState([]);
  const [loadingStations, setLoadingStations] = useState(false);
  const [loadingData, setLoadingData] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadStations() {
      try {
        setLoadingStations(true);
        setError("");
        const result = await fetchStations();
        const stationList = result.stations || [];
        setStations(stationList);

        if (stationList.length > 0) {
          setSelectedStationId(stationList[0].station_id);
        }
      } catch (err) {
        setError(err.message || "Failed to load stations");
      } finally {
        setLoadingStations(false);
      }
    }

    loadStations();
  }, []);

  useEffect(() => {
    if (!selectedStationId) return;

    async function loadStationData() {
      try {
        setLoadingData(true);
        setError("");

        const current = await fetchAQHIByStation(selectedStationId);
        setAqhiData(current);

        const obs = await fetchObservations(selectedStationId, 24);
        setSeries(obs.series || []);
      } catch (err) {
        setError(err.message || "Failed to load station data");
      } finally {
        setLoadingData(false);
      }
    }

    loadStationData();
  }, [selectedStationId]);

  return (
    <div className="page">
      <h1>Agent-Based Alberta Air Quality Explorer</h1>

      {loadingStations && <p>Loading stations...</p>}
      {error && <p className="error">{error}</p>}

      <StationSelector
        stations={stations}
        selectedStationId={selectedStationId}
        onChange={setSelectedStationId}
      />

      {loadingData && <p>Loading air quality data...</p>}

      {aqhiData && (
        <div className="card">
          {aqhiData?.observation?.aqhi == null && (
            <p className="error">No current live AQHI observation is available for this station.</p>
          )}
          <h2>
            {aqhiData?.resolved?.location_name ||
              stations.find((s) => s.station_id === selectedStationId)?.station_name ||
              selectedStationId ||
              "Unknown Station"}
          </h2>
          <p><strong>Station ID:</strong> {selectedStationId}</p>
          <p><strong>AQHI:</strong> {aqhiData.observation?.aqhi ?? "N/A"}</p>
          <p><strong>Category:</strong> {aqhiData.advice?.category ?? "N/A"}</p>
          <p><strong>Observed at:</strong> {aqhiData.observation?.observed_at ?? "N/A"}</p>
          <p><strong>Source:</strong> {aqhiData.source ?? "N/A"}</p>
        </div>
      )}

      {series.length > 0 && (
        <>
          <AQHILineChart data={series} />
          <PollutantChart data={series} />
        </>
      )}
    </div>
  );
}