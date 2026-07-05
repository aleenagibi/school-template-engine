from fastapi import APIRouter, Body
from services.storage import load_sections
from services.exporter import export_sections

router = APIRouter()


@router.post("/assemble")
def assemble(selected_sections: list[dict] = Body(...)):
    all_sections = load_sections()

    lookup = {
        (s["school"], s["section_name"]): s
        for s in all_sections
    }

    selected = []

    for item in selected_sections:
        school = item["school"]
        section_name = item["section_name"]

        key = (school, section_name)

        if key in lookup:
            selected.append(lookup[key])
        else:
            print(
                f"[assemble] No match for school='{school}', "
                f"section_name='{section_name}'"
            )

    if not selected:
        print("[assemble] Warning: no sections matched, export will be empty")

    filename = export_sections(
        selected,
        all_sections
    )

    download_url = f"/exports/{filename}"

    return {
        "message": "Export complete",
        "download": download_url
    }