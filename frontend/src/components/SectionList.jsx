import { useEffect, useState } from "react";
import API from "../api";

function SectionList({
  school,
  onPreview,
  onAdd
}) {
  const [sections, setSections] =
    useState([]);

  const [search, setSearch] =
    useState("");

  useEffect(() => {
    if (!school) return;

    API.get(`/schools/${school}/sections`)
      .then((res) => {
        setSections(res.data.sections);
      });
  }, [school]);

  const filteredSections =
    sections.filter((section) =>
      section.section_name
        .toLowerCase()
        .includes(search.toLowerCase())
    );

  return (
    <div className="section-list">
      <h2>Sections</h2>

      <input
        type="text"
        placeholder="Search sections..."
        value={search}
        onChange={(e) =>
          setSearch(e.target.value)
        }
        className="search-input"
      />

      {filteredSections.map(
        (section, index) => (
          <div
            key={index}
            className="section-card"
          >
            <h3>
              {section.section_name}
            </h3>

            <div className="section-actions">
              <button
                className="preview-btn"
                onClick={() =>
                  onPreview(
                    school,
                    section.section_name
                  )
                }
              >
                Preview
              </button>

              <button
                className="add-btn"
                onClick={() =>
                  onAdd({
                    school,
                    section_name:
                      section.section_name
                  })
                }
              >
                Add
              </button>
            </div>
          </div>
        )
      )}
    </div>
  );
}

export default SectionList;