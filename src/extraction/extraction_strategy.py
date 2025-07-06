from abc import ABC, abstractmethod

class ExtractionStrategy(ABC):
    """Abstract base class for text extraction strategies.

    Defines the interface for extracting text from different file types.
    Concrete strategies (e.g., PDF, Image) must implement the extract_text method.

    """
    @abstractmethod
    def extract_text(self, file_content: bytes) -> str:
        """Extract text from the given file content.

        Args:
            file_content (bytes): Raw bytes of the file to extract text from.

        Returns:
            str: Extracted text from the file.

        Raises:
            NotImplementedError: If not implemented by a subclass.
        """
        pass
    