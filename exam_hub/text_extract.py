import io
from fastapi import UploadFile

async def extract_text_from_upload(file: UploadFile) -> str:
    filename = (file.filename or "").lower()
    content_type = (file.content_type or "").lower()
    
    contents = await file.read()
    if not contents:
        return ""
        
    is_pdf = content_type == "application/pdf" or filename.endswith(".pdf")
    if is_pdf:
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(contents))
            extracted_pages = []
            for page in reader.pages:
                txt = page.extract_text()
                if txt:
                    extracted_pages.append(txt)
            return "\n".join(extracted_pages).strip()
        except Exception:
            pass

    # Try utf-8 text read if plain text
    try:
        text = contents.decode("utf-8", errors="ignore").strip()
        # Filter out non-printable binary blobs
        printable_ratio = sum(1 for c in text if c.isprintable() or c.isspace()) / (len(text) + 1e-5)
        if printable_ratio > 0.8 and len(text) > 5:
            return text
    except Exception:
        pass

    return ""
