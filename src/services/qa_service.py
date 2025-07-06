from typing import Tuple, List
from transformers import pipeline
from utils.logger import setup_logging
from .ner_service import NERService
from .rag_service import RAGService

logger = setup_logging()

class QAService:
    def __init__(self, rag_service: RAGService):
        self.qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
        self.ner_service = NERService()
        self.rag_service = rag_service

    def answer_question(self, question: str) -> Tuple[str, List]:
        context = self.rag_service.retrieve_context(question)
        if not context:
            logger.warning("No context retrieved for question")
            return "No relevant context found", []
        logger.info(f"Question: '{question}', Context: '{context[:50]}...'")
        result = self.qa_pipeline(question=question, context=context)
        logger.info(f"QA result: {result}")
        answer = result["answer"]
        entities = self.ner_service.extract_entities(answer)
        return answer, entities
