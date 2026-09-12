from database.connection import SessionLocal
from models.models import Collaboration


def normalize_pair(name_a, name_b):
    """
    Create a consistent representation of a faculty pair.
    """

    return tuple(sorted([name_a, name_b]))


def get_existing_collaboration_pairs():
    """
    Get all existing faculty collaboration pairs.
    """

    db = SessionLocal()

    try:
        collaborations = db.query(Collaboration).all()

        existing_pairs = set()

        for collaboration in collaborations:
            pair = normalize_pair(
                collaboration.faculty_a,
                collaboration.faculty_b,
            )

            existing_pairs.add(pair)

        return existing_pairs

    finally:
        db.close()


def already_collaborating(name_a, name_b):
    """
    Check whether two faculty members already collaborate.
    """

    existing_pairs = get_existing_collaboration_pairs()

    pair = normalize_pair(name_a, name_b)

    return pair in existing_pairs


def filter_existing_collaborators(
    faculty_name,
    candidates,
):
    """
    Remove candidates who already collaborate
    with the given faculty member.
    """

    existing_pairs = get_existing_collaboration_pairs()

    filtered_candidates = []

    for candidate in candidates:

        candidate_name = candidate["name"]

        pair = normalize_pair(
            faculty_name,
            candidate_name,
        )

        if pair not in existing_pairs:
            filtered_candidates.append(candidate)

    return filtered_candidates