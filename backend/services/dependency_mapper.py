import re


def extract_imports(code):
    imports = re.findall(
        r'import\s+(.*?)\s+from\s+[\'"](.*?)[\'"]',
        code
    )

    return imports