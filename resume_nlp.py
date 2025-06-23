# enhanced_resume_nlp.py

import spacy
import re
from collections import Counter
import logging

logger = logging.getLogger(__name__)

# Enhanced skill categories
TECHNICAL_SKILLS = {
    # Programming Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "php", "ruby", "go", "rust",
    "swift", "kotlin", "scala", "r", "matlab", "sql", "nosql", "html", "css", "sass", "less",
    
    # Frameworks & Libraries
    "react", "angular", "vue.js", "node.js", "express.js", "django", "flask", "spring", "laravel",
    "react native", "flutter", "xamarin", "jquery", "bootstrap", "tailwind css",
    
    # Databases
    "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "cassandra", "oracle", "sqlite",
    "dynamodb", "firebase", "mariadb",
    
    # Cloud & DevOps
    "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "jenkins", "git", "github",
    "gitlab", "bitbucket", "ci/cd", "terraform", "ansible", "vagrant", "linux", "ubuntu",
    
    # Data Science & ML
    "machine learning", "deep learning", "artificial intelligence", "data science", "pandas",
    "numpy", "scipy", "scikit-learn", "tensorflow", "pytorch", "keras", "opencv", "nltk",
    "spacy", "matplotlib", "seaborn", "tableau", "power bi",
    
    # Mobile Development
    "ios", "android", "react native", "flutter", "xamarin", "cordova", "phonegap",
    
    # Testing
    "selenium", "junit", "pytest", "jest", "cypress", "postman", "swagger",
    
    # Others
    "rest api", "graphql", "microservices", "agile", "scrum", "kanban", "jira", "confluence",
    "blockchain", "solidity", "web3", "ethereum"
}

SOFT_SKILLS = {
    "leadership", "teamwork", "communication", "problem solving", "analytical", "creative",
    "adaptable", "flexible", "organized", "detail oriented", "time management", "multitasking",
    "project management", "team player", "collaborative", "innovative", "strategic thinking",
    "customer service", "presentation", "negotiation", "mentoring", "coaching"
}

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logger.warning("spaCy model 'en_core_web_sm' not found. Please install it with: python -m spacy download en_core_web_sm")
    nlp = None


def extract_skills(text):
    """Enhanced skill extraction with better pattern matching"""
    text_lower = text.lower()
    found_technical = set()
    found_soft = set()
    
    # Direct matching for technical skills
    for skill in TECHNICAL_SKILLS:
        # Use word boundaries for better matching
        pattern = r'\b' + re.escape(skill.replace('.', r'\.')) + r'\b'
        if re.search(pattern, text_lower):
            found_technical.add(skill)
    
    # Direct matching for soft skills
    for skill in SOFT_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_soft.add(skill)
    
    # Use spaCy for more sophisticated extraction if available
    if nlp:
        try:
            doc = nlp(text_lower)
            
            # Extract from noun chunks
            for chunk in doc.noun_chunks:
                chunk_text = chunk.text.strip()
                if chunk_text in TECHNICAL_SKILLS:
                    found_technical.add(chunk_text)
                elif chunk_text in SOFT_SKILLS:
                    found_soft.add(chunk_text)
            
            # Extract compound skills (e.g., "machine learning", "data science")
            for i in range(len(doc) - 1):
                bigram = f"{doc[i].text} {doc[i+1].text}"
                if bigram in TECHNICAL_SKILLS:
                    found_technical.add(bigram)
                elif bigram in SOFT_SKILLS:
                    found_soft.add(bigram)
        except Exception as e:
            logger.warning(f"Error in spaCy processing: {e}")
    
    return {
        "technical": list(found_technical),
        "soft": list(found_soft),
        "all": list(found_technical | found_soft)
    }


def extract_experience(text):
    """Enhanced experience extraction with multiple patterns"""
    text_lower = text.lower()
    years = []
    
    # Pattern 1: "X years of experience"
    pattern1 = r'(\d{1,2})\s*\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|exp)'
    matches1 = re.findall(pattern1, text_lower)
    years.extend([int(m) for m in matches1 if m.isdigit()])
    
    # Pattern 2: "X+ years in"
    pattern2 = r'(\d{1,2})\s*\+?\s*(?:years?|yrs?)\s*(?:in|with|using)'
    matches2 = re.findall(pattern2, text_lower)
    years.extend([int(m) for m in matches2 if m.isdigit()])
    
    # Pattern 3: Date ranges (e.g., "2020-2023")
    pattern3 = r'(\d{4})\s*[-–]\s*(\d{4}|present|current)'
    matches3 = re.findall(pattern3, text_lower)
    current_year = 2024
    
    for start, end in matches3:
        try:
            start_year = int(start)
            end_year = current_year if end.lower() in ['present', 'current'] else int(end)
            if start_year <= end_year <= current_year and start_year >= 1990:
                years.append(end_year - start_year)
        except ValueError:
            continue
    
    return max(years) if years else 0


def extract_education(text):
    """Extract education information"""
    text_lower = text.lower()
    degrees = []
    
    # Common degree patterns
    degree_patterns = [
        r'\b(bachelor|b\.?[sa]\.?|bs|ba)\b',
        r'\b(master|m\.?[sa]\.?|ms|ma|mba|msc)\b',
        r'\b(phd|ph\.?d\.?|doctorate|doctoral)\b',
        r'\b(associate|diploma|certificate)\b'
    ]
    
    for pattern in degree_patterns:
        matches = re.findall(pattern, text_lower)
        degrees.extend(matches)
    
    # Extract universities/institutions
    university_patterns = [
        r'university of [\w\s]+',
        r'[\w\s]+ university',
        r'[\w\s]+ college',
        r'[\w\s]+ institute'
    ]
    
    institutions = []
    for pattern in university_patterns:
        matches = re.findall(pattern, text_lower)
        institutions.extend([m.strip() for m in matches])
    
    return {
        "degrees": list(set(degrees)),
        "institutions": list(set(institutions))[:5]  # Limit to prevent noise
    }


