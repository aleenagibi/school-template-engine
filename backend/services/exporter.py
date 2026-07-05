import re
import zipfile
from pathlib import Path
from services.component_graph import resolve_dependencies
from services.class_conflict_resolver import rename_classes
from services.style_analyzer import apply_color_renames, scope_css_with_prefix

# backend/services/exporter.py -> parent -> services -> parent.parent -> backend
EXPORTS_DIR = Path(__file__).resolve().parent.parent / "exports"


def _sanitize_component_name(name):
    """
    Turns "hero-banner" or "hero banner" into "HeroBanner" —
    a valid, PascalCase JS identifier suitable for a component name.
    """
    parts = re.split(r'[^a-zA-Z0-9]+', name)
    parts = [p for p in parts if p]

    pascal = "".join(p[0].upper() + p[1:] for p in parts)

    if not pascal or not pascal[0].isalpha():
        pascal = "Section" + pascal

    return pascal


def _resolve_final_sections(selected_sections, all_sections):
    final_sections = []

    for section in selected_sections:
        dependencies = resolve_dependencies(section, all_sections)
        for dep in dependencies:
            if dep not in final_sections:
                final_sections.append(dep)

    return final_sections


def _scope_section(section):
    """
    Scopes a section's classes to its school, using whichever
    strategy is safe for its type:

    - Inline sections (plain JSX markup, no component_file) get
      wrapped in one outer <div className="school"> and their CSS
      selectors get a matching ancestor-scope prefix. Clean, single
      class added, no per-class renaming needed.

    - Full components (component_file is set — they're entire
      function bodies with hooks/returns/conditionals) can't be
      safely wrapped via string manipulation, so they keep the
      original per-class prefix renaming instead.
    """
    section = dict(section)
    prefix = section["school"].lower()

    if section.get("component_file") is None:
        section["jsx_code"] = (
            f'<div className="{prefix}">\n'
            f'{section["jsx_code"]}\n'
            f'</div>'
        )
        section["css_code"] = scope_css_with_prefix(
            section["css_code"], prefix
        )
    else:
        section = rename_classes(section)

    return section


def export_sections(
    selected_sections,
    all_sections,
    mode="combined",
    color_rename_map=None,
):
    EXPORTS_DIR.mkdir(exist_ok=True)

    final_sections = _resolve_final_sections(selected_sections, all_sections)

    renamed_sections = [_scope_section(section) for section in final_sections]

    if color_rename_map:
        for section in renamed_sections:
            section["css_code"] = apply_color_renames(
                section["css_code"], color_rename_map
            )

    if mode == "separate":
        return _export_separate(renamed_sections)

    return _export_combined(renamed_sections)


def _export_combined(sections):
    combined_jsx = ""
    combined_css = ""

    for section in sections:
        combined_jsx += section["jsx_code"] + "\n\n"
        combined_css += section["css_code"] + "\n\n"

    jsx_path = EXPORTS_DIR / "CombinedPage.jsx"
    css_path = EXPORTS_DIR / "CombinedPage.css"
    zip_path = EXPORTS_DIR / "CombinedExport.zip"

    with open(jsx_path, "w", encoding="utf-8") as f:
        f.write(combined_jsx)

    with open(css_path, "w", encoding="utf-8") as f:
        f.write(combined_css)

    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.write(jsx_path, arcname="CombinedPage.jsx")
        zipf.write(css_path, arcname="CombinedPage.css")

    return zip_path.name


def _export_separate(sections):
    zip_path = EXPORTS_DIR / "SeparateExport.zip"

    used_names = {}
    home_imports = []
    home_jsx_tags = []

    with zipfile.ZipFile(zip_path, "w") as zipf:
        for section in sections:
            raw_name = section.get("component_file") or section["section_name"]
            base_name = _sanitize_component_name(raw_name)

            count = used_names.get(base_name, 0)
            used_names[base_name] = count + 1
            component_name = base_name if count == 0 else f"{base_name}{count + 1}"

            jsx_content = (
                f'import "./{component_name}.css";\n\n'
                f'function {component_name}() {{\n'
                f'  return (\n'
                f'    {section["jsx_code"]}\n'
                f'  );\n'
                f'}}\n\n'
                f'export default {component_name};\n'
            )

            zipf.writestr(f"{component_name}.jsx", jsx_content)
            zipf.writestr(f"{component_name}.css", section["css_code"])

            home_imports.append(f'import {component_name} from "./{component_name}";')
            home_jsx_tags.append(f"      <{component_name} />")

        home_jsx = (
            "\n".join(home_imports) + "\n\n"
            "function Home() {\n"
            "  return (\n"
            "    <>\n"
            + "\n".join(home_jsx_tags) + "\n"
            "    </>\n"
            "  );\n"
            "}\n\n"
            "export default Home;\n"
        )

        zipf.writestr("Home.jsx", home_jsx)

    return zip_path.name