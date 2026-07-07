from fastapi import APIRouter, Body
from services.storage import load_sections
from services.component_graph import resolve_dependencies

router = APIRouter()


@router.post("/analyze")
def analyze(payload: dict = Body(...)):
    """
    Resolves each selected section's dependency chain (via
    component_graph) and tags every resulting section with the
    "mode" (combine/separate) of whichever top-level selection
    pulled it in. All actual JSX/CSS scoping and merging now
    happens client-side, since it requires real JS/JSX parsing
    (Babel) that Python doesn't have a mature equivalent for.
    """
    selected_sections = payload.get("selected_sections", [])
    all_sections = load_sections()

    lookup = {
        (s["school"], s["section_name"]): s
        for s in all_sections
    }

    result_sections = []
    seen = set()

    for item in selected_sections:
        key = (item.get("school"), item.get("section_name"))
        base = lookup.get(key)

        if not base:
            print(f"[analyze] No match for {key}")
            continue

        mode = item.get("mode", "combine")
        dependencies = resolve_dependencies(base, all_sections)

        for dep in dependencies:
            dep_key = (dep["school"], dep["section_name"])
            if dep_key in seen:
                continue
            seen.add(dep_key)

            dep_copy = dict(dep)
            dep_copy["mode"] = mode
            result_sections.append(dep_copy)

    return {"sections": result_sections}