import { useState } from "react";

export default function Filters({ onChange }) {
  const [filters, setFilters] = useState({
    address: "",
    tags: "",
    district: "",
    city: "",
    zone: "",
    typology: "",
    agency: "",
    parking: false,
    elevator: false,
    new_construction: false,
    rented: false,
    trespasse: false,
    min_price: "",
    max_price: "",
    min_price_m2: "",
    max_price_m2: "",
    min_area: "",
    max_area: "",
  });

  const updateFilter = (field, value) => {
    const updated = { ...filters, [field]: value };
    setFilters(updated);
    if (onChange) onChange(updated);
  };

  return (
    <div className="space-y-4 text-sm">
      {/* Text search */}
      <input
        type="text"
        placeholder="Search address..."
        className="w-full p-2 border rounded"
        value={filters.address}
        onChange={(e) => updateFilter("address", e.target.value)}
      />
      <input
        type="text"
        placeholder="Search tags..."
        className="w-full p-2 border rounded"
        value={filters.tags}
        onChange={(e) => updateFilter("tags", e.target.value)}
      />

      {/* Dropdowns */}
      <div>
        <label className="block text-xs text-gray-600">District</label>
        <select
          className="w-full border rounded p-2"
          value={filters.district}
          onChange={(e) => updateFilter("district", e.target.value)}
        >
          <option value="">All</option>
          <option value="Porto">Porto</option>
          <option value="Lisboa">Lisboa</option>
        </select>
      </div>

      <div>
        <label className="block text-xs text-gray-600">City</label>
        <input
          type="text"
          className="w-full border rounded p-2"
          value={filters.city}
          onChange={(e) => updateFilter("city", e.target.value)}
        />
      </div>

      <div>
        <label className="block text-xs text-gray-600">Zone</label>
        <input
          type="text"
          className="w-full border rounded p-2"
          value={filters.zone}
          onChange={(e) => updateFilter("zone", e.target.value)}
        />
      </div>

      <div>
        <label className="block text-xs text-gray-600">Typology</label>
        <input
          type="text"
          className="w-full border rounded p-2"
          value={filters.typology}
          onChange={(e) => updateFilter("typology", e.target.value)}
        />
      </div>

      <div>
        <label className="block text-xs text-gray-600">Agency</label>
        <input
          type="text"
          className="w-full border rounded p-2"
          value={filters.agency}
          onChange={(e) => updateFilter("agency", e.target.value)}
        />
      </div>

      {/* Checkboxes */}
      <div className="space-y-1">
        {[
          ["parking", "Parking"],
          ["elevator", "Elevator"],
          ["new_construction", "New Construction"],
          ["rented", "Rented"],
          ["trespasse", "Trespasse"],
        ].map(([field, label]) => (
          <label key={field} className="flex items-center space-x-2">
            <input
              type="checkbox"
              checked={filters[field]}
              onChange={(e) => updateFilter(field, e.target.checked)}
            />
            <span>{label}</span>
          </label>
        ))}
      </div>

      {/* Numeric ranges */}
      <div>
        <label className="block text-xs text-gray-600">Price (€)</label>
        <div className="flex space-x-2">
          <input
            type="number"
            placeholder="Min"
            className="w-1/2 p-2 border rounded"
            value={filters.min_price}
            onChange={(e) => updateFilter("min_price", e.target.value)}
          />
          <input
            type="number"
            placeholder="Max"
            className="w-1/2 p-2 border rounded"
            value={filters.max_price}
            onChange={(e) => updateFilter("max_price", e.target.value)}
          />
        </div>
      </div>

      <div>
        <label className="block text-xs text-gray-600">Price per m² (€)</label>
        <div className="flex space-x-2">
          <input
            type="number"
            placeholder="Min"
            className="w-1/2 p-2 border rounded"
            value={filters.min_price_m2}
            onChange={(e) => updateFilter("min_price_m2", e.target.value)}
          />
          <input
            type="number"
            placeholder="Max"
            className="w-1/2 p-2 border rounded"
            value={filters.max_price_m2}
            onChange={(e) => updateFilter("max_price_m2", e.target.value)}
          />
        </div>
      </div>

      <div>
        <label className="block text-xs text-gray-600">Area (m²)</label>
        <div className="flex space-x-2">
          <input
            type="number"
            placeholder="Min"
            className="w-1/2 p-2 border rounded"
            value={filters.min_area}
            onChange={(e) => updateFilter("min_area", e.target.value)}
          />
          <input
            type="number"
            placeholder="Max"
            className="w-1/2 p-2 border rounded"
            value={filters.max_area}
            onChange={(e) => updateFilter("max_area", e.target.value)}
          />
        </div>
      </div>
    </div>
  );
}
