from fastapi import APIRouter
from services.scanner import scan_school_repos, SCHOOL_REPOS_DIR

router = APIRouter()


@router.get("/schools")
def get_schools():
    schools = scan_school_repos(str(SCHOOL_REPOS_DIR))

    return [school["name"] for school in schools]