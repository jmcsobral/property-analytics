export default function PropertyCard({ property }) {
  // pick the latest snapshot by highest snapshot_id
  const snapshots = Array.isArray(property.snapshots) ? property.snapshots : [];
  const latestSnap = snapshots.reduce((best, cur) => {
    if (!best) return cur;
    return (cur.snapshot_id || 0) > (best.snapshot_id || 0) ? cur : best;
  }, null);

  const title = property.title || latestSnap?.address || "Untitled";
  const url = property.url || "#";

  const imgUrl =
    latestSnap?.image_url && typeof latestSnap.image_url === "string" && latestSnap.image_url.trim().length
      ? latestSnap.image_url
      : "https://via.placeholder.com/320x200?text=No+Image";

  const price = latestSnap?.price;
  const ppm2 = latestSnap?.price_per_m2;
  const area = property.area;
  const typology = latestSnap?.typology || property.typology;
  const agency = latestSnap?.agency;

  const district = latestSnap?.district;
  const city = latestSnap?.city;
  const zone = latestSnap?.zone;

  const fmt = new Intl.NumberFormat("en-PT", { maximumFractionDigits: 0 });

  return (
    <div className="bg-white rounded-lg shadow p-4 flex gap-4">
      <div className="w-40 h-28 flex-none overflow-hidden rounded-md bg-gray-100">
        {/* plain <img> to avoid Next.js domain config hassles */}
        <img
          src={imgUrl}
          alt={title}
          className="w-full h-full object-cover object-center"
          loading="lazy"
        />
      </div>

      <div className="flex-1">
        <div className="flex items-start justify-between">
          <a
            href={url}
            className="text-base font-semibold hover:underline"
            target="_blank"
            rel="noreferrer"
          >
            {title}
          </a>
          {agency ? <span className="text-xs bg-gray-100 px-2 py-1 rounded">{agency}</span> : null}
        </div>

        <div className="text-sm text-gray-600 mt-1">
          {[district, city, zone].filter(Boolean).join(" • ")}
        </div>

        <div className="flex flex-wrap items-center gap-4 mt-2 text-sm">
          {typeof price === "number" ? (
            <div>
              <span className="font-semibold">€{fmt.format(price)}</span>
              {typeof ppm2 === "number" ? <span className="text-gray-500"> &nbsp;({fmt.format(ppm2)} €/m²)</span> : null}
            </div>
          ) : (
            <div className="text-gray-500">Price on request</div>
          )}

          {typeof area === "number" ? (
            <div className="text-gray-700">{fmt.format(area)} m²</div>
          ) : null}

          {typology ? <div className="text-gray-700">{typology}</div> : null}
        </div>

        {latestSnap?.tags ? (
          <div className="text-xs text-gray-500 mt-2 truncate">Tags: {latestSnap.tags}</div>
        ) : null}
      </div>
    </div>
  );
}
