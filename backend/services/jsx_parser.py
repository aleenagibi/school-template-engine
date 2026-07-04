import os
import re


def find_landing_page(pages_path):
    if not os.path.exists(pages_path):
        return None

    best_file = None
    best_score = 0

    for file in os.listdir(pages_path):
        if file.endswith(".jsx"):
            full_path = os.path.join(pages_path, file)

            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                code = f.read()

            section_count = code.count("<section")
            import_count = code.count("import")

            score = section_count + import_count

            if score > best_score:
                best_score = score
                best_file = full_path

    return best_file


def extract_inline_sections(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()

    matches = re.findall(
        r'(<section.*?</section>)',
        code,
        re.DOTALL
    )

    sections = []

    for i, section in enumerate(matches):
        sections.append({
            "section_name": f"inline_section_{i+1}",
            "jsx_code": section,
            "section_type": "inline"
        })

    return sections


def extract_components(components_path):
    components = []

    if not os.path.exists(components_path):
        return components

    for file in os.listdir(components_path):
        if file.endswith(".jsx"):
            full_path = os.path.join(components_path, file)

            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                code = f.read()

            components.append({
                "section_name": file.replace(".jsx", ""),
                "jsx_code": code,
                "section_type": "component"
            })

    return components