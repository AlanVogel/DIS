from extraction.pdf_extraction import PDFExtractionStrategy
from extraction.image_extraction import ImageExtractionStrategy
from .redis_service import RedisService
from .rag_service import RAGService

class DocumentService:
    """Service for processing and extracting text from uploaded documents.

    Manages the extraction of text from PDF and image files using specific strategies
    and stores the results in Redis and FAISS indices.

    Attributes:
        redis_service (RedisService): Service for Redis operations.
        rag_service (RAGService): Service for retrieval-augmented generation.
        strategies (dict): Mapping of file extensions to extraction strategies.
    """
    def __init__(self, redis_service: RedisService ,rag_service: RAGService):
        """Initialize DocumentService with Redis and RAG services.

        Args:
            redis_service (RedisService): Redis connection service.
            rag_service (RAGService): RAG service instance.
        """
        self.redis_service = redis_service
        self.rag_service = rag_service
        self.strategies = {
            ".pdf": PDFExtractionStrategy(),
            ".jpg": ImageExtractionStrategy(),
            ".jpeg": ImageExtractionStrategy(),
            ".png": ImageExtractionStrategy()
        }

    def process_document(self, filename: str, content: bytes) -> str:
        """Process a document and extract its text.

        Uses the appropriate strategy based on file extension and stores the text.

        Args:
            filename (str): Name of the uploaded file.
            content (bytes): Raw bytes of the file.

        Returns:
            str: Extracted text from the document.
        """
        extension = filename.lower()[filename.rfind("."):]
        strategy = self.strategies.get(extension)
        if not strategy:
            raise ValueError("Unsupported file type")
        text = strategy.extract_text(content)
        self.redis_service.store_document(filename, text)
        self.rag_service.store_embedding(filename, text)
        return text
