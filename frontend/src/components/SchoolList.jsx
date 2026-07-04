import { useEffect, useState } from "react";
import API from "../api";

function SchoolList({
  onSelect,
  selectedSchool
}) {
  const [schools, setSchools] =
    useState([]);

  const [search, setSearch] =
    useState("");

  useEffect(() => {
    API.get("/schools").then((res) => {
      setSchools(res.data);
    });
  }, []);

  const filteredSchools =
    schools.filter((school) =>
      school
        .toLowerCase()
        .includes(search.toLowerCase())
    );

  return (
    <div className="school-list">
      <h2>Schools</h2>

      <input
        type="text"
        placeholder="Search schools..."
        value={search}
        onChange={(e) =>
          setSearch(e.target.value)
        }
        className="search-input"
      />

      {filteredSchools.map(
        (school, index) => (
         <button
  key={index}
  className={`school-btn ${
    selectedSchool === school
      ? "active-school"
      : ""
  }`}
  onClick={() => onSelect(school)}
>
            {school}
          </button>
        )
      )}
    </div>
  );
}

export default SchoolList;