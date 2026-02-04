import re
import spacy

nlp = spacy.load("en_core_web_sm")

SKILLS = {
    "c", "c++", "cpp", "java", "python", "javascript", "typescript",
    "go", "golang", "rust", "kotlin", "swift", "scala", "ruby",
    "php", "r", "matlab", "sql", "nosql",
    "html", "css", "react", "angular", "vue",
    "node", "nodejs", "spring", "django", "flask",
    "kafka", "spark", "hadoop", "aws", "azure", "gcp",
    "linux", "unix", "docker", "kubernetes"
}

EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
PHONE_REGEX = r"\b\d{10}\b"


def extract_email(text):
    m = re.search(EMAIL_REGEX, text)
    return m.group(0) if m else None


def extract_phone(text):
    m = re.search(PHONE_REGEX, text)
    return m.group(0) if m else None


def extract_skills(text):
    text_lower = text.lower()
    return sorted({s for s in SKILLS if s in text_lower})


def extract_name(text):
    INVALID_WORDS = {
        "award","awards","winner","winning","finalist","hack","hackathon",
        "project","projects","pipeline","system","framework","platform",
        "application","app","tool","tools","model","models","algorithm",
        "solution","solutions","module","modules","service","services",
        "api","apis","microservice","microservices",
        "engineer","engineering","developer","development","software",
        "backend","frontend","fullstack","intern","internship","trainee",
        "lead","manager","architect","consultant",
        "best","top","rank","ranking","achievement","achievements",
        "certification","certifications","certificate","certified",
        "experience","experiences","education","skills","skill",
        "technology","technologies","tech","stack",
        "kafka","spark","hadoop","aws","azure","gcp","docker","kubernetes",
        "react","angular","vue","spring","django","flask","node","nodejs",
        "java","python","c","cpp","c++","javascript","typescript","sql","r",
        "linux","unix","windows","android","ios",
        "college","university","institute","school","department",
        "bachelor","master","degree","btech","mtech","phd",
        "research","paper","publication","conference","journal",
        "team","teams","group","organization","company","startup",
        "role","roles","responsibility","responsibilities",
        "summary","profile","objective","overview",
        "location","address","contact","email","phone"
    }

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

        if not (2 <= len(words) <= 3):
            continue

        bad = False
        for w in words:
            lw = w.lower()
            if not w.isalpha():
                bad = True
                break
            if lw in SKILLS or lw in INVALID_WORDS:
                bad = True
                break
            if not w[0].isupper():
                bad = True
                break

        if bad:
            continue

        return candidate

    return None


def extract_education(text):
    edu_keywords = ["bachelor", "master", "b.tech", "m.tech", "degree"]
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    education = []

    for line in lines:
        lower = line.lower()
        if any(k in lower for k in edu_keywords):
            education.append(line)

    return education


def parse_resume(text):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text)
    }
