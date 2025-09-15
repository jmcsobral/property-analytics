// frontend/components/Graphs.js
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function Graphs({ data }) {
  // optional: small formatters for nicer axes tooltips
  const currency = (v) =>
    typeof v === "number" ? v.toLocaleString(undefined, { maximumFractionDigits: 0 }) : v;
  const integer = (v) =>
    typeof v === "number" ? Math.round(v).toLocaleString() : v;

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      {/* Avg Price / m² */}
      <div className="bg-white rounded-lg shadow p-4">
        <h3 className="text-sm font-semibold mb-2">Avg Price/m²</h3>
        <div className="h-56">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data}>
              <CartesianGrid stroke="#e5e7eb" />
              <XAxis dataKey="month" />
              <YAxis tickFormatter={currency} />
              <Tooltip formatter={(v) => currency(v)} />
              <Line
                type="monotone"
                dataKey="avg_price"    // ✅ matches backend key
                stroke="#2563eb"
                dot={false}
                strokeWidth={2}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Min / Median / Max */}
      <div className="bg-white rounded-lg shadow p-4">
        <h3 className="text-sm font-semibold mb-2">Min/Median/Max</h3>
        <div className="h-56">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data}>
              <CartesianGrid stroke="#e5e7eb" />
              <XAxis dataKey="month" />
              <YAxis tickFormatter={currency} />
              <Tooltip formatter={(v) => currency(v)} />
              <Line
                type="monotone"
                dataKey="min_price"    // ✅ was "min" before
                stroke="#16a34a"
                dot={false}
                strokeWidth={2}
              />
              <Line
                type="monotone"
                dataKey="median_price" // ✅ was "median" before
                stroke="#f59e0b"
                dot={false}
                strokeWidth={2}
              />
              <Line
                type="monotone"
                dataKey="max_price"    // ✅ was "max" before
                stroke="#dc2626"
                dot={false}
                strokeWidth={2}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Total Listings */}
      <div className="bg-white rounded-lg shadow p-4">
        <h3 className="text-sm font-semibold mb-2">Total Listings</h3>
        <div className="h-56">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data}>
              <CartesianGrid stroke="#e5e7eb" />
              <XAxis dataKey="month" />
              <YAxis tickFormatter={integer} />
              <Tooltip formatter={(v) => integer(v)} />
              <Bar
                dataKey="listings"     // ✅ was "count" before
                fill="#3b82f6"
                radius={[4, 4, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
