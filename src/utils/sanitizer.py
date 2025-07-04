import re

def sanitize_input(text: str) -> str:
    return re.sub(r"[<>;{}]", "", text).strip()
