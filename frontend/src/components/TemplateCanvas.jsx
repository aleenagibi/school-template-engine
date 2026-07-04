function TemplateCanvas({
  selectedSections,
  setSelectedSections
}) {
  const moveUp = (index) => {
    if (index === 0) return;

    const updated = [...selectedSections];

    [updated[index - 1], updated[index]] = [
      updated[index],
      updated[index - 1]
    ];

    setSelectedSections(updated);
  };

  const moveDown = (index) => {
    if (
      index ===
      selectedSections.length - 1
    )
      return;

    const updated = [...selectedSections];

    [updated[index + 1], updated[index]] = [
      updated[index],
      updated[index + 1]
    ];

    setSelectedSections(updated);
  };

  const removeSection = (indexToRemove) => {
    setSelectedSections((prev) =>
      prev.filter(
        (_, index) =>
          index !== indexToRemove
      )
    );
  };

  return (
    <div className="builder">
      <h2>Website Structure</h2>

      <div className="builder-canvas">
        {selectedSections.length === 0 ? (
          <div className="empty-state">
            Add sections to build template
          </div>
        ) : (
          selectedSections.map(
            (section, index) => (
              <div
                key={index}
                className="template-block"
              >
                <div className="template-block-top">
                  <div>
                    <h4>
                      {section.section_name}
                    </h4>
                    <p>{section.school}</p>
                  </div>

                  <button
                    className="remove-section-btn"
                    onClick={() =>
                      removeSection(index)
                    }
                  >
                    ×
                  </button>
                </div>

                <div className="template-actions">
                  <button
                    disabled={index === 0}
                    onClick={() =>
                      moveUp(index)
                    }
                  >
                    ↑
                  </button>

                  <button
                    disabled={
                      index ===
                      selectedSections.length -
                        1
                    }
                    onClick={() =>
                      moveDown(index)
                    }
                  >
                    ↓
                  </button>
                </div>
              </div>
            )
          )
        )}
      </div>
    </div>
  );
}

export default TemplateCanvas;