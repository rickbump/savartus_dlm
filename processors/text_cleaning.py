import re


def clean_up_transcript(original_text):
    # Fix stuck words where lowercase followed by uppercase (e.g., "wordStuck" -> "word Stuck")
    original_text = re.sub(r'([a-z])([A-Z])', r'\1 \2', original_text)
    # Fix numbers followed by words or vice versa (e.g., "123word" -> "123 word", "word123" -> "word 123")
    original_text = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', original_text)
    original_text = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', original_text)
    # Ensure there's a space after punctuation (e.g., "word,another" -> "word, another")
    original_text = re.sub(r'([.,!?;:])([^\s])', r'\1 \2', original_text)
    original_text = re.sub(r'\s+', ' ', original_text)
    cleaned_text = original_text.strip()
    return cleaned_text
