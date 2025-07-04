import spacy

class NERService:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def extract_entities(self, text: str) -> list:
        doc = self.nlp(text)
        return [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
