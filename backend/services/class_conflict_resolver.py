import re
from services.style_analyzer import BOOTSTRAP_PREFIXES


def rename_classes(section):
    school_prefix = section["school"].lower()

    jsx_code = section["jsx_code"]
    css_code = section["css_code"]

    class_attr_pattern = r'className\s*=\s*(["\'])([^"\']+)\1'

    # First pass: collect every distinct class token in the file,
    # so the whole file uses one consistent rename map.
    class_map = {}

    for match in re.finditer(class_attr_pattern, jsx_code):
        for cls in match.group(2).split():
            if cls in class_map:
                continue
            if any(cls.startswith(prefix) for prefix in BOOTSTRAP_PREFIXES):
                continue
            class_map[cls] = f"{school_prefix}-{cls}"

    # Second pass: rewrite each className value token-by-token.
    #
    # This deliberately avoids re.sub(r'\bOLD\b', NEW, whole_file) —
    # \b treats "-" as a boundary, so a short class like "bi" is a
    # valid \b-bounded match *inside* a longer class like
    # "bi-envelope-fill". Renaming them independently causes
    # cascading double-prefixing (bi-envelope-fill gets bi's
    # renamed applied once as a side effect, then its own rename
    # applied again on top). Operating on whole className tokens
    # instead of substrings of the raw file text avoids this
    # entirely, since each token is compared for exact equality.
    def replace_class_attr(match):
        quote = match.group(1)
        tokens = match.group(2).split()
        new_tokens = [class_map.get(t, t) for t in tokens]
        return f'className={quote}{" ".join(new_tokens)}{quote}'

    jsx_code = re.sub(class_attr_pattern, replace_class_attr, jsx_code)

    # CSS selectors aren't as cleanly tokenized as a className
    # attribute, so we still use regex substitution here — but
    # processing longest class names first prevents a short class
    # (".bi") from matching inside a longer one that's already
    # been renamed (".demo6-bi-envelope-fill" no longer contains
    # a literal ".bi" once "bi-envelope-fill" has been handled
    # first).
    for old_cls, new_cls in sorted(class_map.items(), key=lambda kv: -len(kv[0])):
        css_code = re.sub(
            rf'\.{re.escape(old_cls)}\b',
            f'.{new_cls}',
            css_code
        )

    section["jsx_code"] = jsx_code
    section["css_code"] = css_code

    return section