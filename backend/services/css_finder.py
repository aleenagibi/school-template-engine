import os


def find_main_css(css_path):
    if not os.path.exists(css_path):
        return None

    css_files = []

    for file in os.listdir(css_path):
        if file.endswith(".css"):
            full_path = os.path.join(css_path, file)
            size = os.path.getsize(full_path)

            css_files.append((size, full_path))

    if not css_files:
        return None

    css_files.sort(reverse=True)

    return css_files[0][1]