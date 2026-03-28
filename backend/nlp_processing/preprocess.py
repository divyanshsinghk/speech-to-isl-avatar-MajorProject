import spacy

nlp = spacy.load("en_core_web_sm")

STOP_WORDS = {
    "am", "is", "are", "was", "were",
    "a", "an", "the",
    "to", "of", "in", "on", "at"
}

def preprocess_text(text):
    """
    Cleans English sentence and returns ISL-ready tokens
    """

    text = text.lower()

    # 🔴 FIX 1: handle negation BEFORE spaCy
    text = text.replace("don't", "dont")
    text = text.replace("can't", "cant")
    text = text.replace("won't", "wont")

    doc = nlp(text)

    tokens = []
    for token in doc:
        if token.is_alpha and token.text not in STOP_WORDS:

            word = token.text.upper()

            # 🔴 FIX 2: preserve negation words
            if word in {"DONT", "CANT", "WONT"}:
                tokens.append(word)
            else:
                tokens.append(token.lemma_.upper())

    return tokens