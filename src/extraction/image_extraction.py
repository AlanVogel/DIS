import easyocr
import io
from PIL import Image
from .extraction_strategy import ExtractionStrategy

class ImageExtractionStrategy(ExtractionStrategy):
    def __init__(self):
        self.reader = easyocr.Reader(["en"])

    def extract_text(self, file_content: bytes) -> str:
        try:
            image = Image.open(io.BytesIO(file_content))
            result = self.reader.readtext(image, detail=0)
            return " ".join(result)
        except Exception as e:
            raise ValueError(f"Image extraction failed: {str(e)}")
