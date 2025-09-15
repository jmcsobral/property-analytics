import Layout from "../components/Layout";
import Graphs from "../components/Graphs";
import PropertyCard from "../components/PropertyCard";
import Filters from "../components/Filters";
import api from "../lib/api";
import { useEffect, useState } from "react";

export default function Home() {
  const [properties, setProperties] = useState([]);
  const [chartData, setChartData] = useState([]);
  const [filters, setFilters] = useState({});

  const buildQuery = (filters) => {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, val]) => {
      if (val !== "" && val !== null && val !== false) {
        params.append(key, val);
      }
    });
    return params.toString();
  };

  const loadData = async (activeFilters = {}) => {
    try {
      const query = buildQuery(activeFilters);
      const res = await api.get(`/properties/?${query}`);
      setProperties(res.data);

      const [avg, dist, count] = await Promise.all([
        api.get(`/analytics/avg_price_per_m2?${query}`),
        api.get(`/analytics/price_distribution?${query}`),
        api.get(`/analytics/listings_per_month?${query}`),
      ]);

      const merged = {};
      avg.data.forEach((r) => {
        merged[r.month] = { month: r.month, avg_price: r.avg_price };
      });
      dist.data.forEach((r) => {
        merged[r.month] = { ...merged[r.month], ...r };
      });
      count.data.forEach((r) => {
        merged[r.month] = { ...merged[r.month], count: r.count };
      });
      setChartData(Object.values(merged));
    } catch (err) {
      console.error("Error loading data:", err);
    }
  };

  useEffect(() => {
    loadData(filters);
  }, [filters]);

  return (
    <Layout sidebar={<Filters onChange={setFilters} />}>
      {/* Graphs */}
      <Graphs data={chartData} />

      {/* Property listings */}
      <div className="grid grid-cols-1 gap-4 mt-6">
        {properties.map((p) => (
          <PropertyCard key={p.id} property={p} />
        ))}
      </div>
    </Layout>
  );
}
