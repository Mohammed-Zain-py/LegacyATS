import io
import logging
from typing import TypedDict, Optional
import pdfplumber

# Set up clean logging for debugging the backend
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("legacy_parser")

class ParserResponse(TypedDict):
    """Structured dictionary response schema for the legacy parser."""
    status: str          # "success" or "error"
    extracted_text: Optional[str]
    message: str

def extract_text_from_pdf(file_bytes: bytes) -> ParserResponse:
    """Rips text from a PDF byte stream using coordinate-based layout mapping.
    
    Intentionally avoids OCR to replicate the exact limitations of an older,
    rigid corporate ATS that cannot digest flattened images or scanned papers.
    
    Args:
        file_bytes: The raw binary data of the uploaded PDF file.
        
    Returns:
        A ParserResponse dictionary containing status, text, and metadata.
    """
    try:
        extracted_pages = []
        
        # Convert raw bytes into an in-memory file stream so pdfplumber can open it
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                # .extract_text() reads character by character based on layout coordinates
                text = page.extract_text()
                if text:
                    extracted_pages.append(text)
        
        # Combine all page text with clean spacing
        full_text = "\n".join(extracted_pages).strip()
        
        # CRITICAL CHECK: THE CANVA TRAP (Image-Only PDFs)
        # If a user uploads an image, scanned document, or an illustrative layout 
        # flattened into a PDF, the character length will be near zero.
        if len(full_text) < 50:
            logger.warning("Canva Trap Triggered: Document contains insufficient parseable text.")
            return {
                "status": "error",
                "extracted_text": None,
                "message": "0% Parseability: Image-only or flattened PDF detected. A real legacy ATS would instantly trash this resume because it cannot read pixels."
            }
            
        logger.info(f"Successfully parsed PDF. Extracted {len(full_text)} characters.")
        return {
            "status": "success",
            "extracted_text": full_text,
            "message": "Text successfully extracted from document."
        }
        
    except Exception as e:
        logger.error(f"Failed to parse PDF due to exception: {str(e)}")
        return {
            "status": "error",
            "extracted_text": None,
            "message": f"Parsing Failure: File is corrupted or unreadable. Error: {str(e)}"
        }