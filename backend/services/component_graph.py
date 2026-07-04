def resolve_dependencies(section, all_sections):
    resolved = []
    visited = set()

    def dfs(current_section):
        section_key = (
            current_section["school"],
            current_section["section_name"]
        )

        if section_key in visited:
            return

        visited.add(section_key)
        resolved.append(current_section)

        imports = current_section.get("imports", [])

        for imported_name, _ in imports:
            for sec in all_sections:
                if (
                    sec["school"] == current_section["school"]
                    and sec["section_name"] == imported_name
                ):
                    dfs(sec)

    dfs(section)

    return resolved