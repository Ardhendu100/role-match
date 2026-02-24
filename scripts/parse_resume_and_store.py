import os
from app.database import Database
from app.embeddings import EmbeddingModel
from app.llm_utils import extract_resume_info  # You’ll write this using RAG/LLM
from dotenv import load_dotenv
import json

load_dotenv()

from PyPDF2 import PdfReader

# 1. Load your resume PDF and extract text
resume_path = "resumes/Ardhendu-sekhar-sahoo.pdf"
reader = PdfReader(resume_path)
resume_text = "\n".join(page.extract_text() for page in reader.pages)

# 2. Use LLM/RAG to extract structured info (skills, experience, etc.)
resume_info = extract_resume_info(resume_text)  # Returns dict with skills, experience, etc.
print("Extracted Resume Info:", resume_info)

# 3. Connect to database and embedding model
db = Database(os.getenv("CONNECTION_STRING"))
model = EmbeddingModel()
embedding = model.encode(resume_text)

# 4. Remove all previous resumes (keep only one record)
def delete_all_resumes(db):
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM resumes")
            conn.commit()

delete_all_resumes(db)

# 5. Insert the new resume
db.insert_resume(
    name="Ardhendu Sekhar Sahoo",
    content=resume_text,
    embedding=embedding,
    skills=json.dumps(resume_info.get("skills")),
    experience_level=resume_info.get("experience_level"),
    tech_stack=json.dumps(resume_info.get("tech_stack")),
    locations=json.dumps(resume_info.get("locations")),
    job_preferences=json.dumps(resume_info.get("job_preferences"))
)

print("Resume parsed, extracted, and stored in database (only one record kept).")


# to run this use python -m scripts.parse_resume_and_store