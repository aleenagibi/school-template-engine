function PreviewPanel({ preview, loading }) {
  if (loading) {
    return (
      <div>
        <h2>Section Preview</h2>
        <p className="status-text">Loading preview...</p>
      </div>
    );
  }

  if (!preview) return null;

  return (
    <div>
      <h2>
        Section Preview
        <span className="preview-context">
          {preview.school} — {preview.section_name}
        </span>
      </h2>

      <div className="preview-section">
        <h3>JSX</h3>
        <pre>{preview.jsx_code}</pre>
      </div>

      <div className="preview-section">
        <h3>CSS</h3>
        <pre>{preview.css_code}</pre>
      </div>
    </div>
  );
}

export default PreviewPanel;