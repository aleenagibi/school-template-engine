import re

BOOTSTRAP_PREFIXES = [
    "col-", "row", "container", "text-", "d-", "justify-",
    "align-", "mt-", "mb-", "ms-", "me-", "pt-", "pb-", "p-", "m-",
    "img-fluid",
]

CSS_NAMED_COLORS = {
    "red", "blue", "green", "black", "white", "gray", "grey",
    "yellow", "orange", "purple", "pink", "brown", "cyan",
    "magenta", "lime", "navy", "teal", "maroon", "olive",
    "silver", "gold", "transparent", "currentcolor"
}


def extract_all_classes(jsx_code):
    pattern = r'className\s*=\s*["\']([^"\']+)["\']'
    classes = set()

    for match in re.findall(pattern, jsx_code):
        classes.update(match.split())

    meaningful = [
        c for c in classes
        if not any(c.startswith(p) for p in BOOTSTRAP_PREFIXES)
    ]

    return sorted(meaningful)


def extract_all_colors(css_code):
    colors = set()

    hex_pattern = r'#[0-9a-fA-F]{3,8}\b'
    rgb_pattern = r'rgba?\([^)]+\)'

    colors.update(re.findall(hex_pattern, css_code))
    colors.update(re.findall(rgb_pattern, css_code))

    words = re.findall(r'[a-zA-Z]+', css_code)
    for word in words:
        if word.lower() in CSS_NAMED_COLORS:
            colors.add(word.lower())

    return sorted(colors)


def apply_color_renames(css_code, color_rename_map):
    """
    Replaces a literal color value everywhere it appears in CSS.
    The negative lookahead prevents "#fff" from matching inside
    a longer hex value like "#ffffff".
    """
    for old_color, new_color in (color_rename_map or {}).items():
        if not new_color or old_color == new_color:
            continue

        pattern = re.escape(old_color) + r'(?![0-9a-fA-F])'
        css_code = re.sub(pattern, new_color, css_code)

    return css_code


def scope_css_with_prefix(css_code, prefix):
    """
    Prefixes every selector with an ancestor scope class
    (".demo3 .Mission" instead of ".demo3-Mission"), assuming
    the matching JSX will be wrapped in an element carrying
    `prefix` as its className.

    Only safe to use on inline sections, whose JSX is plain
    markup that can be wrapped in a single outer <div> without
    risking a JSX/JS structural break. Full components (which
    have their own return statements, hooks, etc.) should NOT
    use this — see rename_classes in class_conflict_resolver.py
    for that case instead.

    @keyframes blocks are protected and left untouched — their
    internal selectors (0%, 50%, from, to) are animation steps,
    not CSS class selectors, and must never be scoped.
    """
    keyframe_blocks = []

    def stash_keyframes(match):
        keyframe_blocks.append(match.group(0))
        return f"__KEYFRAME_BLOCK_{len(keyframe_blocks) - 1}__"

    protected = re.sub(
        r'@keyframes\s+[\w-]+\s*\{(?:[^{}]|\{[^{}]*\})*\}',
        stash_keyframes,
        css_code
    )

    def scope_line(match):
        selector = match.group(1)

        # @media condition lines pass through untouched — only the
        # rules *inside* the block get scoped, matched separately
        # by this same regex on its next pass over the string.
        if selector.strip().startswith("@media"):
            return match.group(0)

        parts = [
            f".{prefix} {part.strip()}"
            for part in selector.split(",")
        ]
        return ", ".join(parts) + " {"

    scoped = re.sub(r'([^{}\n]+)\{', scope_line, protected)

    for i, block in enumerate(keyframe_blocks):
        scoped = scoped.replace(f"__KEYFRAME_BLOCK_{i}__", block)

    return scoped