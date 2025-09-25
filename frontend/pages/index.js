import Layout from "../components/Layout";
import Graphs from "../components/Graphs";
import PropertyCard from "../components/PropertyCard";
import Filters from "../components/Filters";
import api from "../lib/api";
import { useEffect, useState, useMemo } from "react";

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

      // Filter out listings marked "Interesting: No"
      const filtered = (res.data || []).filter((p) => {
        const ann = p.annotations?.[0];
        return !(ann && ann.interesting === "No");
      });
      setProperties(filtered);

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
        merged[r.month] = {
          ...merged[r.month],
          min: r.min_price ?? null,
          median: r.median_price ?? null,
          max: r.max_price ?? null,
        };
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
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filters]);

  const handleAnnotationChange = (propertyId, updatedAnnotation) => {
    setProperties((prev) => {
      const next = prev.map((p) => {
        if (p.id !== propertyId) return p;
        const anns = p.annotations && p.annotations.length ? [updatedAnnotation] : [updatedAnnotation];
        return { ...p, annotations: anns };
      });
      // Remove it if marked Interesting "No"
      return next.filter((p) => !(p.annotations?.[0]?.interesting === "No"));
    });
  };

  return (
    <Layout sidebar={<Filters onChange={setFilters} />}>
      {/* Graphs */}
      <Graphs data={chartData} />

      {/* Property listings */}
      <div className="grid grid-cols-1 gap-4 mt-6">
        {properties.map((p) => (
          <PropertyCard key={p.id} property={p} onAnnotationChange={handleAnnotationChange} />
        ))}
      </div>
    </Layout>
  );
}
