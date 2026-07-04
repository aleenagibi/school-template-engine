import re


def rename_classes(section):
    school_prefix = section["school"].lower()

    jsx_code = section["jsx_code"]
    css_code = section["css_code"]

    class_pattern = r'className\s*=\s*["\']([^"\']+)["\']'
    matches = re.findall(class_pattern, jsx_code)

    class_map = {}

    for match in matches:
        classes = match.split()

        bootstrap_prefixes = [
    "col-",
    "row",
    "container",
    "text-",
    "d-",
    "justify-",
    "align-",
    "mt-",
    "mb-",
    "ms-",
    "me-",
    "pt-",
    "pb-",
    "p-",
    "m-"
]

    for cls in classes:
        if any(cls.startswith(prefix) for prefix in bootstrap_prefixes):
            continue

        new_cls = f"{school_prefix}-{cls}"
        class_map[cls] = new_cls


    # replace in JSX
    for old_cls, new_cls in class_map.items():
        jsx_code = re.sub(
            rf'\b{old_cls}\b',
            new_cls,
            jsx_code
        )

    # replace in CSS
    for old_cls, new_cls in class_map.items():
        css_code = re.sub(
            rf'\.{old_cls}\b',
            f".{new_cls}",
            css_code
        )

    section["jsx_code"] = jsx_code
    section["css_code"] = css_code

    return section