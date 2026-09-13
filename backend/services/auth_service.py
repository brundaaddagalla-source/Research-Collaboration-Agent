import os
import random
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt


JWT_SECRET = os.getenv(
    "JWT_SECRET",
    "dev-only-insecure-secret-change-me",
)

JWT_ALGORITHM = "HS256"

JWT_EXPIRE_MINUTES = int(
    os.getenv("JWT_EXPIRE_MINUTES", "60")
)


# ============================================================
# FACULTY GRID
# ============================================================

GRID_POSITIONS = [
    f"G{i}"
    for i in range(1, 17)
]


def pick_random_grid_positions() -> tuple[str, str]:
    """
    Pick two distinct grid positions from G1-G16.
    """
    return tuple(
        random.sample(GRID_POSITIONS, 2)
    )


# ============================================================
# PASSWORD
# ============================================================

def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(
        plain_password.encode("utf-8"),
        bcrypt.gensalt(),
    ).decode("utf-8")


def verify_password(
    plain_password: str,
    password_hash: str,
) -> bool:
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            password_hash.encode("utf-8"),
        )
    except ValueError:
        return False


# ============================================================
# JWT
# ============================================================

def create_access_token(
    faculty_id: str,
    name: str,
) -> str:

    now = datetime.now(timezone.utc)

    payload = {
        "sub": faculty_id,
        "name": name,
        "iat": now,
        "exp": now + timedelta(
            minutes=JWT_EXPIRE_MINUTES
        ),
    }

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token,
        JWT_SECRET,
        algorithms=[JWT_ALGORITHM],
    )