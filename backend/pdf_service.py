"""PDF text extraction for resume uploads."""
import io
from PyPDF2 import PdfReader


MAX_PDF_SIZE = 10 * 1024 * 1024  # 10 MB


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract text from PDF file bytes.

    Args:
        file_bytes: Raw bytes of the uploaded PDF file.

    Returns:
        Extracted text as a single string.

    Raises:
        ValueError: If the file is too large or not a valid PDF.
    """
    if len(file_bytes) > MAX_PDF_SIZE:
        raise ValueError(f"PDF too large ({len(file_bytes)} bytes). Max: {MAX_PDF_SIZE} bytes.")

    try:
        reader = PdfReader(io.BytesIO(file_bytes))
    except Exception as e:
        raise ValueError(f"Invalid PDF file: {e}")

    if len(reader.pages) == 0:
        raise ValueError("PDF has no pages.")

    text_parts = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_parts.append(page_text.strip())

    full_text = "\n\n".join(text_parts)

    if not full_text.strip():
        raise ValueError("Could not extract any text from the PDF. It may be image-based.")

    print(f"[PDF] Extracted {len(full_text)} chars from {len(reader.pages)} page(s)")
    return full_text
