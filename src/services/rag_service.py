import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from utils.logger import setup_logging
from .redis_service import RedisService

logger = setup_logging()
class RAGService:
    """Service for retrieval-augmented generation using FAISS and Redis.

    Manages document embeddings and context retrieval for question answering.

    Attributes:
        model (SentenceTransformer): Model for generating text embeddings.
        index (faiss.IndexFlatL2): FAISS index for similarity search.
        redis_service (RedisService): Redis connection service.
        doc_map (dict): Mapping of index positions to filenames.
    """
    def __init__(self, redis_service: RedisService):
        """Initialize RAGService with a Redis service.

        Args:
            redis_service (RedisService): Redis connection service.
        """
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatL2(384)
        self.redis_service = redis_service
        self.doc_map = {}

    def store_embedding(self, filename: str, text: str):
        """Store a text embedding in the FAISS index.

        Args:
            filename (str): Name of the document.
            text (str): Text content to embed.
        """
        embedding = self.model.encode(text)
        self.index.add(np.array([embedding]))
        self.doc_map[self.index.ntotal - 1] = filename
        logger.info(f"Stored embedding for {filename}, index size: {self.index.ntotal}")

    def retrieve_context(self, question: str) -> str:
        """Retrieve relevant context for a question from the index.

        Args:
            question (str): Question to find context for.

        Returns:
            str: Retrieved context text, or empty string if none found.
        """
        query_embedding = self.model.encode(question)
        logger.info(f"Query embedding shape: {query_embedding.shape}")
        _, indices = self.index.search(np.array([query_embedding]), k=1)
        logger.info(f"Search indices: {indices}")

        if indices[0][0] == -1 or indices[0][0] >= self.index.ntotal:
            logger.warning("No valid index found")
            return ""
        
        index = indices[0][0]
        filename = self.doc_map.get(index, "")
        if not filename:
            logger.warning(f"No filename found for index: {index}")
            return ""
        
        context = self.redis_service.get_document(filename)
        logger.info(f"Retrieved context for {filename}: {context[:100]}...")
        return context if context else ""
