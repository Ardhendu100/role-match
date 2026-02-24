import numpy as np
import json
from app.llm_utils import get_explanation

def get_top_matches(db, top_n=5):
    # Fetch latest resume and its embedding
    resume_record = db.get_latest_resume()
    if not resume_record:
        return []
    resume_text = resume_record["content"]
    resume_embedding = resume_record["embedding"]
    if isinstance(resume_embedding, str):
        resume_embedding = np.array(json.loads(resume_embedding))
    # Find top jobs by vector similarity
    top_jobs = db.find_similar_jobs(resume_embedding, top_n=top_n)
    results = []
    for job in top_jobs:
        job_id, title, description, url, embedding, distance = job
        explanation = get_explanation(resume_text, description)
        results.append({
            "job_id": job_id,
            "title": title,
            "description": description,
            "distance": distance,
            "explanation": explanation,
            "url": url,
            # Add more fields if needed (e.g., url)
        })
    return results