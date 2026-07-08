from pathlib import Path
from fastapi import FastAPI
from routes.scan import router as scan_router
from routes.schools import router as schools_router
from routes.search import router as search_router
from routes.assemble import router as assemble_router
from routes.sections import router as sections_router
from routes.preview import router as preview_router
from routes.analyze import router as analyze_router
from services.semantic_indexer import build_index
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

EXPORTS_DIR = Path(__file__).resolve().parent / "exports"
EXPORTS_DIR.mkdir(exist_ok=True)

app = FastAPI()

app.mount(
    "/exports",
    StaticFiles(directory=str(EXPORTS_DIR)),
    name="exports"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten to your actual Vercel domain once it exists — see note below
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scan_router)
app.include_router(preview_router)
app.include_router(schools_router)
app.include_router(search_router)
app.include_router(assemble_router)
app.include_router(sections_router)
app.include_router(analyze_router)


@app.on_event("startup")
def startup_event():
    build_index()


@app.get("/")
def home():
    return {"message": "School Template Intelligence System Running"}