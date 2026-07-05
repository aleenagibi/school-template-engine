import os
from pathlib import Path

# Single source of truth for the school_repos location.
# services/scanner.py -> parent -> services
#                      -> parent.parent -> backend
#                      -> parent.parent.parent -> school-template-engine (project root)
SCHOOL_REPOS_DIR = Path(__file__).resolve().parent.parent.parent / "school_repos"


def find_folder_case_insensitive(
    parent_path,
    target_name
):
    """
    Finds folder regardless of case.
    Example:
    Pages / pages / PAGES
    """
    if not os.path.exists(parent_path):
        return None
    for item in os.listdir(parent_path):
        if item.lower() == target_name.lower():
            return os.path.join(
                parent_path,
                item
            )
    return None


def scan_school_repos(root_path):
    schools = []

    if not os.path.exists(root_path):
        print(f"[scan] ERROR: root_path does not exist: {root_path}")
        return schools

    for folder in os.listdir(root_path):
        school_path = os.path.join(
            root_path,
            folder
        )

        if not os.path.isdir(school_path):
            continue

        src_path = find_folder_case_insensitive(
            school_path,
            "src"
        )

        if not src_path:
            print(f"[scan] Skipping '{folder}': no 'src' folder found")
            continue

        pages_path = (
            find_folder_case_insensitive(
                src_path,
                "Pages"
            )
        )
        components_path = (
            find_folder_case_insensitive(
                src_path,
                "components"
            )
        )
        assets_path = (
            find_folder_case_insensitive(
                src_path,
                "assets"
            )
        )

        css_path = None
        if assets_path:
            css_path = (
                find_folder_case_insensitive(
                    assets_path,
                    "css"
                )
            )

        if not pages_path:
            print(f"[scan] Warning: '{folder}' has no Pages folder")
        if not components_path:
            print(f"[scan] Warning: '{folder}' has no components folder")
        if not assets_path:
            print(f"[scan] Warning: '{folder}' has no assets folder")
        elif not css_path:
            print(f"[scan] Warning: '{folder}' has assets but no css folder inside it")

        schools.append(
            {
                "name": folder,
                "path": school_path,
                "pages_path": pages_path,
                "components_path": components_path,
                "css_path": css_path
            }
        )

    print(f"[scan] Found {len(schools)} school folder(s) under {root_path}")
    return schools