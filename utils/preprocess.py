import re

def clean_text(text):
    """
    Cleans text by removing special characters, multiple spaces,
    and making it lowercase.
    """
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
