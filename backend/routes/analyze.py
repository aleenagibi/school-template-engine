from fastapi import APIRouter, Body
from services.storage import load_sections
from services.component_graph import resolve_dependencies
from services.style_analyzer import (
    extract_all_classes,
    extract_all_colors,
    apply_color_renames,
)

router = APIRouter()


def _resolve_selected(selected_sections, all_sections):
    lookup = {
        (s["school"], s["section_name"]): s
        for s in all_sections
    }

    selected = []
    for item in selected_sections:
        key = (item["school"], item["section_name"])
        if key in lookup:
            selected.append(lookup[key])

    final_sections = []
    for section in selected:
        dependencies = resolve_dependencies(section, all_sections)
        for dep in dependencies:
            if dep not in final_sections:
                final_sections.append(dep)

    return final_sections


@router.post("/analyze")
def analyze(payload: dict = Body(...)):
    selected_sections = payload.get("selected_sections", [])

    all_sections = load_sections()
    final_sections = _resolve_selected(selected_sections, all_sections)

    combined_jsx = "\n\n".join(s["jsx_code"] for s in final_sections)
    combined_css = "\n\n".join(s["css_code"] for s in final_sections)

    return {
        "combined_jsx": combined_jsx,
        "combined_css": combined_css,
        "classes": extract_all_classes(combined_jsx),
        "colors": extract_all_colors(combined_css),
    }


@router.post("/analyze/rename")
def rename(payload: dict = Body(...)):
    css_code = payload.get("css_code", "")
    color_rename_map = payload.get("color_rename_map", {})

    css_code = apply_color_renames(css_code, color_rename_map)

    return {
        "css_code": css_code,
        "colors": extract_all_colors(css_code),
    }