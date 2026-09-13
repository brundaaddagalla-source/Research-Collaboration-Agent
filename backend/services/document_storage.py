"""
Local file storage abstraction for uploaded faculty research documents
(spec section 7/46).

The database stores metadata + a storage reference (this module's
`save_file` return value), never the raw file bytes and never the
user-supplied filename as a filesystem path - that would allow path
traversal. Storage location is a single directory, configurable via
the RESEARCH_DOCS_STORAGE_DIR env var, so it's easy to point at a
different disk/volume in another environment without touching any
calling code.
"""

import os
import uuid
from pathlib import Path

STORAGE_DIR = Path(os.getenv("RESEARCH_DOCS_STORAGE_DIR", "storage/research_documents"))
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx"}
ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}
MAX_FILE_SIZE_BYTES = int(os.getenv("RESEARCH_DOCS_MAX_FILE_SIZE_MB", "20")) * 1024 * 1024


class UploadValidationError(ValueError):
    pass


def validate_upload(filename: str, content_type: str, size: int) -> str:
    """Returns the lowercase extension (without dot) if valid, else raises."""
    ext = Path(filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise UploadValidationError("Only .pdf, .doc and .docx files are allowed.")

    if content_type and content_type not in ALLOWED_CONTENT_TYPES:
        # Some browsers send generic/octet-stream content types for .doc -
        # only hard-fail on a content type that is clearly something else.
        if content_type not in ("application/octet-stream", ""):
            raise UploadValidationError("Unrecognized file content type.")

    if size is not None and size > MAX_FILE_SIZE_BYTES:
        raise UploadValidationError(
            f"File is too large (max {MAX_FILE_SIZE_BYTES // (1024 * 1024)} MB)."
        )

    return ext.lstrip(".")


def save_file(faculty_id: int, original_filename: str, content: bytes) -> str:
    """
    Saves `content` under a generated, collision-safe filename (never the
    user-supplied name) and returns the storage reference (relative path)
    to store in FacultyResearchDocument.file_reference.
    """
    ext = Path(original_filename or "").suffix.lower()
    safe_name = f"{faculty_id}_{uuid.uuid4().hex}{ext}"
    faculty_dir = STORAGE_DIR / str(faculty_id)
    faculty_dir.mkdir(parents=True, exist_ok=True)

    destination = faculty_dir / safe_name
    with open(destination, "wb") as f:
        f.write(content)

    return str(destination)


def delete_file(file_reference: str) -> None:
    """Best-effort delete - never raises if the file is already gone."""
    try:
        path = Path(file_reference)
        # Guard against a corrupted/unexpected reference escaping the
        # storage directory.
        if STORAGE_DIR.resolve() in path.resolve().parents:
            path.unlink(missing_ok=True)
    except Exception as exc:  # noqa: BLE001
        print(f"[document_storage] Could not delete {file_reference}: {exc}")


def read_file(file_reference: str) -> bytes:
    with open(file_reference, "rb") as f:
        return f.read()