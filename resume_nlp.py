# resume_nlp.py

import spacy
import re

COMMON_SKILLS = {
    "python", "java", "c++", "sql", "javascript", "react", "node.js",
    "html", "css", "machine learning", "deep learning", "git", "docker",
    "kubernetes", "flask", "django", "pandas", "numpy", "aws", "azure"
}

nlp = spacy.load("en_core_web_sm")

def extract_skills(text):
    doc = nlp(text.lower())
    found_skills = set()

    for token in doc:
        if token.text in COMMON_SKILLS:
            found_skills.add(token.text)

    # check for multi word phrases
    for chunk in doc.noun_chunks:
        chunk_text = chunk.text.strip().lower()
        if chunk_text in COMMON_SKILLS:
            found_skills.add(chunk_text)

    return list(found_skills)

def extract_years_of_experience(text):
    matches = re.findall(r'(\d{1,2})\s*\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience)?', text.lower())
    years = [int(m) for m in matches if m.isdigit()]
    return max(years) if years else None

def extract_resume_features(text):
    return {
        "skills": extract_skills(text),
        "experience_years": extract_years_of_experience(text)
    }
