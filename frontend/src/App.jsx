import { useState } from "react";
import API from "./api";
import SchoolList from "./components/SchoolList";
import SectionList from "./components/SectionList";
import PreviewPanel from "./components/PreviewPanel";
import AssemblePanel from "./components/AssemblePanel";
import TemplateCanvas from "./components/TemplateCanvas";
import "./App.css";

function App() {
  const [selectedSchool, setSelectedSchool] = useState(null);

  const [preview, setPreview] = useState(null);

  const [selectedSections, setSelectedSections] = useState([]);

  const [activeTab, setActiveTab] = useState("schools");

  const loadPreview = async (school, section_name) => {
    const res = await API.get(`/preview/${school}/${section_name}`);
    setPreview(res.data);
  };

  const addSection = (section) => {
    setSelectedSections((prev) => {
      const exists = prev.find((s) => s.section_name === section.section_name);

      if (exists) return prev;

      return [...prev, section];
    });
  };

  return (
    <div className="app-container">
      <div className="workspace">
        {/* LEFT PANEL */}
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
            >
              Sections
            </button>
          </div>

          {activeTab === "schools" && (
            <SchoolList
              onSelect={setSelectedSchool}
              selectedSchool={selectedSchool}
            />
          )}

          {activeTab === "sections" && (
            <SectionList
              school={selectedSchool}
              onPreview={loadPreview}
              onAdd={addSection}
            />
          )}
        </div>

        {/* CENTER */}
        <TemplateCanvas
          selectedSections={selectedSections}
          setSelectedSections={setSelectedSections}
        />

        {/* RIGHT */}
        <div className="right-panel">
          <PreviewPanel preview={preview} />
        </div>
      </div>

      {/* BOTTOM */}
      <div className="bottom-panel">
        <AssemblePanel selected={selectedSections} />
      </div>
    </div>
  );
}

export default App;
