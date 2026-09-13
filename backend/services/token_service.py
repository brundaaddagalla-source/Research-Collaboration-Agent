"""
Secure one-time response tokens for collaboration-request emails
(Accept/Reject, Approve/Reject buttons).

Design (per spec sections 26-31):
  - The raw token is a cryptographically secure random string. It is
    put in the email link and NEVER stored anywhere.
  - Only a SHA-256 hash of the token is stored in the database
    (CollaborationResponseToken.token_hash).
  - Tokens expire, are one-time use, and are scoped to one request,
    one recipient, and one action.
"""

import hashlib
import os
import secrets
from datetime import datetime, timedelta

TOKEN_BYTES = 32  # 256-bit token
DEFAULT_EXPIRY_HOURS = int(os.getenv("COLLAB_TOKEN_EXPIRE_HOURS", "72"))


def generate_raw_token() -> str:
    """A cryptographically secure, URL-safe random token."""
    return secrets.token_urlsafe(TOKEN_BYTES)


def hash_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


def default_expiry() -> datetime:
    return datetime.utcnow() + timedelta(hours=DEFAULT_EXPIRY_HOURS)