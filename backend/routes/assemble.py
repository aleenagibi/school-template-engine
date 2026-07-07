from fastapi import APIRouter, Body
from services.exporter import export_final

router = APIRouter()


@router.post("/export")
def export_project(payload: dict = Body(...)):
    """
    Takes final, already-built file contents (produced client-side
    by mergeSections.js) and just writes + zips them. No scoping,
    no merging, no dependency resolution happens here anymore.
    """
    combined = payload.get("combined")           # {"jsx_code": str, "css_code": str} or None
    separate_files = payload.get("separate_files", [])  # [{"name": str, "jsx_code": str, "css_code": str}]
    home_jsx = payload.get("home_jsx")            # str or None

    filename = export_final(combined, separate_files, home_jsx)

    return {
        "message": "Export complete",
        "download": f"/exports/{filename}",
    }