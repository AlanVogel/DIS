import io
import easyocr
import numpy as np
from PIL import Image
from .extraction_strategy import ExtractionStrategy

class ImageExtractionStrategy(ExtractionStrategy):
    """Strategy for extracting text from image files using OCR.

    This class implements the ExtractionStrategy interface to handle image files
    (e.g., .jpg, .jpeg, .png) by converting the raw bytes to a processable format
    and using the easyocr library for text recognition.

    Attributes:
        reader (easyocr.Reader): OCR reader instance initialized for English.

    """
    def __init__(self):
        """Initialize the ImageExtractionStrategy with an English OCR reader."""
        self.reader = easyocr.Reader(["en"])

    def extract_text(self, file_content: bytes) -> str:
        """Extract text from image bytes using OCR.

        Converts the input bytes to a PIL Image, processes it into a numpy array,
        and applies OCR to extract text.

        Args:
            file_content (bytes): Raw bytes of the image file.

        Returns:
            str: Extracted text from the image, or empty string if extraction fails.

        Raises:
            ValueError: If image processing or OCR fails, with a descriptive message.
        """
        try:
            image = Image.open(io.BytesIO(file_content))
            image = image.convert("L")
            image_np = np.array(image)
            result = self.reader.readtext(image_np, detail=0)
            return " ".join(result) if result else ""
        except Exception as e:
            raise ValueError(f"Image extraction failed: {str(e)}")