def extract_contact_info(text):
    """Extract contact information"""
    contact = {}
    
    # Email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    if emails:
        contact['email'] = emails[0]
    
    # Phone
    phone_pattern = r'(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
    phones = re.findall(phone_pattern, text)
    if phones:
        contact['phone'] = ''.join(phones[0])
    
    # LinkedIn
    linkedin_pattern = r'linkedin\.com/in/[\w-]+'
    linkedin_matches = re.findall(linkedin_pattern, text.lower())
    if linkedin_matches:
        contact['linkedin'] = linkedin_matches[0]
    
    # GitHub
    github_pattern = r'github\.com/[\w-]+'
    github_matches = re.findall(github_pattern, text.lower())
    if github_matches:
        contact['github'] = github_matches[0]
    
    return contact


def extract_certifications(text):
    """Extract certifications and licenses"""
    text_lower = text.lower()
    cert_keywords = [
        'certified', 'certification', 'certificate', 'license', 'licensed',
        'aws certified', 'microsoft certified', 'google certified', 'cisco',
        'comptia', 'pmp', 'scrum master', 'agile'
    ]
    
    certifications = []
    for keyword in cert_keywords:
        pattern = rf'\b{re.escape(keyword)}\s+[\w\s]{{1,50}}'
        matches = re.findall(pattern, text_lower)
        certifications.extend([m.strip() for m in matches])
    
    return list(set(certifications))[:10]  # Limit to prevent noise


def calculate_text_quality_score(text):
    """Calculate a quality score for the resume text"""
    score = 0
    
    # Length check
    if len(text) > 1000:
        score += 20
    elif len(text) > 500:
        score += 10
    
    # Sections check
    sections = ['experience', 'education', 'skills', 'projects']
    for section in sections:
        if section in text.lower():
            score += 15
    
    # Professional keywords
    professional_keywords = ['responsible', 'managed', 'developed', 'implemented', 'achieved']
    for keyword in professional_keywords:
        if keyword in text.lower():
            score += 2
    
    # Email and contact info
    if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
        score += 10
    
    return min(score, 100)


def extract_resume_features(text):
    """Main function to extract all features from resume text"""
    if not text or len(text.strip()) < 50:
        return {
            "skills": {"technical": [], "soft": [], "all": []},
            "experience_years": 0,
            "education": {"degrees": [], "institutions": []},
            "contact": {},
            "certifications": [],
            "quality_score": 0,
            "text_length": len(text) if text else 0
        }
    
    try:
        features = {
            "skills": extract_skills(text),
            "experience_years": extract_experience(text),
            "education": extract_education(text),
            "contact": extract_contact_info(text),
            "certifications": extract_certifications(text),
            "quality_score": calculate_text_quality_score(text),
            "text_length": len(text)
        }
        
        return features
    
    except Exception as e:
        logger.error(f"Error extracting features: {e}")
        return {
            "skills": {"technical": [], "soft": [], "all": []},
            "experience_years": 0,
            "education": {"degrees": [], "institutions": []},
            "contact": {},
            "certifications": [],
            "quality_score": 0,
            "text_length": len(text)
        }


def calculate_match_score(jd_features, resume_features):
    """Calculate comprehensive match score between JD and resume"""
    
    # Get skills for comparison
    jd_skills = set(jd_features.get("skills", {}).get("all", []))
    resume_skills = set(resume_features.get("skills", {}).get("all", []))
    
    # Skills matching
    if jd_skills:
        matching_skills = jd_skills.intersection(resume_skills)
        missing_skills = jd_skills - resume_skills
        skill_score = len(matching_skills) / len(jd_skills)
        skill_coverage = len(matching_skills) / len(jd_skills) if jd_skills else 0
    else:
        matching_skills = set()
        missing_skills = set()
        skill_score = 0
        skill_coverage = 0
    
    # Experience matching
    jd_exp = jd_features.get("experience_years", 0) or 0
    resume_exp = resume_features.get("experience_years", 0) or 0
    
    if jd_exp == 0:
        experience_score = 1.0
    elif resume_exp >= jd_exp:
        experience_score = 1.0
    else:
        experience_score = min(resume_exp / jd_exp, 1.0) if jd_exp else 0
    
    # Quality bonus
    quality_bonus = resume_features.get("quality_score", 0) / 1000  # Small bonus for quality
    
    # Calculate total score (weighted)
    total_score = (
        skill_score * 0.6 +           # 60% for skills
        experience_score * 0.3 +      # 30% for experience
        quality_bonus * 0.1           # 10% for quality
    ) * 100
    
    # Additional metrics
    technical_skills_match = len(set(jd_features.get("skills", {}).get("technical", [])).intersection(
        set(resume_features.get("skills", {}).get("technical", []))
    ))
    
    soft_skills_match = len(set(jd_features.get("skills", {}).get("soft", [])).intersection(
        set(resume_features.get("skills", {}).get("soft", []))
    ))
    
    return {
        "total_score": round(total_score, 2),
        "skill_score": round(skill_score * 100, 2),
        "experience_score": round(experience_score * 100, 2),
        "quality_score": resume_features.get("quality_score", 0),
        "matching_skills": list(matching_skills),
        "missing_skills": list(missing_skills),
        "technical_skills_match": technical_skills_match,
        "soft_skills_match": soft_skills_match,
        "skill_coverage": round(skill_coverage * 100, 2),
        "resume_experience": resume_exp,
        "jd_experience_required": jd_exp,
        "experience_gap": max(0, jd_exp - resume_exp)
    }