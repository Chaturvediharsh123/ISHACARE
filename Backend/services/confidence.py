import re

def calculate_confidence(text, key, value):

    confidence = 1.0

    # Check if keyword exists clearly
    if key.lower() not in text.lower():
        confidence -= 0.3

    # Penalize unrealistic values
    if value < 0:
        confidence -= 0.5

    # OCR noise check (random characters nearby)
    noisy_pattern = r"[^\w\s]"
    if re.search(noisy_pattern, text):
        confidence -= 0.1

    return max(confidence, 0.0)