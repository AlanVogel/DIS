from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from .redis_service import RedisService

class RAGService:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatL2(384)
        self.redis_service = RedisService()
        self.doc_map = {}

    def store_embedding(self, filename: str, text: str):
        embedding = self.model.encode(text)
        self.index.add(np.array([embedding]))
        self.doc_map[self.index.ntotal - 1] = filename

    def retrieve_context(self, question: str) -> str:
        query_embedding = self.model.encode(question)
        _, indices = self.index.search(np.array([query_embedding]), k=1)
        if indices[0][0] == -1:
            return ""
        filename = self.doc_map.get(indices[0][0], "")
        return self.redis_service.get_document(filename) or ""
