from extraction.pdf_extraction import PDFExtractionStrategy
from extraction.image_extraction import ImageExtractionStrategy
from .redis_service import RedisService
from .rag_service import RAGService

class DocumentService:
    def __init__(self):
        self.redis_service = RedisService()
        self.rag_service = RAGService()
        self.strategies = {
            ".pdf": PDFExtractionStrategy(),
            ".jpg": ImageExtractionStrategy(),
            ".jpeg": ImageExtractionStrategy(),
            ".png": ImageExtractionStrategy()
        }

    def process_document(self, filename: str, content: bytes) -> str:
        extension = filename.lower()[filename.rfind("."):]
        strategy = self.strategies.get(extension)
        if not strategy:
            raise ValueError("Unsupported file type")
        text = strategy.extract_text(content)
        self.redis_service.store_document(filename, text)
        self.rag_service.store_embedding(filename, text)
        return text
