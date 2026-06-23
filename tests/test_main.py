import pytest
from unittest.mock import patch, MagicMock
from backend.legacy_parser import extract_text_from_pdf

@patch('backend.legacy_parser.pdfplumber.open')
def test_canva_trap_rejection(mock_pdfplumber_open):
    """
    Tests the Canva Trap logic by mocking pdfplumber. 
    We force it to return empty text to prove our < 50 chars logic works.
    """
    # 1. Create a fake "page" that returns just a few spaces (less than 50 chars)
    mock_page = MagicMock()
    mock_page.extract_text.return_value = "   "
    
    # 2. Attach the fake page to our fake PDF object
    mock_pdf = MagicMock()
    mock_pdf.pages = [mock_page]
    
    # 3. Make sure the 'with pdfplumber.open(...)' block uses our fake PDF
    mock_pdfplumber_open.return_value.__enter__.return_value = mock_pdf
    
    # 4. Run the function. The mock intercepts the bytes, so dummy bytes are fine.
    result = extract_text_from_pdf(b"dummy_bytes_dont_matter")
    
    # 5. Assert the Canva Trap caught it!
    assert result["status"] == "error"
    assert "0% Parseability" in result["message"]

def test_corrupted_pdf_rejection():
    """
    Ensures the system gracefully handles completely invalid/corrupted files
    without crashing the server.
    """
    # This uses the fake bytes that originally broke your test!
    fake_pdf_bytes = b"%PDF-1.4\nEOF"
    
    result = extract_text_from_pdf(fake_pdf_bytes)
    
    assert result["status"] == "error"
    assert "Parsing Failure" in result["message"]