from fastapi import APIRouter
from services.scanner import scan_school_repos

router = APIRouter()


@router.get("/schools")
def get_schools():
    schools = scan_school_repos("../school_repos")

    return [school["name"] for school in schools]