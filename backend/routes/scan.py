from fastapi import APIRouter
import re

from services.scanner import scan_school_repos, SCHOOL_REPOS_DIR
from services.jsx_parser import (
    find_landing_page,
    extract_inline_sections,
    extract_components,
)
from services.css_finder import find_main_css
from services.css_parser import (
    extract_classes,
    extract_css,
)
from services.dependency_mapper import extract_imports
from services.storage import save_sections
from services.semantic_indexer import build_index
from services.asset_mapper import extract_assets
from services.api_mapper import extract_external_apis

router = APIRouter()


def extract_primary_class(
    jsx_code,
    fallback="UnnamedSection"
):
    """
    Extract first className from JSX.
    Example:
    <section className="Mission">
    -> Mission
    """

    match = re.search(
        r'className\s*=\s*["\']([^"\']+)["\']',
        jsx_code
    )

    if match:
        return match.group(1).split()[0]

    return fallback


@router.post("/scan")
def scan():
    schools = scan_school_repos(
        str(SCHOOL_REPOS_DIR)
    )

    all_sections = []

    for school in schools:
        landing_page = find_landing_page(
            school["pages_path"]
        )

        css_file = None

        if school["css_path"]:
            css_file = find_main_css(
                school["css_path"]
            )

        # INLINE SECTIONS
        if landing_page:
            inline_sections = (
                extract_inline_sections(
                    landing_page
                )
            )

            for section in inline_sections:
                classes = extract_classes(
                    section["jsx_code"]
                )

                css_code = extract_css(
                    css_file,
                    classes
                )

                imports = extract_imports(
                    section["jsx_code"]
                )

                assets = extract_assets(
                    section["jsx_code"]
                )

                external_apis = (
                    extract_external_apis(
                        section["jsx_code"]
                    )
                )

                section_name = (
                    extract_primary_class(
                        section["jsx_code"],
                        section["section_name"]
                    )
                )

                all_sections.append(
                    {
                        "school": school["name"],
                        "section_name": section_name,
                        # Inline sections aren't standalone files,
                        # so there's no filename identity to track.
                        "component_file": None,
                        "section_type": section["section_type"],
                        "jsx_code": section["jsx_code"],
                        "css_code": css_code,
                        "imports": imports,
                        "assets": assets,
                        "external_apis": external_apis,
                    }
                )

        # COMPONENT SECTIONS
        components = extract_components(
            school["components_path"]
        )

        for component in components:
            classes = extract_classes(
                component["jsx_code"]
            )

            css_code = extract_css(
                css_file,
                classes
            )

            imports = extract_imports(
                component["jsx_code"]
            )

            assets = extract_assets(
                component["jsx_code"]
            )

            external_apis = (
                extract_external_apis(
                    component["jsx_code"]
                )
            )

            # Capture the filename-based identity BEFORE
            # extract_primary_class potentially overwrites it
            # with a CSS className. This is what import
            # statements elsewhere (e.g. "./Header") reference.
            component_file_name = component["section_name"]

            section_name = (
                extract_primary_class(
                    component["jsx_code"],
                    component["section_name"]
                )
            )

            all_sections.append(
                {
                    "school": school["name"],
                    "section_name": section_name,
                    "component_file": component_file_name,
                    "section_type": component["section_type"],
                    "jsx_code": component["jsx_code"],
                    "css_code": css_code,
                    "imports": imports,
                    "assets": assets,
                    "external_apis": external_apis,
                }
            )

    save_sections(all_sections)
    build_index()

    return {
        "message": "Real scan complete",
        "sections_found": len(all_sections),
    }