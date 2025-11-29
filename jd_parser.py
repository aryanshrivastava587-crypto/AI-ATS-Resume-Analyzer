from typing import Optional
import io
import pdfplumber


def extract_jd_text(uploaded_file, jd_text_manual: str) -> Optional[str]:
    """
    Priority:
    1) If user pasted JD text manually -> use that.
    2) Else try to read from uploaded file (PDF or TXT).
    """
    if jd_text_manual and jd_text_manual.strip():
        return jd_text_manual.strip()

    if uploaded_file is None:
        return None

    name = uploaded_file.name.lower()
    file_bytes = uploaded_file.read()

    if name.endswith(".pdf"):
        text = ""
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    if name.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore")

    return None
