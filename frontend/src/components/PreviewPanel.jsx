function PreviewPanel({ preview }) {
  if (!preview) return null;

  return (
    <div>
      <h2>Section Preview</h2>

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