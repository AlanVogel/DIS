from abc import ABC, abstractmethod

class ExtractionStrategy(ABC):
    @abstractmethod
    def extract_text(self, file_content: bytes) -> str:
        pass
    