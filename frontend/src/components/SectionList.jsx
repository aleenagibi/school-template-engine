import { useEffect, useState } from "react";
import API from "../api";

function SectionList({ school, onPreview, onAdd, selectedSections }) {
  const [sections, setSections] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!school) return;

    setLoading(true);
    setError(null);

    API.get(`/schools/${school}/sections`)
      .then((res) => {
        setSections(res.data.sections);
      })
      .catch((err) => {
        console.error("Failed to load sections:", err);
        setError("Could not load sections for this school.");
      })
      .finally(() => {
        setLoading(false);
      });
  }, [school]);

  const filteredSections = sections.filter((section) =>
    section.section_name.toLowerCase().includes(search.toLowerCase())
  );

  const isAdded = (sectionName) =>
    selectedSections?.some((s) => s.section_name === sectionName);

  return (
    <div className="section-list">
      <h2>Sections</h2>

      <input
        type="text"
        placeholder="Search sections..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="search-input"
      />

      {loading && <p className="status-text">Loading sections...</p>}

      {error && <p className="status-text status-error">{error}</p>}

      {!loading && !error && filteredSections.length === 0 && (
        <p className="status-text">
          {sections.length === 0
            ? "No sections found for this school."
            : "No sections match your search."}
        </p>
      )}

      {!loading &&
        filteredSections.map((section, index) => {
          const added = isAdded(section.section_name);

          return (
            <div key={index} className="section-card">
              <h3>
                {section.section_name}
                {added && <span className="added-badge">✓ Added</span>}
              </h3>

              <div className="section-actions">
                <button
                  className="preview-btn"
                  onClick={() =>
                    onPreview(school, section.section_name)
                  }
                >
                  Preview
                </button>

                <button
                  className="add-btn"
                  disabled={added}
                  onClick={() =>
                    onAdd({
                      school,
                      section_name: section.section_name,
                    })
                  }
                >
                  {added ? "Added" : "Add"}
                </button>
              </div>
            </div>
          );
        })}
    </div>
  );
}

export default SectionList;