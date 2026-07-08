import { useState, useEffect } from "react";
import API from "./api";
import SchoolList from "./components/SchoolList";
import SectionList from "./components/SectionList";
import PreviewPanel from "./components/PreviewPanel";
import CompiledPreviewPanel from "./components/CompiledPreviewPanel";
import TemplateCanvas from "./components/TemplateCanvas";
import ThemeToggle from "./components/ThemeToggle";
import Footer from "./components/Footer";
import { SpeedInsights } from "@vercel/speed-insights/react";
import "./App.css";

function App() {
  const [selectedSchool, setSelectedSchool] = useState(null);
  const [preview, setPreview] = useState(null);
  const [selectedSections, setSelectedSections] = useState([]);
  const [activeTab, setActiveTab] = useState("schools");
  const [previewLoading, setPreviewLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);

  const [theme, setTheme] = useState(
    () => localStorage.getItem("stie-theme") || "dark"
  );

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("stie-theme", theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === "dark" ? "light" : "dark"));
  };

  const handleSchoolSelect = (school) => {
    setSelectedSchool(school);
    setActiveTab("sections");
  };

  const loadPreview = async (school, section_name) => {
    setPreviewLoading(true);
    setErrorMessage(null);

    try {
      const res = await API.get(`/preview/${school}/${section_name}`);
      setPreview(res.data);
    } catch (err) {
      console.error("Failed to load preview:", err);
      setPreview(null);
      setErrorMessage(
        `Could not load preview for "${section_name}". It may no longer exist — try re-scanning.`
      );
    } finally {
      setPreviewLoading(false);
    }
  };

const addSection = (section) => {
  setSelectedSections((prev) => {
    const exists = prev.find((s) => s.section_name === section.section_name);
    if (exists) return prev;

    const defaultMode = section.component_file ? "separate" : "combine";
    return [...prev, { ...section, mode: defaultMode }];
  });
};

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="app-header-title">
          <span className="app-header-mark">STIE</span>
          <span className="app-header-name">
            School Template Intelligence System
          </span>
        </div>

        <ThemeToggle theme={theme} onToggle={toggleTheme} />
      </header>

      {errorMessage && (
        <div className="error-banner">
          {errorMessage}
          <button
            className="error-dismiss"
            onClick={() => setErrorMessage(null)}
          >
            ×
          </button>
        </div>
      )}

      <div className="workspace">
        <div className="left-panel">
          <div className="tabs">
            <button
              className={activeTab === "schools" ? "tab active" : "tab"}
              onClick={() => setActiveTab("schools")}
            >
              Schools
            </button>

            <button
              className={activeTab === "sections" ? "tab active" : "tab"}
              onClick={() => setActiveTab("sections")}
              disabled={!selectedSchool}
            >
              Sections
            </button>
          </div>

          {activeTab === "schools" && (
            <SchoolList
              onSelect={handleSchoolSelect}
              selectedSchool={selectedSchool}
            />
          )}

          {activeTab === "sections" && (
            <SectionList
              school={selectedSchool}
              onPreview={loadPreview}
              onAdd={addSection}
              selectedSections={selectedSections}
            />
          )}
        </div>

        <TemplateCanvas
          selectedSections={selectedSections}
          setSelectedSections={setSelectedSections}
        />

        <div className="right-panel">
          <PreviewPanel preview={preview} loading={previewLoading} />
        </div>
      </div>

<div className="bottom-panel">
  <CompiledPreviewPanel selected={selectedSections} />
</div>
<Footer/>
<SpeedInsights/>
    </div>
  );
}

export default App;