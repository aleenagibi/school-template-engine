from fastapi import APIRouter, Body
from services.storage import load_sections
from services.exporter import export_sections

router = APIRouter()


@router.post("/assemble")
def assemble(payload: dict = Body(...)):
    selected_sections = payload.get("selected_sections", [])
    mode = payload.get("mode", "combined")
    color_rename_map = payload.get("color_rename_map", {})

    all_sections = load_sections()

    lookup = {
        (s["school"], s["section_name"]): s
        for s in all_sections
    }

    selected = []

    for item in selected_sections:
        key = (item["school"], item["section_name"])

        if key in lookup:
            selected.append(lookup[key])
        else:
            print(
                f"[assemble] No match for school='{item['school']}', "
                f"section_name='{item['section_name']}'"
            )

    if not selected:
        print("[assemble] Warning: no sections matched, export will be empty")

    filename = export_sections(
        selected,
        all_sections,
        mode=mode,
        color_rename_map=color_rename_map,
    )

    return {
        "message": "Export complete",
        "download": f"/exports/{filename}",
    }