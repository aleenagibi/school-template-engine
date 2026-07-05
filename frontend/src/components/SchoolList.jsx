import { useEffect, useState } from "react";
import API from "../api";

function SchoolList({ onSelect, selectedSchool }) {
  const [schools, setSchools] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);

    API.get("/schools")
      .then((res) => {
        setSchools(res.data);
      })
      .catch((err) => {
        console.error("Failed to load schools:", err);
        setError("Could not load schools. Is the backend running?");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  const filteredSchools = schools.filter((school) =>
    school.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="school-list">
      <h2>Schools</h2>

      <input
        type="text"
        placeholder="Search schools..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="search-input"
      />

      {loading && <p className="status-text">Loading schools...</p>}

      {error && <p className="status-text status-error">{error}</p>}

      {!loading && !error && filteredSchools.length === 0 && (
        <p className="status-text">
          {schools.length === 0
            ? "No schools found. Try running a scan."
            : "No schools match your search."}
        </p>
      )}

      {!loading &&
        filteredSchools.map((school, index) => (
          <button
            key={index}
            className={`school-btn ${
              selectedSchool === school ? "active-school" : ""
            }`}
            onClick={() => onSelect(school)}
          >
            {school}
          </button>
        ))}
    </div>
  );
}

export default SchoolList;