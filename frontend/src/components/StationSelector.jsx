export default function StationSelector({
  stations,
  selectedStationId,
  onChange,
}) {
  return (
    <div className="selector-row">
      <label htmlFor="station-select"><strong>Select station:</strong></label>
      <select
        id="station-select"
        value={selectedStationId}
        onChange={(e) => onChange(e.target.value)}
      >
        <option value="">Choose a station</option>
        {stations.map((station) => (
          <option key={station.station_id} value={station.station_id}>
            {station.station_name} ({station.city})
          </option>
        ))}
      </select>
    </div>
  );
}