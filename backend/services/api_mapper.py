import re


def extract_external_apis(code):
    """
    Extract all external API URLs from JSX/JS files.
    Detects:
    - fetch()
    - axios()
    - const URL variables
    """

    url_pattern = r'https?://[^\s"\']+'

    matches = re.findall(url_pattern, code)

    cleaned = []

    for url in matches:
        cleaned.append(url.strip())

    return list(set(cleaned))