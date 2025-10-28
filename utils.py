import io
from PyPDF2 import PdfReader

def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    return "\n".join([page.extract_text() or "" for page in reader.pages])

def chunk_text(text: str, max_chars: int = 3000):
    if len(text) <= max_chars:
        return [text]
    parts, cur = [], ""
    for p in text.split("\n\n"):
        if len(cur) + len(p) < max_chars:
            cur += p + "\n\n"
        else:
            parts.append(cur)
            cur = p + "\n\n"
    if cur:
        parts.append(cur)
    return parts
