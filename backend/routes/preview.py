from fastapi import APIRouter, HTTPException
from services.storage import load_sections

router = APIRouter()


@router.get("/preview/{school}/{section_name}")
def preview_section(school: str, section_name: str):
    sections = load_sections()

    for section in sections:
        if (
            section["school"].lower() == school.lower()
            and section["section_name"].lower() == section_name.lower()
        ):
            return {
                "school": section["school"],
                "section_name": section["section_name"],
                "jsx_code": section["jsx_code"],
                "css_code": section["css_code"],
                "imports": section.get("imports", []),
                "assets": section.get("assets", []),
                "external_apis": section.get("external_apis", []),
            }

    raise HTTPException(
        status_code=404,
        detail=f"Section not found: school='{school}', section_name='{section_name}'"
    )