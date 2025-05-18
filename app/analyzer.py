import spacy
from collections import Counter

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    """
    Extracts the most common nouns and proper nouns from the input text.
    """
    doc = nlp(text)
    keywords = [
        token.text.lower()
        for token in doc
        if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop
    ]
    return Counter(keywords).most_common(10)

# Optional test run
if __name__ == "__main__":
    jd = """
    We are looking for a backend Python developer with experience in Flask, SQL, and REST APIs.
    Experience with Docker and AWS is a plus. Must have 3+ years of experience.
    """
    print(extract_keywords(jd))
