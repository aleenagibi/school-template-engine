from fastapi import APIRouter
from pydantic import BaseModel
from services.semantic_indexer import search_sections

router = APIRouter()


class SearchRequest(BaseModel):
    query: str


@router.post("/search")
def search(request: SearchRequest):
    return search_sections(request.query)