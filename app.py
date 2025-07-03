########################## part1 that uses sqlite ######################

# import os
# import re
# import fitz  # PyMuPDF for PDF
# import spacy
# import sqlite3
# import nltk
# from nltk.corpus import stopwords
# from fuzzywuzzy import process
# from dateutil import parser

# # Download required nltk corpora
# nltk.download('stopwords')

# # Load spaCy NLP model
# nlp = spacy.load("en_core_web_sm")

# # Sample job titles and skills
# JOB_TITLES = ["Data Scientist", "Software Engineer", "ML Engineer", "Product Manager", "AI Researcher"]
# SKILLS = ["Python", "SQL", "Machine Learning", "Deep Learning", "Data Analysis", "TensorFlow", "PyTorch", "NLP"]

# def extract_text_from_file(file_path):
#     """Extract text from PDF or TXT file."""
#     if file_path.endswith(".pdf"):
#         with fitz.open(file_path) as doc:
#             return " ".join(page.get_text() for page in doc)
#     elif file_path.endswith(".txt"):
#         with open(file_path, "r", encoding="utf-8") as f:
#             return f.read()
#     else:
#         raise ValueError("Unsupported file format. Use PDF or TXT.")

# def clean_text(text):
#     """Clean and normalize the text."""
#     text = text.lower()
#     text = re.sub(r"\n+", " ", text)
#     text = re.sub(r"\s+", " ", text)
#     text = re.sub(r"[^a-zA-Z0-9,. ]", "", text)
#     stop_words = set(stopwords.words("english"))
#     words = text.split()
#     return " ".join([w for w in words if w not in stop_words])

# def extract_resume_info(text):
#     """Extract structured info from resume text."""
#     doc = nlp(text)
#     info = {
#         "job_title": None,
#         "skills": [],
#         "experience_years": None,
#         "education": None
#     }

#     # Job title
#     job_matches = [process.extractOne(token.text, JOB_TITLES)[0] for token in doc if token.pos_ == "NOUN"]
#     info["job_title"] = job_matches[0] if job_matches else None

#     # Skills
#     for token in doc:
#         skill_match = process.extractOne(token.text, SKILLS)
#         if skill_match[1] > 80:
#             info["skills"].append(skill_match[0])
#     info["skills"] = list(set(info["skills"]))  # Remove duplicates

#     # Experience
#     exp_match = re.search(r"(\d+)\s+years?", text)
#     if exp_match:
#         info["experience_years"] = int(exp_match.group(1))

#     # Education
#     degrees = ["bachelor", "master", "phd", "associate"]
#     edu_matches = [token.text for token in doc if token.text.lower() in degrees]
#     info["education"] = edu_matches[0] if edu_matches else None

#     return info

# def store_to_db(data, db_name="resumes.db"):
#     """Store extracted data in SQLite DB."""
#     conn = sqlite3.connect(db_name)
#     cursor = conn.cursor()
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS resumes (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             job_title TEXT,
#             skills TEXT,
#             experience_years INTEGER,
#             education TEXT
#         )
#     """)
#     cursor.execute("""
#         INSERT INTO resumes (job_title, skills, experience_years, education)
#         VALUES (?, ?, ?, ?)
#     """, (
#         data["job_title"],
#         ", ".join(data["skills"]),
#         data["experience_years"],
#         data["education"]
#     ))
#     conn.commit()
#     conn.close()

# def process_resume(file_path):
#     """Main function to run the resume ingestion pipeline."""
#     print(f"\nProcessing: {file_path}")
#     text = extract_text_from_file(file_path)
#     cleaned = clean_text(text)
#     extracted = extract_resume_info(cleaned)
#     store_to_db(extracted)
#     print("✅ Resume processed and stored successfully.")
#     print("Extracted Info:", extracted)

# # Example usage
# if __name__ == "__main__":
#     sample_path = input("Enter path to resume (.pdf or .txt): ").strip()
#     if not os.path.exists(sample_path):
#         print("❌ File not found.")
#     else:
#         process_resume(sample_path)


####### part2 using postgres ###########
import os
import re
import fitz
import spacy
import nltk
from nltk.corpus import stopwords
from fuzzywuzzy import process
from database.db_handler import store_resume_to_postgres  # ✅ Import the separated DB logic

# Init spaCy and NLTK
nlp = spacy.load("en_core_web_sm")
nltk.download('stopwords')

# Sample data for matching
JOB_TITLES = ["Data Scientist", "Software Engineer", "ML Engineer", "Product Manager"]
SKILLS = ["Python", "SQL", "Machine Learning", "TensorFlow", "NLP", "Data Analysis"]

def extract_text_from_file(file_path):
    if file_path.endswith(".pdf"):
        with fitz.open(file_path) as doc:
            return " ".join(page.get_text() for page in doc)
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError("Only .pdf or .txt files are supported.")

def clean_text(text):
    text = text.lower()
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-zA-Z0-9,. ]", "", text)
    stop_words = set(stopwords.words("english"))
    return " ".join([word for word in text.split() if word not in stop_words])

def extract_resume_info(text):
    doc = nlp(text)
    info = {
        "job_title": None,
        "skills": [],
        "experience_years": None,
        "education": None
    }

    job_matches = [process.extractOne(token.text, JOB_TITLES)[0] for token in doc if token.pos_ == "NOUN"]
    info["job_title"] = job_matches[0] if job_matches else None

    for token in doc:
        skill_match = process.extractOne(token.text, SKILLS)
        if skill_match[1] > 80:
            info["skills"].append(skill_match[0])
    info["skills"] = list(set(info["skills"]))

    exp_match = re.search(r"(\d+)\s+years?", text)
    if exp_match:
        info["experience_years"] = int(exp_match.group(1))

    degrees = ["bachelor", "master", "phd"]
    edu_matches = [token.text for token in doc if token.text.lower() in degrees]
    info["education"] = edu_matches[0] if edu_matches else None

    return info

def process_resume(file_path):
    print(f"📂 Processing: {file_path}")
    text = extract_text_from_file(file_path)
    cleaned = clean_text(text)
    extracted = extract_resume_info(cleaned)
    store_resume_to_postgres(extracted)  # ✅ Call the external DB handler
    print("📦 Extracted info:", extracted)

# Run the pipeline
if __name__ == "__main__":
    path = input("Enter path to resume (.pdf or .txt): ").strip()
    if not os.path.exists(path):
        print("❌ File not found.")
    else:
        process_resume(path)
