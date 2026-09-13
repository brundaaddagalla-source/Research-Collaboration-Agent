"""
Agent 24 - Expertise Mapping

Converts faculty research evidence into structured
expertise concepts for collaboration discovery.
"""


def normalize_text(text):
    """
    Normalize text for consistent matching.
    """

    if not text:
        return ""

    return " ".join(
        str(text)
        .lower()
        .strip()
        .split()
    )


def extract_research_areas(research_areas):
    """
    Extract declared research areas.

    Example:
        ["Computer Vision", "Deep Learning"]

    Returns:
        ["Computer Vision", "Deep Learning"]
    """

    if not research_areas:
        return []

    if isinstance(research_areas, str):
        research_areas = [
            research_areas
        ]

    areas = []

    for area in research_areas:

        area = str(area).strip()

        if area and area not in areas:
            areas.append(area)

    return areas


def extract_publication_titles(publications):
    """
    Extract publication titles.
    """

    if not publications:
        return []

    titles = []

    for publication in publications:

        if isinstance(publication, dict):
            title = publication.get(
                "title"
            )
        else:
            title = getattr(
                publication,
                "title",
                None,
            )

        if title:
            titles.append(
                str(title).strip()
            )

    return titles


def extract_project_topics(projects):
    """
    Extract useful project-level research topics.
    """

    if not projects:
        return []

    topics = []

    for project in projects:

        if isinstance(project, dict):

            title = project.get(
                "title"
            )

            description = project.get(
                "description"
            )

            research_area = project.get(
                "research_area"
            )

        else:

            title = getattr(
                project,
                "title",
                None,
            )

            description = getattr(
                project,
                "description",
                None,
            )

            research_area = getattr(
                project,
                "research_area",
                None,
            )

        if title:
            topics.append(
                str(title).strip()
            )

        if research_area:
            topics.append(
                str(research_area).strip()
            )

        if description:
            topics.append(
                str(description).strip()
            )

    return topics


def build_expertise_map(
    research_areas=None,
    publications=None,
    projects=None,
):
    """
    Build a structured expertise map.

    Declared research areas are treated as the
    strongest expertise signals.

    Publications and projects provide supporting
    evidence.
    """

    areas = extract_research_areas(
        research_areas
    )

    publication_titles = (
        extract_publication_titles(
            publications
        )
    )

    project_topics = (
        extract_project_topics(
            projects
        )
    )

    expertise = []

    # --------------------------------------------------
    # Primary expertise
    # --------------------------------------------------

    for area in areas:

        if area not in expertise:
            expertise.append(area)

    # --------------------------------------------------
    # Supporting expertise from project research areas
    # --------------------------------------------------

    for topic in project_topics:

        topic = topic.strip()

        if not topic:
            continue

        # Only add short research-area-like values.
        # Full descriptions remain evidence rather
        # than becoming expertise labels.
        if len(topic.split()) <= 5:

            if topic not in expertise:
                expertise.append(topic)

    return {
        "expertise": expertise,
        "research_areas": areas,
        "publication_titles": publication_titles,
        "project_topics": project_topics,
    }


def build_faculty_expertise(
    faculty,
    publications=None,
    projects=None,
):
    """
    Build an expertise map for one faculty member.

    Expected faculty fields:
        name
        department
        research_areas
    """

    return {
        "faculty_id": getattr(
            faculty,
            "id",
            None,
        ),

        "name": getattr(
            faculty,
            "name",
            None,
        ),

        "department": getattr(
            faculty,
            "department",
            None,
        ),

        **build_expertise_map(
            research_areas=getattr(
                faculty,
                "research_areas",
                None,
            ),

            publications=publications,

            projects=projects,
        ),
    }


def get_expertise_for_faculty(
    faculty_id,
    faculty_evidence,
):
    """
    Get expertise for one faculty member
    from the structured evidence dictionary.
    """

    evidence = faculty_evidence.get(
        faculty_id,
        {},
    )

    return build_expertise_map(
        research_areas=evidence.get(
            "research_areas",
            [],
        ),

        publications=evidence.get(
            "publications",
            [],
        ),

        projects=evidence.get(
            "projects",
            [],
        ),
    )