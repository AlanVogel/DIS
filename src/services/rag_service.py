import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from utils.logger import setup_logging
from .redis_service import RedisService

logger = setup_logging()
class RAGService:
    def __init__(self, redis_service: RedisService):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatL2(384)
        self.redis_service = redis_service
        self.doc_map = {}

    def store_embedding(self, filename: str, text: str):
        embedding = self.model.encode(text)
        self.index.add(np.array([embedding]))
        self.doc_map[self.index.ntotal - 1] = filename
        logger.info(f"Stored embedding for {filename}, index size: {self.index.ntotal}")

    def retrieve_context(self, question: str) -> str:
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
