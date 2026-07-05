import os
import zipfile
from pathlib import Path
from services.component_graph import resolve_dependencies
from services.class_conflict_resolver import rename_classes

# backend/services/exporter.py -> parent -> services -> parent.parent -> backend
EXPORTS_DIR = Path(__file__).resolve().parent.parent / "exports"


def export_sections(selected_sections, all_sections):
    EXPORTS_DIR.mkdir(exist_ok=True)

    final_sections = []

    for section in selected_sections:
        dependencies = resolve_dependencies(
            section,
            all_sections
        )

        for dep in dependencies:
            if dep not in final_sections:
                final_sections.append(dep)

    combined_jsx = ""
    combined_css = ""

    for section in final_sections:
        section = rename_classes(section)

        combined_jsx += section["jsx_code"] + "\n\n"
        combined_css += section["css_code"] + "\n\n"

    jsx_path = EXPORTS_DIR / "CombinedPage.jsx"
    css_path = EXPORTS_DIR / "CombinedPage.css"
    zip_path = EXPORTS_DIR / "CombinedExport.zip"

    with open(jsx_path, "w", encoding="utf-8") as f:
        f.write(combined_jsx)

    with open(css_path, "w", encoding="utf-8") as f:
        f.write(combined_css)

    with zipfile.ZipFile(
        zip_path,
        "w"
    ) as zipf:
        zipf.write(
            jsx_path,
            arcname="CombinedPage.jsx"
        )
        zipf.write(
            css_path,
            arcname="CombinedPage.css"
        )

    return zip_path.name   # just "CombinedExport.zip"