import spacy
from utils.logger import setup_logging

logger = setup_logging()

class NERService:
    """Service for named entity recognition (NER) using SpaCy.

    Extracts entities (e.g., dates, organizations) from text using a pre-trained
    SpaCy model, with logging for debugging and error handling.

    Attributes:
        nlp (spacy.Language): SpaCy language model instance for NER.
    """
    def __init__(self):
        """Initialize NERService by setting up the SpaCy model.

        Loads or downloads the 'en_core_web_sm' model for English NER.
        """
        self.setup_model()

    def extract_entities(self, text: str) -> list:
        """Extract named entities from the input text.

        Processes the text with the SpaCy model and returns a list of detected entities.

        Args:
            text (str): Input text to analyze for entities.

        Returns:
            list: List of dictionaries, each containing 'text' and 'label' of an entity.

        Notes:
            Logs the extraction process and any warnings for empty/invalid input.
        """
        logger.info(f"Extracting entities from text: '{text[:50]}...'")
        if not text or not isinstance(text, str):
            logger.warning("Empty or invalid text provided for entity extraction")
            return []
        
        doc = self.nlp(text)
        entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
        logger.info(f"Detected entities: {entities}")
        return entities

    def setup_model(self) -> None:
        """Set up the SpaCy model for NER.

        Loads the 'en_core_web_sm' model, downloading it if not available.

        Raises:
            OSError: If model loading or download fails (handled internally with logging).
        """
        try:
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("Loaded SpaCy model 'en_core_web_sm' successfully")
        except OSError:
            logger.warning("Model 'en_core_web_sm' not found. Downloading...")
            spacy.cli.download("en_core_web_sm")
            logger.info("Downloaded and loaded 'en_core_web_sm'")
