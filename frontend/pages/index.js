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

  const buildQuery = (f) => {
    const params = new URLSearchParams();
    Object.entries(f).forEach(([key, val]) => {
      if (val === undefined || val === null || val === "" ) return;

      // arrays (e.g., multiple typology)
      if (Array.isArray(val)) {
        val.forEach((v) => {
          if (v !== null && v !== "") params.append(key, v);
        });
      } else {
        // include zeros/false if explicitly set
        params.append(key, val);
      }
    });
    return params.toString();
  };

  const loadData = async (activeFilters = {}) => {
    try {
      const query = buildQuery(activeFilters);

      const propsRes = await api.get(`/properties/?${query}`);
      setProperties(propsRes.data || []);

      const [avg, dist, listingsRes] = await Promise.all([
        api.get(`/analytics/avg_price_per_m2?${query}`),
        api.get(`/analytics/price_distribution?${query}`),
        api.get(`/analytics/listings_per_month?${query}`),
      ]);

      const merged = {};
      (avg.data || []).forEach((r) => {
        merged[r.month] = { month: r.month, avg_price: r.avg_price };
      });
      (dist.data || []).forEach((r) => {
        merged[r.month] = { ...(merged[r.month] || { month: r.month }), ...r };
      });
      (listingsRes.data || []).forEach((r) => {
        merged[r.month] = { ...(merged[r.month] || { month: r.month }), listings: r.listings };
      });

      setChartData(Object.values(merged).sort((a,b) => a.month.localeCompare(b.month)));
    } catch (err) {
      console.error("Error loading data:", err);
    }
  };

  useEffect(() => {
    loadData(filters);
  }, [filters]);

  return (
    <Layout sidebar={<Filters onChange={setFilters} />}>
      <Graphs data={chartData} />

      <div className="grid grid-cols-1 gap-4 mt-6">
        {properties.map((p) => (
          <PropertyCard key={p.id} property={p} />
        ))}
      </div>
    </Layout>
  );
}
