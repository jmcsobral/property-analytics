import { useState } from "react";
import api from "../lib/api";

export default function PropertyCard({ property }) {
  // load first annotation if exists, otherwise empty
  const [annotations, setAnnotations] = useState(
    property.annotations && property.annotations.length > 0
      ? property.annotations[0]
      : { reviewed: false, interesting: "maybe", contacted: false, notes: "" }
  );

  // Save annotation immediately when changed
  const updateAnnotation = async (field, value) => {
    const updated = { ...annotations, [field]: value };
    setAnnotations(updated);
    try {
      const res = await api.post(`/annotations/${property.id}`, updated);
      setAnnotations(res.data); // keep backend state
    } catch (err) {
      console.error("Error saving annotation:", err);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-4 flex space-x-4">
      <a href={property.url} target="_blank" rel="noreferrer">
        <img
          src={property.image_url || "https://via.placeholder.com/150"}
          alt=""
          className="w-32 h-24 object-cover rounded hover:opacity-80 transition"
        />
      </a>
      <div className="flex-1">
        <h3 className="font-semibold text-lg">{property.title}</h3>
        <p className="text-sm text-gray-500">
          {property.area} m² •{" "}
          {property.snapshots?.[0]?.price_per_m2 || "-"} €/m²
        </p>
        <p className="font-bold text-blue-600">
          {property.snapshots?.[0]?.price || "-"} €
        </p>

        {/* Annotation controls */}
        <div className="mt-3 grid grid-cols-2 gap-4 text-sm">
          <label className="flex items-center space-x-2">
            <input
              type="checkbox"
              checked={annotations.reviewed || false}
              onChange={(e) => updateAnnotation("reviewed", e.target.checked)}
            />
            <span>Reviewed</span>
          </label>

          <label className="flex items-center space-x-2">
            <span>Interesting:</span>
            <select
              className="border rounded p-1"
              value={annotations.interesting || "maybe"}
              onChange={(e) => updateAnnotation("interesting", e.target.value)}
            >
              <option value="yes">Yes</option>
              <option value="no">No</option>
              <option value="maybe">Maybe</option>
            </select>
          </label>

          <label className="flex items-center space-x-2">
            <input
              type="checkbox"
              checked={annotations.contacted || false}
              onChange={(e) => updateAnnotation("contacted", e.target.checked)}
            />
            <span>Contacted</span>
          </label>
        </div>

        <textarea
          className="w-full mt-3 border rounded p-2 text-sm"
          placeholder="Notes..."
          value={annotations.notes || ""}
          onChange={(e) => updateAnnotation("notes", e.target.value)}
        />
      </div>
    </div>
  );
}
