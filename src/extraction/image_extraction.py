import io
import easyocr
import numpy as np
from PIL import Image
from .extraction_strategy import ExtractionStrategy

class ImageExtractionStrategy(ExtractionStrategy):
    def __init__(self):
        self.reader = easyocr.Reader(["en"])

    def extract_text(self, file_content: bytes) -> str:
        try:
            image = Image.open(io.BytesIO(file_content))
            image = image.convert("L")
            image_np = np.array(image)
            result = self.reader.readtext(image_np, detail=0)
            return " ".join(result) if result else ""
        except Exception as e:
            raise ValueError(f"Image extraction failed: {str(e)}")
