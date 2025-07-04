from .extraction_strategy import ExtractionStrategy
import fitz

class PDFExtractionStrategy(ExtractionStrategy):
    def extract_text(self, file_content: bytes) -> str:
        try:
            doc = fitz.open(stream=file_content, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except Exception as e:
            raise ValueError(f"PDF extraction failed: {str(e)}")
 