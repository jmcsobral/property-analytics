import { useEffect, useMemo, useState } from "react";
import api from "../lib/api";

export default function Filters({ onChange }) {
  // ---- dropdown options ----
  const [options, setOptions] = useState({
    districts: [],
    cities: [],
    zones: [],
    typologies: [],
    agencies: [],
  });

  // ---- UI state (local) ----
  const [district, setDistrict] = useState("");
  const [city, setCity] = useState("");
  const [zone, setZone] = useState("");
  const [agency, setAgency] = useState("");

  // Only T* entries for the threshold control
  const tTypologies = useMemo(
    () => options.typologies.filter((t) => t && t.toUpperCase().startsWith("T")),
    [options.typologies]
  );
  const [minTypology, setMinTypology] = useState(""); // e.g., "T2"

  // Ranges
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [minPriceM2, setMinPriceM2] = useState("");
  const [maxPriceM2, setMaxPriceM2] = useState("");
  const [minArea, setMinArea] = useState("");
  const [maxArea, setMaxArea] = useState("");

  // Booleans (only send when true)
  const [parking, setParking] = useState(false);
  const [elevator, setElevator] = useState(false);
  const [newConstruction, setNewConstruction] = useState(false);
  const [rented, setRented] = useState(false);
  const [trespasse, setTrespasse] = useState(false);

  // Search
  const [searchAddress, setSearchAddress] = useState("");
  const [searchTags, setSearchTags] = useState("");

  // ---- helpers ----
  const parseNum = (v) => {
    if (v === "" || v === null || v === undefined) return undefined;
    const n = Number(v);
    return Number.isFinite(n) ? n : undefined;
  };

  const parseTNumber = (t) => {
    if (!t || !t.toUpperCase().startsWith("T")) return undefined;
    const num = parseInt(t.slice(1), 10);
    return Number.isFinite(num) ? num : undefined;
    // fallback undefined if non numeric
  };

  // Build the typology list from threshold (e.g., pick all >= T2)
  const computedTypologyList = useMemo(() => {
    const minNum = parseTNumber(minTypology);
    if (minNum === undefined) return undefined; // no filter
    const eligible = tTypologies.filter((t) => {
      const n = parseTNumber(t);
      return n !== undefined && n >= minNum;
    });
    return eligible.length ? eligible : undefined;
  }, [minTypology, tTypologies]);

  // ---- load options ----
  // Initial options
  useEffect(() => {
    const loadInitial = async () => {
      const res = await api.get(`/properties/options`);
      setOptions(res.data || { districts: [], cities: [], zones: [], typologies: [], agencies: [] });
    };
    loadInitial();
  }, []);

  // When district changes, refresh cities & zones
  useEffect(() => {
    const run = async () => {
      const params = new URLSearchParams();
      if (district) params.append("district", district);
      const res = await api.get(`/properties/options?${params.toString()}`);
      setOptions((prev) => ({
        ...prev,
        cities: res.data.cities || [],
        zones: res.data.zones || [],
      }));
    };
    // clear dependent values
    setCity("");
    setZone("");
    if (district) run();
    else {
      // if district cleared, reload full city/zone lists
      (async () => {
        const res = await api.get(`/properties/options`);
        setOptions((prev) => ({
          ...prev,
          cities: res.data.cities || [],
          zones: res.data.zones || [],
        }));
      })();
    }
  }, [district]);

  // When city changes, refresh zones
  useEffect(() => {
    const run = async () => {
      const params = new URLSearchParams();
      if (district) params.append("district", district);
      if (city) params.append("city", city);
      const res = await api.get(`/properties/options?${params.toString()}`);
      setOptions((prev) => ({
        ...prev,
        zones: res.data.zones || [],
      }));
    };
    setZone("");
    if (city || district) run();
  }, [city, district]);

  // ---- push filters to parent on any change ----
  useEffect(() => {
    const filters = {
      // categorical
      district: district || undefined,
      city: city || undefined,
      zone: zone || undefined,
      agency: agency || undefined,

      // typology list (array of strings), only if present
      typology: computedTypologyList,

      // ranges
      min_price: parseNum(minPrice),
      max_price: parseNum(maxPrice),
      min_price_per_m2: parseNum(minPriceM2),
      max_price_per_m2: parseNum(maxPriceM2),
      min_area: parseNum(minArea),
      max_area: parseNum(maxArea),

      // search (pass only if non-empty)
      search_address: searchAddress?.trim() ? searchAddress.trim() : undefined,
      search_tags: searchTags?.trim() ? searchTags.trim() : undefined,
    };

    // booleans: send ONLY when true (else omit)
    if (parking) filters.parking = true;
    if (elevator) filters.elevator = true;
    if (newConstruction) filters.new_construction = true;
    if (rented) filters.rented = true;
    if (trespasse) filters.trespasse = true;

    onChange(filters);
  }, [
    district,
    city,
    zone,
    agency,
    minTypology,
    minPrice,
    maxPrice,
    minPriceM2,
    maxPriceM2,
    minArea,
    maxArea,
    searchAddress,
    searchTags,
    parking,
    elevator,
    newConstruction,
    rented,
    trespasse,
    computedTypologyList,
    onChange,
  ]);

  const reset = () => {
    setDistrict("");
    setCity("");
    setZone("");
    setAgency("");
    setMinTypology("");

    setMinPrice("");
    setMaxPrice("");
    setMinPriceM2("");
    setMaxPriceM2("");
    setMinArea("");
    setMaxArea("");

    setSearchAddress("");
    setSearchTags("");

    setParking(false);
    setElevator(false);
    setNewConstruction(false);
    setRented(false);
    setTrespasse(false);
  };

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-semibold">Filters</h2>

      {/* Location */}
      <div>
        <label className="block text-sm font-medium mb-1">District</label>
        <select
          className="w-full border rounded p-2"
          value={district}
          onChange={(e) => setDistrict(e.target.value)}
        >
          <option value="">Any</option>
          {options.districts.map((d) => (
            <option key={d} value={d}>
              {d}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium mb-1">City</label>
        <select
          className="w-full border rounded p-2"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          disabled={!options.cities.length}
        >
          <option value="">Any</option>
          {options.cities.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium mb-1">Zone</label>
        <select
          className="w-full border rounded p-2"
          value={zone}
          onChange={(e) => setZone(e.target.value)}
          disabled={!options.zones.length}
        >
          <option value="">Any</option>
          {options.zones.map((z) => (
            <option key={z} value={z}>
              {z}
            </option>
          ))}
        </select>
      </div>

      {/* Agency */}
      <div>
        <label className="block text-sm font-medium mb-1">Agency</label>
        <select
          className="w-full border rounded p-2"
          value={agency}
          onChange={(e) => setAgency(e.target.value)}
        >
          <option value="">Any</option>
          {options.agencies.map((a) => (
            <option key={a} value={a}>
              {a}
            </option>
          ))}
        </select>
      </div>

      {/* Typology threshold */}
      <div>
        <label className="block text-sm font-medium mb-1">Minimum Typology (T*)</label>
        <select
          className="w-full border rounded p-2"
          value={minTypology}
          onChange={(e) => setMinTypology(e.target.value)}
        >
          <option value="">Any</option>
          {tTypologies.map((t) => (
            <option key={t} value={t}>
              {t}
            </option>
          ))}
        </select>
        <p className="text-xs text-gray-500 mt-1">
          Selecting e.g. <b>T2</b> automatically includes T2, T3, T4, …
        </p>
      </div>

      {/* Price */}
      <div>
        <label className="block text-sm font-medium">Price (€)</label>
        <div className="grid grid-cols-2 gap-2 mt-1">
          <input
            type="number"
            className="border rounded p-2"
            placeholder="Min"
            value={minPrice}
            onChange={(e) => setMinPrice(e.target.value)}
          />
          <input
            type="number"
            className="border rounded p-2"
            placeholder="Max"
            value={maxPrice}
            onChange={(e) => setMaxPrice(e.target.value)}
          />
        </div>
      </div>

      {/* Price per m² */}
      <div>
        <label className="block text-sm font-medium">Price / m² (€)</label>
        <div className="grid grid-cols-2 gap-2 mt-1">
          <input
            type="number"
            className="border rounded p-2"
            placeholder="Min"
            value={minPriceM2}
            onChange={(e) => setMinPriceM2(e.target.value)}
          />
          <input
            type="number"
            className="border rounded p-2"
            placeholder="Max"
            value={maxPriceM2}
            onChange={(e) => setMaxPriceM2(e.target.value)}
          />
        </div>
      </div>

      {/* Area */}
      <div>
        <label className="block text-sm font-medium">Area (m²)</label>
        <div className="grid grid-cols-2 gap-2 mt-1">
          <input
            type="number"
            className="border rounded p-2"
            placeholder="Min"
            value={minArea}
            onChange={(e) => setMinArea(e.target.value)}
          />
          <input
            type="number"
            className="border rounded p-2"
            placeholder="Max"
            value={maxArea}
            onChange={(e) => setMaxArea(e.target.value)}
          />
        </div>
      </div>

      {/* Search */}
      <div>
        <label className="block text-sm font-medium">Search Address</label>
        <input
          type="text"
          className="w-full border rounded p-2 mt-1"
          placeholder="e.g., Rua ..."
          value={searchAddress}
          onChange={(e) => setSearchAddress(e.target.value)}
        />
      </div>

      <div>
        <label className="block text-sm font-medium">Search Tags</label>
        <input
          type="text"
          className="w-full border rounded p-2 mt-1"
          placeholder="e.g., 'oportunidade'"
          value={searchTags}
          onChange={(e) => setSearchTags(e.target.value)}
        />
      </div>

      {/* Booleans */}
      <div className="grid grid-cols-2 gap-2">
        <label className="inline-flex items-center space-x-2">
          <input type="checkbox" checked={parking} onChange={(e) => setParking(e.target.checked)} />
          <span className="text-sm">Parking</span>
        </label>
        <label className="inline-flex items-center space-x-2">
          <input type="checkbox" checked={elevator} onChange={(e) => setElevator(e.target.checked)} />
          <span className="text-sm">Elevator</span>
        </label>
        <label className="inline-flex items-center space-x-2">
          <input
            type="checkbox"
            checked={newConstruction}
            onChange={(e) => setNewConstruction(e.target.checked)}
          />
          <span className="text-sm">New Construction</span>
        </label>
        <label className="inline-flex items-center space-x-2">
          <input type="checkbox" checked={rented} onChange={(e) => setRented(e.target.checked)} />
          <span className="text-sm">Rented</span>
        </label>
        <label className="inline-flex items-center space-x-2">
          <input type="checkbox" checked={trespasse} onChange={(e) => setTrespasse(e.target.checked)} />
          <span className="text-sm">Trespasse</span>
        </label>
      </div>

      {/* Actions */}
      <div className="flex gap-2 pt-2">
        <button
          type="button"
          className="px-3 py-2 rounded bg-gray-100 hover:bg-gray-200 text-sm"
          onClick={reset}
        >
          Reset
        </button>
      </div>
    </div>
  );
}
