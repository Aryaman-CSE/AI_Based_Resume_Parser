import re
import spacy

nlp = spacy.load("en_core_web_sm")

SKILLS = {
    "c", "c++", "cpp", "java", "python", "javascript", "typescript",
    "go", "golang", "rust", "kotlin", "swift", "scala", "ruby",
    "php", "r", "matlab", "sql", "nosql", "bash", "shell", "perl",
    "html", "css", "react", "angular", "vue", "svelte", "nextjs",
    "tailwind", "bootstrap", "graphql", "rest", "restful",
    "node", "nodejs", "spring", "django", "flask", "fastapi",
    "express", "laravel", "rails",
    "pandas", "numpy", "tensorflow", "pytorch", "keras", "scikit-learn",
    "sklearn", "matplotlib", "seaborn", "opencv", "nlp", "llm",
    "kafka", "spark", "hadoop", "aws", "azure", "gcp",
    "s3", "ec2", "lambda", "bigquery", "snowflake", "databricks",
    "linux", "unix", "docker", "kubernetes", "git", "github",
    "gitlab", "jenkins", "terraform", "ansible",
    "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
    "sqlite", "oracle", "cassandra",
}

EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
PHONE_REGEX = r"(?:\+?\d[\d\s\-().]{7,}\d)"
LINKEDIN_REGEX = r"linkedin\.com/in/[\w\-]+"
GITHUB_REGEX = r"github\.com/[\w\-]+"

INVALID_WORDS = {
    "award", "awards", "winner", "winning", "finalist", "hack", "hackathon",
    "project", "projects", "pipeline", "system", "framework", "platform",
    "application", "app", "tool", "tools", "model", "models", "algorithm",
    "solution", "solutions", "module", "modules", "service", "services",
    "api", "apis", "microservice", "microservices",
    "engineer", "engineering", "developer", "development", "software",
    "backend", "frontend", "fullstack", "intern", "internship", "trainee",
    "lead", "manager", "architect", "consultant",
    "best", "top", "rank", "ranking", "achievement", "achievements",
    "certification", "certifications", "certificate", "certified",
    "experience", "experiences", "education", "skills", "skill",
    "technology", "technologies", "tech", "stack",
    "kafka", "spark", "hadoop", "aws", "azure", "gcp", "docker", "kubernetes",
    "react", "angular", "vue", "spring", "django", "flask", "node", "nodejs",
    "java", "python", "javascript", "typescript", "sql", "linux", "unix",
    "college", "university", "institute", "school", "department",
    "bachelor", "master", "degree", "btech", "mtech", "phd",
    "research", "paper", "publication", "conference", "journal",
    "team", "teams", "group", "organization", "company", "startup",
    "role", "roles", "responsibility", "responsibilities",
    "summary", "profile", "objective", "overview",
    "location", "address", "contact", "email", "phone", "resume", "curriculum",
}


def extract_email(text):
    m = re.search(EMAIL_REGEX, text)
    return m.group(0) if m else None


def extract_phone(text):
    m = re.search(PHONE_REGEX, text)
    return m.group(0).strip() if m else None


def extract_linkedin(text):
    m = re.search(LINKEDIN_REGEX, text, re.IGNORECASE)
    return "https://" + m.group(0) if m else None


def extract_github(text):
    m = re.search(GITHUB_REGEX, text, re.IGNORECASE)
    return "https://" + m.group(0) if m else None


def extract_skills(text):
    text_lower = text.lower()
    found = set()
    for skill in SKILLS:
        pattern = r"(?<![a-zA-Z0-9_+#])" + re.escape(skill) + r"(?![a-zA-Z0-9_+#])"
        if re.search(pattern, text_lower):
            found.add(skill)
    return sorted(found)


def extract_name(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    top_text = "\n".join(lines[:25])
    doc = nlp(top_text)

    for ent in doc.ents:
        if ent.label_ != "PERSON":
            continue
        candidate = ent.text.strip()
        if "\n" in candidate:
            continue
        words = candidate.split()
        if not (2 <= len(words) <= 4):
            continue
        bad = any(
            not w.isalpha()
            or w.lower() in SKILLS
            or w.lower() in INVALID_WORDS
            or not w[0].isupper()
            for w in words
        )
        if bad:
            continue
        return candidate

    for line in lines[:10]:
        words = line.strip().split()
        if 2 <= len(words) <= 4 and all(
            w.isalpha() and w[0].isupper()
            and w.lower() not in INVALID_WORDS
            and w.lower() not in SKILLS
            for w in words
        ):
            return line.strip()

    return None


def extract_education(text):
    edu_keywords = [
        "bachelor", "master", "b.tech", "m.tech", "b.e", "m.e",
        "b.sc", "m.sc", "phd", "ph.d", "mba", "degree", "diploma",
        "graduate", "undergraduate", "postgraduate",
    ]
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    education = []
    for i, line in enumerate(lines):
        if any(k in line.lower() for k in edu_keywords):
            block = line
            if i + 1 < len(lines):
                block = line + " — " + lines[i + 1]
            education.append(block)
    seen = set()
    deduped = []
    for e in education:
        if e.lower() not in seen:
            seen.add(e.lower())
            deduped.append(e)
    return deduped


def extract_experience(text):
    year_pattern = re.compile(r"(19|20)\d{2}")
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    experience = []
    for line in lines:
        if year_pattern.search(line) and len(line) > 15:
            lower = line.lower()
            if any(k in lower for k in ["bachelor", "master", "b.tech", "phd", "university", "college"]):
                continue
            experience.append(line)
    return experience[:10]


def parse_resume(text):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "linkedin": extract_linkedin(text),
        "github": extract_github(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience_hints": extract_experience(text),
    }