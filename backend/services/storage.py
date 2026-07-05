import json
from pathlib import Path

# backend/services/storage.py -> parent -> services -> parent.parent -> backend
STORAGE_DIR = Path(__file__).resolve().parent.parent / "storage"
STORAGE_FILE = STORAGE_DIR / "indexed_sections.json"


def save_sections(data):
    STORAGE_DIR.mkdir(exist_ok=True)

    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_sections():
    if not STORAGE_FILE.exists():
        return []

    with open(STORAGE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)