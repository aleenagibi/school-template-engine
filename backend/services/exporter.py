import zipfile
from pathlib import Path

# backend/services/exporter.py -> parent -> services -> parent.parent -> backend
EXPORTS_DIR = Path(__file__).resolve().parent.parent / "exports"


def export_final(combined, separate_files, home_jsx):
    EXPORTS_DIR.mkdir(exist_ok=True)
    zip_path = EXPORTS_DIR / "Export.zip"

    with zipfile.ZipFile(zip_path, "w") as zipf:
        if combined:
            zipf.writestr("CombinedPage.jsx", combined["jsx_code"])
            zipf.writestr("CombinedPage.css", combined["css_code"])

        for file in (separate_files or []):
            zipf.writestr(f"{file['name']}.jsx", file["jsx_code"])
            zipf.writestr(f"{file['name']}.css", file["css_code"])

        if home_jsx:
            zipf.writestr("Home.jsx", home_jsx)

    return zip_path.name