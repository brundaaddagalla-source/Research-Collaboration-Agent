"""
Text extraction for uploaded research documents (spec section 8).

PDF  -> pypdf
DOCX -> python-docx
DOC  -> not practical to extract reliably without extra system
        dependencies in this environment; we store the document and
        report extraction as "unavailable" instead of failing the
        upload.

Returns (extracted_text: str | None, status: "extracted" | "unavailable").
"""

from typing import Optional, Tuple


def extract_text(file_path: str, file_type: str) -> Tuple[Optional[str], str]:
    file_type = (file_type or "").lower()

    if file_type == "pdf":
        return _extract_pdf(file_path)
    if file_type == "docx":
        return _extract_docx(file_path)
    if file_type == "doc":
        # Legacy binary .doc - no reliable pure-Python extractor available
        # here. Do not break the upload; just report it.
        return None, "unavailable"

    return None, "unavailable"


def _extract_pdf(file_path: str) -> Tuple[Optional[str], str]:
    try:
        from pypdf import PdfReader

        reader = PdfReader(file_path)
        pages_text = [page.extract_text() or "" for page in reader.pages]
        text = "\n".join(pages_text).strip()
        if not text:
            return None, "unavailable"
        return text, "extracted"
    except Exception as exc:  # noqa: BLE001
        print(f"[document_extraction] PDF extraction failed for {file_path}: {exc}")
        return None, "unavailable"


def _extract_docx(file_path: str) -> Tuple[Optional[str], str]:
    try:
        import docx

        document = docx.Document(file_path)
        text = "\n".join(p.text for p in document.paragraphs).strip()
        if not text:
            return None, "unavailable"
        return text, "extracted"
    except Exception as exc:  # noqa: BLE001
        print(f"[document_extraction] DOCX extraction failed for {file_path}: {exc}")
        return None, "unavailable"