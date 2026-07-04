import { useState } from "react";
import API from "../api";

function SearchBar({ onResults }) {
  const [query, setQuery] = useState("");

  const search = async () => {
    const res = await API.post(
      "/search",
      { query }
    );

    onResults(res.data);
  };

  return (
    <div className="search-bar">
      <input
        type="text"
        value={query}
        onChange={(e) =>
          setQuery(e.target.value)
        }
        placeholder="Search section..."
      />

      <button className="search-btn" onClick={search}>
        Search
      </button>
    </div>
  );
}

export default SearchBar;