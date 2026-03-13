import io

from pypdf import PdfReader


class PDFExtractionError(Exception):
    """Raised when PDF text extraction fails."""


def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
    except Exception as exc:
        raise PDFExtractionError("Could not read the uploaded PDF.") from exc

    page_texts: list[str] = []
    for page in reader.pages:
        text = (page.extract_text() or "").strip()
        if text:
            page_texts.append(text)

    combined_text = "\n".join(page_texts).strip()
    if not combined_text:
        raise PDFExtractionError("No extractable text was found in the PDF.")

    return combined_text
