import pdfplumber
import io

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extracts all text from a given PDF file bytes in memory."""
    extracted_text = ""
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
        return extracted_text.strip()
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")
