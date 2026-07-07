import { useState } from "react";
import API from "../api";
import {
  scopeSection,
  buildCombinedFile,
  buildSeparateComponent,
  buildHomeFile,
  sanitizeComponentName,
  extractAllClasses,
  extractAllColors,
} from "../utils/mergeSections";

function CompiledPreviewPanel({ selected }) {
  const [built, setBuilt] = useState(null);
  const [showReference, setShowReference] = useState(false);
  const [loading, setLoading] = useState(false);
  const [exporting, setExporting] = useState(false);
  const [error, setError] = useState(null);

  const runCompile = async () => {
    setLoading(true);
    setError(null);

    try {
      const res = await API.post("/analyze", {
        selected_sections: selected.map((s) => ({
          school: s.school,
          section_name: s.section_name,
          mode: s.mode || "combine",
        })),
      });

      const rawSections = res.data.sections;
      const scoped = rawSections.map(scopeSection);

      const combineGroup = scoped.filter((s) => s.mode === "combine");
      const separateGroup = scoped.filter((s) => s.mode === "separate");

      let combined = null;
      if (combineGroup.length > 0) {
        combined = buildCombinedFile(combineGroup);
      }

      const usedNames = {};
      const separateFiles = separateGroup.map((section) => {
        const raw = section.component_file || section.section_name;
        const base = sanitizeComponentName(raw);
        const count = usedNames[base] || 0;
        usedNames[base] = count + 1;
        const name = count === 0 ? base : `${base}${count + 1}`;

        return {
          name,
          jsxCode: buildSeparateComponent(section, name),
          cssCode: section.css_code,
        };
      });

      const homeJsx =
        separateFiles.length > 0
          ? buildHomeFile(separateFiles.map((f) => f.name))
          : null;

      const allJsxForRef = scoped.map((s) => s.wrappedReturn).join("\n");
      const allCssForRef = scoped.map((s) => s.css_code).join("\n");

      setBuilt({
        combined,
        separateFiles,
        homeJsx,
        classes: extractAllClasses(allJsxForRef),
        colors: extractAllColors(allCssForRef),
      });
    } catch (err) {
      console.error("Compile failed:", err);
      setError(
        "Could not compile preview. This usually means one of the selected files has JSX Babel couldn't parse — check the browser console for details."
      );
    } finally {
      setLoading(false);
    }
  };

  const exportFinal = async () => {
    if (!built) return;

    setExporting(true);
    setError(null);

    try {
      const res = await API.post("/export", {
        combined: built.combined
          ? { jsx_code: built.combined.jsxCode, css_code: built.combined.cssCode }
          : null,
        separate_files: built.separateFiles.map((f) => ({
          name: f.name,
          jsx_code: f.jsxCode,
          css_code: f.cssCode,
        })),
        home_jsx: built.homeJsx,
      });

      const downloadPath = res.data.download.replace(/^\/+/, "");
      window.open(`${API.defaults.baseURL}/${downloadPath}`);
    } catch (err) {
      console.error("Export failed:", err);
      setError("Export failed. Check that the backend is running.");
    } finally {
      setExporting(false);
    }
  };

  if (selected.length === 0) return null;

  return (
    <div className="compiled-preview">
      <div className="compiled-preview-header">
        <h2>Compile &amp; Export</h2>
        <button className="preview-btn" onClick={runCompile} disabled={loading}>
          {loading ? "Compiling..." : "Compile Preview"}
        </button>
      </div>

      {error && <p className="status-text status-error">{error}</p>}

      {built && (
        <>
          {built.combined && (
            <div className="compiled-code-grid">
              <div className="preview-section">
                <h3>Combined JSX</h3>
                <pre>{built.combined.jsxCode}</pre>
              </div>
              <div className="preview-section">
                <h3>Combined CSS</h3>
                <pre>{built.combined.cssCode}</pre>
              </div>
            </div>
          )}

          {built.separateFiles.length > 0 && (
            <div className="separate-files-list">
              <h3>Separate Components ({built.separateFiles.length})</h3>
              {built.separateFiles.map((f) => (
                <details key={f.name} className="separate-file-block">
                  <summary>{f.name}.jsx</summary>
                  <pre>{f.jsxCode}</pre>
                </details>
              ))}
              {built.homeJsx && (
                <details className="separate-file-block">
                  <summary>Home.jsx</summary>
                  <pre>{built.homeJsx}</pre>
                </details>
              )}
            </div>
          )}

          <button
            className="reference-toggle"
            onClick={() => setShowReference((prev) => !prev)}
          >
            {showReference ? "▾" : "▸"} Classes &amp; Colors ({built.classes.length}, {built.colors.length})
          </button>

          {showReference && (
            <div className="edit-grid">
              <div>
                <h3>Classes ({built.classes.length})</h3>
                <div className="scroll-list">
                  {built.classes.map((cls) => (
                    <div key={cls} className="class-chip">
                      {cls}
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <h3>Colors ({built.colors.length})</h3>
                <div className="scroll-list">
                  {built.colors.map((color) => (
                    <div key={color} className="rename-row">
                      <span className="color-swatch" style={{ background: color }} />
                      <span className="rename-old">{color}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          <button className="assemble-btn" onClick={exportFinal} disabled={exporting}>
            {exporting ? "Exporting..." : "Export & Download"}
          </button>
        </>
      )}
    </div>
  );
}

export default CompiledPreviewPanel;