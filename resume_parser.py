import io
from typing import Optional

import pdfplumber
import docx


def _extract_from_pdf(file_bytes: bytes) -> str:
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"
    return text


def _extract_from_docx(file_bytes: bytes) -> str:
    file_stream = io.BytesIO(file_bytes)
    document = docx.Document(file_stream)
    return "\n".join(p.text for p in document.paragraphs)


def extract_resume_text(uploaded_file) -> Optional[str]:
    """
    Takes a Streamlit UploadedFile and returns plain text.
    Supports PDF and DOCX. Returns None for unsupported types.
    """
    if uploaded_file is None:
        return None

    file_bytes = uploaded_file.read()
    name = uploaded_file.name.lower()

    if name.endswith(".pdf"):
        return _extract_from_pdf(file_bytes)
    elif name.endswith(".docx"):
        return _extract_from_docx(file_bytes)
    else:
        return None
