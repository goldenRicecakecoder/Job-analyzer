import spacy
from collections import Counter
import re
import json
from pathlib import Path


keywords_path = Path(__file__).parent / "keywords.json"
with open(keywords_path, "r") as f:
    keyword_sets = json.load(f)

tool_keywords = set(keyword_sets["tool_keywords"])
tech_keywords = set(keyword_sets["tech_keywords"])
soft_skills = set(keyword_sets["soft_skills"])


nlp = spacy.load("en_core_web_sm")

def extract_keywords(text, limit=20):
    doc = nlp(text)
    keywords = []
    for token in doc:
        if token.pos_ in {"NOUN", "PROPN", "ADJ"} and not token.is_stop and token.is_alpha:
            word = token.lemma_.lower()
            if word.endswith("s") and len(word) > 3:
                word = word[:-1]
            keywords.append(word)
    return Counter(keywords).most_common(limit)

def extract_experience_phrases(text):
    pattern = r'(?i)(?:at least |minimum |up to |over |more than |[a-z]*\s)?\d+\+?\s+years?'
    matches = re.findall(pattern, text)
    return [match.strip().capitalize() for match in matches]

def classify_keywords(keywords):
    classified = {
        "tools": [],
        "tech": [],
        "soft_skills": [],
        "other": []
    }
    for word, count in keywords:
        if word in tool_keywords:
            classified["tools"].append((word, count))
        elif word in tech_keywords:
            classified["tech"].append((word, count))
        elif word in soft_skills:
            classified["soft_skills"].append((word, count))
        else:
            classified["other"].append((word, count))
    return classified

def group_keywords(keywords):
    grouped = {"TOOLS": [], "TECH": [], "SOFT_SKILLS": [], "OTHER": []}
    for kw in keywords:
        lower_kw = kw.lower()
        if lower_kw in tool_keywords:
            grouped["TOOLS"].append(lower_kw)
        elif lower_kw in tech_keywords:
            grouped["TECH"].append(lower_kw)
        elif lower_kw in soft_skills:
            grouped["SOFT_SKILLS"].append(lower_kw)
        else:
            grouped["OTHER"].append(lower_kw)
    return grouped

if __name__ == "__main__":
    job_description = """
    We are seeking a passionate and experienced Senior Backend Engineer with at least 5 years of hands-on experience designing scalable APIs and working with cloud-native systems.

    Candidates must have strong knowledge of Python (minimum 3 years), Flask, and PostgreSQL. Experience with AWS (S3, Lambda, EC2), Docker, and Terraform is highly preferred.

    You’ll be contributing to a microservices architecture and collaborating with cross-functional teams in a fast-paced, agile environment. 2+ years of experience in CI/CD pipelines (Jenkins, GitHub Actions) and container orchestration tools like Kubernetes are a must.

    Ideal candidates will be team players with excellent communication skills, strong attention to detail, and a willingness to take ownership of backend modules. Experience mentoring junior engineers or leading initiatives is a bonus.

    Bonus points for familiarity with monitoring stacks like Datadog or New Relic, async programming, and Redis-based caching.
    """

    print("Top Keywords:")
    print(extract_keywords(job_description))

    print("\nExperience Phrases:")
    print(extract_experience_phrases(job_description))

    print("\nGrouped Keywords:")
    classified = classify_keywords(extract_keywords(job_description))
    for category, items in classified.items():
        print(f"\n{category.upper()}:")
        for word, count in items:
            print(f"- {word} ({count})")

    print("\nExtracted Keywords (raw):")
    for word, count in extract_keywords(job_description):
        print(word)

    print("\nRaw Lemmas from SpaCy:")
    for token in nlp(job_description):
        if token.pos_ in {"NOUN", "PROPN", "ADJ"} and not token.is_stop and token.is_alpha:
            print(token.lemma_.lower())
