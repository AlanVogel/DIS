import re

def sanitize_input(text: str) -> str:
    """Sanitize input text by removing special characters.

    Removes angle brackets, semicolons, and curly braces from the input text
    to prevent potential security issues or formatting errors.

    Args:
        text (str): Input text to sanitize.

    Returns:
        str: Sanitized text with special characters removed and stripped of whitespace.
    """
    return re.sub(r"[<>;{}]", "", text).strip()
