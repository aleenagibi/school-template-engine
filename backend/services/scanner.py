import os


def scan_school_repos(root_path):
    schools = []

    for folder in os.listdir(root_path):
        school_path = os.path.join(root_path, folder)

        if not os.path.isdir(school_path):
            continue

        src_path = os.path.join(school_path, "src")

        pages_path = os.path.join(src_path, "Pages")
        components_path = os.path.join(src_path, "components")
        css_path = os.path.join(src_path, "assets", "css")

        schools.append({
            "name": folder,
            "path": school_path,
            "pages_path": pages_path,
            "components_path": components_path,
            "css_path": css_path
        })

    return schools