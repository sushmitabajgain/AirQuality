import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

export default function PollutantChart({ data }) {
  return (
    <div className="chart-card">
      <h3>Pollutant Trends</h3>
      <ResponsiveContainer width="100%" height={320}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="timestamp" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="pm25" name="PM2.5" />
          <Line type="monotone" dataKey="o3" name="O3" />
          <Line type="monotone" dataKey="no2" name="NO2" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}