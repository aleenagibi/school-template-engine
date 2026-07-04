def detect_section_tag(section_name, jsx_code):
    text = (
        section_name + " " + jsx_code
    ).lower()

    if any(x in text for x in [
        "header", "navbar"
    ]):
        return "Header"

    if any(x in text for x in [
        "hero", "slider", "banner"
    ]):
        return "Slider"

    if any(x in text for x in [
        "about", "vision", "mission"
    ]):
        return "About"

    if any(x in text for x in [
        "gallery", "photo", "album"
    ]):
        return "Gallery"

    if any(x in text for x in [
        "event", "upcoming"
    ]):
        return "Events"

    if any(x in text for x in [
        "news", "latest"
    ]):
        return "News"

    if any(x in text for x in [
        "notice", "announcement"
    ]):
        return "Notice"

    if any(x in text for x in [
        "footer", "copyright"
    ]):
        return "Footer"

    if any(x in text for x in [
        "calendar", "schedule"
    ]):
        return "Calendar"

    if any(x in text for x in [
        "birthday"
    ]):
        return "Birthday"

    if any(x in text for x in [
        "topper", "achievement"
    ]):
        return "Topper"
    
    if any(x in text for x in [
        "highlight"
    ]):
        return "Highlight"

    return "General"