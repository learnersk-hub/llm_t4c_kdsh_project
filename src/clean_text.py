import re

def clean_gutenberg_text(text):
    """
    Removes Project Gutenberg header and keeps only the story.
    Strategy:
    - Find first occurrence of 'CHAPTER'
    - Keep text from there
    """

    # Normalize text
    text = text.replace("\r\n", "\n")

    # Look for CHAPTER (case-insensitive)
    match = re.search(r"\bCHAPTER\s+[IVXLCDM0-9]+\b", text, re.IGNORECASE)

    if match:
        text = text[match.start():]

    return text.strip()
