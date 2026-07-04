from fastapi import APIRouter, Body
from services.storage import load_sections
from services.exporter import export_sections

router = APIRouter()


@router.post("/assemble")
def assemble(selected_sections: list[dict] = Body(...)):
    all_sections = load_sections()

    selected = []

    for item in selected_sections:
        school = item["school"]
        section_name = item["section_name"]

        for section in all_sections:
            if (
                section["school"] == school
                and section["section_name"] == section_name
            ):
                selected.append(section)

    zip_path = export_sections(
        selected,
        all_sections
    )

    return {
        "message": "Export complete",
        "download": zip_path
    }