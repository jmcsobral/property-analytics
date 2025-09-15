import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import api from "../lib/api";

export default function Snapshots() {
  const [snapshots, setSnapshots] = useState([]);
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const loadSnapshots = async () => {
    try {
      const res = await api.get("/snapshots/");
      setSnapshots(res.data);
    } catch (err) {
      console.error("Error loading snapshots:", err);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return alert("Please select an Excel file first.");

    const formData = new FormData();
    formData.append("file", file);

    try {
      setUploading(true);
      await api.post("/snapshots/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setFile(null);
      loadSnapshots();
    } catch (err) {
      console.error("Upload failed:", err);
      alert("Upload failed. Check console for details.");
    } finally {
      setUploading(false);
    }
  };

  const deleteSnapshot = async (id) => {
    if (!confirm("Are you sure you want to delete this snapshot?")) return;
    try {
      await api.delete(`/snapshots/${id}`);
      loadSnapshots();
    } catch (err) {
      console.error("Error deleting snapshot:", err);
    }
  };

  useEffect(() => {
    loadSnapshots();
  }, []);

  return (
    <Layout>
      <div className="p-6 max-w-4xl mx-auto">
        <h1 className="text-2xl font-bold mb-6">Snapshots</h1>

        {/* Upload form */}
        <form
          onSubmit={handleUpload}
          className="mb-6 flex items-center space-x-4 bg-white p-4 rounded shadow"
        >
          <input
            type="file"
            accept=".xlsx"
            onChange={(e) => setFile(e.target.files[0])}
            className="border p-2 rounded w-full"
          />
          <button
            type="submit"
            disabled={uploading}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
          >
            {uploading ? "Uploading..." : "Upload Snapshot"}
          </button>
        </form>

        {/* Snapshot cards */}
        <div className="grid gap-4">
          {snapshots.map((s) => (
            <div
              key={s.id}
              className="bg-white shadow rounded p-4 flex items-center justify-between hover:shadow-md transition"
            >
              <div>
                <p className="text-sm text-gray-500">Snapshot ID: {s.id}</p>
                <p className="text-lg font-semibold text-gray-800">
                  {new Date(s.upload_date).toLocaleString()}
                </p>
                <p className="text-sm text-gray-600">
                  {s.property_count} properties
                </p>
              </div>
              <button
                onClick={() => deleteSnapshot(s.id)}
                className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
              >
                Delete
              </button>
            </div>
          ))}
          {snapshots.length === 0 && (
            <div className="text-center text-gray-500 bg-white p-6 rounded shadow">
              No snapshots uploaded yet.
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}
