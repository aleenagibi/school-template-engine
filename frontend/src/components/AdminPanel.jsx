    import { useState } from "react";
import API from "../api";

function AdminPanel() {
  const [loading, setLoading] =
    useState(false);

  const [message, setMessage] =
    useState("");

const handleScan = async () => {
  console.log("Scan clicked");

  try {
    const res = await API.post(
      "/scan",
      {},
      {
        headers: {
          "x-admin-key":
            "entab-admin-secret"
        }
      }
    );

    console.log("Scan response:", res.data);
  } catch (error) {
    console.log("Scan error:", error);
  }
};
  return (
    <div className="admin-panel">
      <button
        className="scan-btn"
        onClick={handleScan}
        disabled={loading}
      >
        {loading
          ? "Scanning..."
          : "Scan Templates"}
      </button>

      {message && (
        <p className="scan-status">
          {message}
        </p>
      )}
    </div>
  );
}

export default AdminPanel;