import { useState } from "react";
import API from "../api";

function AssemblePanel({ selected }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const assemble = async () => {
    setLoading(true);
    setError(null);

    try {
      const res = await API.post("/assemble", selected);

      const downloadPath = res.data.download.replace(/^\/+/, "");

      window.open(`http://127.0.0.1:8000/${downloadPath}`);
    } catch (err) {
      console.error("Failed to assemble export:", err);
      setError("Export failed. Check that the backend is running and try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="assemble-panel">
      <div>
        <p>Total Sections: {selected.length}</p>
        {error && <p className="status-text status-error">{error}</p>}
      </div>

      <button
        className="assemble-btn"
        onClick={assemble}
        disabled={selected.length === 0 || loading}
      >
        {loading ? "Assembling..." : "Assemble & Download"}
      </button>
    </div>
  );
}

export default AssemblePanel;