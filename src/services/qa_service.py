from transformers import pipeline
from .ner_service import NERService
from .rag_service import RAGService

class QAService:
    def __init__(self):
        self.qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
        self.ner_service = NERService()
        self.rag_service = RAGService()

    def answer_question(self, question: str) -> tuple:
        context = self.rag_service.retrieve_context(question)
        if not context:
            return "No relevant context found", []
        result = self.qa_pipeline(question=question, context=context)
        entities = self.ner_service.extract_entities(result["answer"])
        return result["answer"], entities
