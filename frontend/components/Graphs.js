import { LineChart, Line, BarChart, Bar, CartesianGrid, XAxis, YAxis, Tooltip } from "recharts";

export default function Graphs({ data }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <div className="bg-white rounded-lg shadow p-4">
        <h3 className="text-sm font-semibold mb-2">Avg Price/m²</h3>
        <LineChart width={300} height={200} data={data}>
          <CartesianGrid stroke="#ccc" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="avg_price" stroke="#2563eb" />
        </LineChart>
      </div>
      <div className="bg-white rounded-lg shadow p-4">
        <h3 className="text-sm font-semibold mb-2">Min/Median/Max</h3>
        <LineChart width={300} height={200} data={data}>
          <CartesianGrid stroke="#ccc" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="min" stroke="#16a34a" />
          <Line type="monotone" dataKey="median" stroke="#f59e0b" />
          <Line type="monotone" dataKey="max" stroke="#dc2626" />
        </LineChart>
      </div>
      <div className="bg-white rounded-lg shadow p-4">
        <h3 className="text-sm font-semibold mb-2">Total Listings</h3>
        <BarChart width={300} height={200} data={data}>
          <CartesianGrid stroke="#ccc" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="count" fill="#3b82f6" />
        </BarChart>
      </div>
    </div>
  );
}
