from fastapi import APIRouter
from services.storage import load_sections

router = APIRouter()


@router.get("/schools/{school}/sections")
def get_school_sections(school: str):
    sections = load_sections()

    filtered_sections = [
        {
            "section_name": section["section_name"],
            "section_type": section["section_type"],
            "component_file": section.get("component_file"),
        }
        for section in sections
        if section["school"].lower() == school.lower()
    ]

    return {
        "school": school,
        "sections": filtered_sections
    }