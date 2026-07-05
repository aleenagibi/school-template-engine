import re


def extract_assets(code):
    assets = []

    # Imported local assets
    import_pattern = r'import\s+\w+\s+from\s+[\'"](.*?\.(png|jpg|jpeg|svg|webp|pdf|mp4))[\'"]'
    import_matches = re.findall(import_pattern, code, re.IGNORECASE)

    for match in import_matches:
        assets.append(match[0])

    # Root-relative / direct paths
    direct_patterns = [
        r'src=["\'](.*?\.(png|jpg|jpeg|svg|webp|pdf|mp4))["\']',
        r'href=["\'](.*?\.(pdf))["\']'
    ]

    for pattern in direct_patterns:
        matches = re.findall(pattern, code, re.IGNORECASE)

        for match in matches:
            assets.append(match[0])

    # Constant URLs (fallback images / CDN / S3)
    url_pattern = r'[\'"](https?:\/\/.*?\.(png|jpg|jpeg|svg|webp|pdf|mp4))[\'"]'
    url_matches = re.findall(url_pattern, code, re.IGNORECASE)

    for match in url_matches:
        assets.append(match[0])

    return list(dict.fromkeys(assets))