import fitz
from .extraction_strategy import ExtractionStrategy

class PDFExtractionStrategy(ExtractionStrategy):
    """Strategy for extracting text from PDF files.

    This class implements the ExtractionStrategy interface to handle PDF files
    by using the PyMuPDF (fitz) library to extract text from all pages.

    """
    def extract_text(self, file_content: bytes) -> str:
        """Extract text from PDF bytes.

        Opens the PDF from raw bytes and concatenates text from all pages.

        Args:
            file_content (bytes): Raw bytes of the PDF file.

        Returns:
            str: Extracted text from the PDF, or empty string if extraction fails.

        Raises:
            ValueError: If PDF processing fails, with a descriptive message.
        """
        try:
            doc = fitz.open(stream=file_content, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except Exception as e:
            raise ValueError(f"PDF extraction failed: {str(e)}")
 