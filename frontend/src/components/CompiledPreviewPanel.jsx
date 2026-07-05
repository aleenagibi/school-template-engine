import { useState } from "react";
import API from "../api";

function CompiledPreviewPanel({ selected }) {
  const [analysis, setAnalysis] = useState(null);
  const [colorRenames, setColorRenames] = useState({});
  const [classFilter, setClassFilter] = useState("");
  const [mode, setMode] = useState("combined");
  const [loading, setLoading] = useState(false);
  const [exporting, setExporting] = useState(false);
  const [error, setError] = useState(null);

  const runAnalyze = async () => {
    setLoading(true);
    setError(null);

    try {
      const res = await API.post("/analyze", {
        selected_sections: selected,
      });
      setAnalysis(res.data);
      setColorRenames({});
    } catch (err) {
      console.error("Analyze failed:", err);
      setError("Could not compile preview. Check that the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const applyRenames = async () => {
    if (!analysis) return;

    setLoading(true);
    setError(null);

    try {
      const res = await API.post("/analyze/rename", {
        css_code: analysis.combined_css,
        color_rename_map: colorRenames,
      });

      setAnalysis((prev) => ({
        ...prev,
        combined_css: res.data.css_code,
        colors: res.data.colors,
      }));
      setColorRenames({});
    } catch (err) {
      console.error("Rename failed:", err);
      setError("Could not apply color changes.");
    } finally {
      setLoading(false);
    }
  };

  const exportFinal = async () => {
    setExporting(true);
    setError(null);

    try {
      const res = await API.post("/assemble", {
        selected_sections: selected,
        mode,
        color_rename_map: colorRenames,
      });

      const downloadPath = res.data.download.replace(/^\/+/, "");
      window.open(`http://127.0.0.1:8000/${downloadPath}`);
    } catch (err) {
      console.error("Export failed:", err);
      setError("Export failed. Check that the backend is running.");
    } finally {
      setExporting(false);
    }
  };

  if (selected.length === 0) return null;

  const filteredClasses =
    analysis?.classes.filter((c) =>
      c.toLowerCase().includes(classFilter.toLowerCase())
    ) || [];

  return (
    <div className="compiled-preview">
      <div className="compiled-preview-header">
        <h2>Compile &amp; Export</h2>
        <button className="preview-btn" onClick={runAnalyze} disabled={loading}>
          {loading ? "Compiling..." : "Compile Preview"}
        </button>
      </div>

      {error && <p className="status-text status-error">{error}</p>}

      {analysis && (
        <>
          <div className="compiled-code-grid">
            <div className="preview-section">
              <h3>Compiled JSX</h3>
              <pre>{analysis.combined_jsx}</pre>
            </div>
            <div className="preview-section">
              <h3>Compiled CSS</h3>
              <pre>{analysis.combined_css}</pre>
            </div>
          </div>

          <div className="edit-grid">
            <div>
              <h3>Classes ({filteredClasses.length}/{analysis.classes.length})</h3>
              <input
                type="text"
                className="search-input"
                placeholder="Filter classes..."
                value={classFilter}
                onChange={(e) => setClassFilter(e.target.value)}
              />
              <div className="scroll-list">
                {filteredClasses.map((cls) => (
                  <div key={cls} className="class-chip">
                    {cls}
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h3>Colors ({analysis.colors.length})</h3>
              <div className="scroll-list">
                {analysis.colors.map((color) => (
                  <div key={color} className="rename-row">
                    <span className="color-swatch" style={{ background: color }} />
                    <span className="rename-old">{color}</span>
                    <input
                      type="text"
                      placeholder="new value..."
                      value={colorRenames[color] || ""}
                      onChange={(e) =>
                        setColorRenames((prev) => ({
                          ...prev,
                          [color]: e.target.value,
                        }))
                      }
                    />
                  </div>
                ))}
              </div>
            </div>
          </div>

          <button className="add-btn" onClick={applyRenames} disabled={loading}>
            Apply Color Changes
          </button>

          <div className="export-mode-row">
            <label>
              <input
                type="radio"
                name="mode"
                checked={mode === "combined"}
                onChange={() => setMode("combined")}
              />
              Single combined file
            </label>
            <label>
              <input
                type="radio"
                name="mode"
                checked={mode === "separate"}
                onChange={() => setMode("separate")}
              />
              Separate files + Home.jsx
            </label>
          </div>

          <button className="assemble-btn" onClick={exportFinal} disabled={exporting}>
            {exporting ? "Exporting..." : "Export & Download"}
          </button>
        </>
      )}
    </div>
  );
}

export default CompiledPreviewPanel;