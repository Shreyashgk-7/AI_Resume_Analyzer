import re
from utils.filters import STOPWORDS, ROLES
from utils.rmp import RMP_SKILLS

def normalize_text(text):
    text = text.lower()
    # Keep + and #, remove all other punctuation
    text = re.sub(r"[^\w\s+#]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_skills_section(text):
    skills_text = ""
    lines = text.splitlines()
    capture = False
    for line in lines:
        line_clean = line.strip().lower()
        if line_clean.startswith("skills"):
            capture = True
            continue
        elif line_clean in ["personal information", "education", "projects",
                            "experience", "certifications", "languages"]:
            capture = False
        if capture:
            skills_text += " " + line
    return normalize_text(skills_text)

def filter_words(words):
    """Remove stopwords and role words, but keep any word present in RMP_SKILLS."""
    filtered = []
    for w in words:
        w_norm = normalize_text(w)
        # Keep word if it's in RMP_SKILLS, otherwise remove if stopword or role
        if any(normalize_text(skill) == w_norm for skill in RMP_SKILLS):
            filtered.append(w)
        elif w not in STOPWORDS and w not in ROLES:
            filtered.append(w)
    return filtered

def extract_valid_skills(text):
    """Detect multi-word and single-word skills from text."""
    detected = []
    normalized_text = normalize_text(text)

    # First check all multi-word skills in RMP_SKILLS
    for skill in RMP_SKILLS:
        skill_norm = normalize_text(skill)
        # Use word boundaries to match exact phrases
        if re.search(r"\b" + re.escape(skill_norm) + r"\b", normalized_text):
            detected.append(skill)

    # Then check remaining words individually
    words = normalized_text.split()
    for w in words:
        if w not in STOPWORDS and w not in ROLES:
            # Avoid duplicates if part of multi-word skill
            if not any(normalize_text(w) in normalize_text(s) for s in detected):
                detected.append(w)

    return list(set(detected))

def compare_skills(resume_text, jd_text):
    resume_skills_text = extract_skills_section(resume_text)
    resume_skills = extract_valid_skills(resume_skills_text)

    jd_skills_text = normalize_text(jd_text)
    jd_skills = extract_valid_skills(jd_skills_text)

    matched_skills = list(set(resume_skills) & set(jd_skills))
    missing_skills = list(set(jd_skills) - set(resume_skills))
    extra_resume_skills = list(set(resume_skills) - set(jd_skills))

    score = round((len(matched_skills) / len(jd_skills) * 100), 2) if jd_skills else 0.0

    return {
        "Detected Skills": resume_skills,
        "Matched Skills": matched_skills,
        "Missing Skills": missing_skills,
        "Extra Resume Skills": extra_resume_skills,
        "Score": score
    }
