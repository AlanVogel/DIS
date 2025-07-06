import spacy
from utils.logger import setup_logging

logger = setup_logging()

class NERService:
    def __init__(self):
        self.setup_model()

    def extract_entities(self, text: str) -> list:
        logger.info(f"Extracting entities from text: '{text[:50]}...'")
        if not text or not isinstance(text, str):
            logger.warning("Empty or invalid text provided for entity extraction")
            return []
        doc = self.nlp(text)
        entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
        logger.info(f"Detected entities: {entities}")
        return entities

    def setup_model(self) -> None:
        try:
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("Loaded SpaCy model 'en_core_web_sm' successfully")
        except OSError:
            logger.warning("Model 'en_core_web_sm' not found. Downloading...")
            spacy.cli.download("en_core_web_sm")
            logger.info("Downloaded and loaded 'en_core_web_sm'")
