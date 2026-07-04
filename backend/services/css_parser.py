import cssutils
import logging
import re

cssutils.log.setLevel(logging.CRITICAL)


def extract_classes(code):
    patterns = [
        r'className\s*=\s*["\']([^"\']+)["\']',
        r'class\s*=\s*["\']([^"\']+)["\']'
    ]

    classes = []

    for pattern in patterns:
        matches = re.findall(pattern, code)

        for match in matches:
            classes.extend(match.split())

    return list(set(classes))


def selector_matches(selector, classes):
    for cls in classes:
        pattern = rf'\.{re.escape(cls)}(\b|:|\.|#|\s|>|~|\+)'

        if re.search(pattern, selector):
            return True

    return False


def extract_css(css_file, classes):
    if not css_file:
        return ""

    sheet = cssutils.parseFile(css_file)

    extracted = []

    for rule in sheet:

        # Normal selectors
        if rule.type == rule.STYLE_RULE:
            selector = rule.selectorText

            if selector_matches(selector, classes):
                extracted.append(str(rule.cssText))

        elif rule.type == rule.MEDIA_RULE:
            media_blocks = []

            for subrule in rule.cssRules:
                if subrule.type == subrule.STYLE_RULE:
                    selector = subrule.selectorText

                    if selector_matches(selector, classes):
                        media_blocks.append(str(subrule.cssText))

            if media_blocks:
                extracted.append(
                    f"@media {rule.media.mediaText} {{\n"
                    + "\n".join(media_blocks)
                    + "\n}"
                )

        elif hasattr(rule, "KEYFRAMES_RULE") and rule.type == rule.KEYFRAMES_RULE:
            extracted.append(str(rule.cssText))

    return "\n\n".join(extracted)