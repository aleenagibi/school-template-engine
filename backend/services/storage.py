import json
import os

STORAGE_FILE = "storage/indexed_sections.json"


def save_sections(data):
    os.makedirs("storage", exist_ok=True)

    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_sections():
    if not os.path.exists(STORAGE_FILE):
        return []

    with open(STORAGE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)