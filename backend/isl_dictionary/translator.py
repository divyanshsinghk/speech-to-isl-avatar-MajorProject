import json
import os

BASE_DIR = os.path.dirname(__file__)

# Load dictionaries
with open(os.path.join(BASE_DIR, "sentence_signs.json")) as f:
    SENTENCE_SIGNS = json.load(f)

with open(os.path.join(BASE_DIR, "word_signs.json")) as f:
    WORD_SIGNS = json.load(f)

def translate_gloss(gloss: str):
    """
    Converts gloss into a list of sign tokens.
    """
    gloss = gloss.strip().upper()

    # 1️⃣ Sentence-level sign
    if gloss in SENTENCE_SIGNS:
        return [SENTENCE_SIGNS[gloss]]

    signs = []

    # 2️⃣ Word-level or fingerspelling
    for word in gloss.split():
        if word in WORD_SIGNS:
            signs.append(WORD_SIGNS[word])
        else:
            # 3️⃣ Fingerspelling fallback
            for letter in word:
                signs.append(f"FS_{letter}")

    return signs

def translate_to_fingerspelling(text: str):
    """
    Converts input text into ISL fingerspelling tokens.
    Example: 'RONNET' -> ['FS_R', 'FS_O', 'FS_N', 'FS_N', 'FS_E', 'FS_T']
    """
    text = text.upper()
    signs = []

    for char in text:
        if char.isalpha():
            signs.append(f"FS_{char}")
        elif char == " ":
            signs.append("PAUSE")

    return signs
