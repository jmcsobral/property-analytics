import { useState } from "react";
import api from "../lib/api";

export default function PropertyCard({ property, onAnnotationChange }) {
  const latest = property.snapshots?.[property.snapshots.length - 1] || {};
  const ann = property.annotations?.[0] || {}; // we keep one row per property

  const [reviewed, setReviewed] = useState(!!ann.reviewed);
  const [contacted, setContacted] = useState(!!ann.contacted);
  const [interesting, setInteresting] = useState(ann.interesting ?? "");
  const [notes, setNotes] = useState(ann.notes ?? "");
  const [saving, setSaving] = useState(false);

  const saveAnnotation = async (patch) => {
    setSaving(true);
    try {
      const payload = {
        reviewed,
        contacted,
        notes,
        interesting,
        ...patch,
      };
      const res = await api.post(`/annotations/${property.id}`, payload);
      if (onAnnotationChange) onAnnotationChange(property.id, res.data);
    } catch (e) {
      console.error("Failed saving annotation:", e);
      alert("Failed to save annotation");
    } finally {
      setSaving(false);
    }
  };

  const handleInterestingChange = async (val) => {
    setInteresting(val);
    // Save immediately
    await saveAnnotation({ interesting: val });
  };

  const handleReviewedToggle = async (val) => {
    setReviewed(val);
    await saveAnnotation({ reviewed: val });
  };

  const handleContactedToggle = async (val) => {
    setContacted(val);
    await saveAnnotation({ contacted: val });
  };

  const handleNotesBlur = async () => {
    await saveAnnotation({});
  };

  return (
    <div className="bg-white rounded-lg shadow p-4">
      <div className="flex items-start gap-4">
        <img
          src={latest.image_url || "/no-image.png"}
          alt={property.title || "Property"}
          className="w-24 h-24 object-cover rounded"
          onError={(e) => {
            e.currentTarget.src = "/no-image.png";
          }}
        />
        <div className="flex-1">
          <a
            href={property.url || (latest.raw_json ? JSON.parse(latest.raw_json).href : "#")}
            target="_blank"
            rel="noreferrer"
            className="text-blue-600 font-medium hover:underline"
          >
            {property.title || `Property ${property.property_id}`}
          </a>
          <div className="text-sm text-gray-600 mt-1">
            {latest.district || "-"} / {latest.city || "-"} / {latest.zone || "-"}
          </div>
          <div className="text-sm mt-1">
            <span className="font-medium">Price:</span> {latest.price ?? "-"} &nbsp;|&nbsp;
            <span className="font-medium">€/m²:</span> {latest.price_per_m2 ?? "-"} &nbsp;|&nbsp;
            <span className="font-medium">Area:</span> {property.area ?? "-"} m² &nbsp;|&nbsp;
            <span className="font-medium">Typology:</span> {property.typology ?? "-"}
          </div>

          {/* Annotation controls */}
          <div className="mt-3 grid grid-cols-1 md:grid-cols-4 gap-2 items-center">
            <label className="inline-flex items-center gap-2">
              <input
                type="checkbox"
                checked={reviewed}
                onChange={(e) => handleReviewedToggle(e.target.checked)}
              />
              <span>Reviewed</span>
            </label>

            <label className="inline-flex items-center gap-2">
              <input
                type="checkbox"
                checked={contacted}
                onChange={(e) => handleContactedToggle(e.target.checked)}
              />
              <span>Contacted</span>
            </label>

            <label className="inline-flex items-center gap-2">
              <span>Interesting</span>
              <select
                className="border rounded px-2 py-1"
                value={interesting || ""}
                onChange={(e) => handleInterestingChange(e.target.value)}
              >
                <option value="">—</option>
                <option value="Yes">Yes</option>
                <option value="No">No</option>
              </select>
              {saving && <span className="text-xs text-gray-400">saving…</span>}
            </label>

            <input
              className="border rounded px-2 py-1"
              placeholder="Notes…"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              onBlur={handleNotesBlur}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
