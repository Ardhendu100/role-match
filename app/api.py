from fastapi import FastAPI, Body, Request
from pydantic import BaseModel
from app.embeddings import EmbeddingModel
from app.database import Database
import os
from app.llm_utils import get_explanation
import numpy as np
import json
from app.match_utils import get_top_matches

app = FastAPI()
model = EmbeddingModel()
CONNECTION_STRING = os.getenv("CONNECTION_STRING")
db = Database(CONNECTION_STRING)
class ResumeRequest(BaseModel):
    resume: str

@app.post("/match")
def match_resume():
    # 1. Fetch the latest resume from the database
    results = get_top_matches(db, top_n=5)
    # 5. Return results as JSON
    return {"matches": results}

@app.get("/jobs")
def get_jobs():
    jobs = db.fetch_jobs()
    # jobs is a list of tuples: (id, title, description, url, embedding)
    job_list = []
    for job in jobs:
        print("Fetched job from DB:", job)  # Debug print
        job_id, title, description, url, embedding = job
        job_list.append({
            "job_id": job_id,
            "title": title,
            "description": description,
            "url": url,
            # Optionally, add more fields if needed
        })
    return {"jobs": job_list}

@app.get("/job-preferences")
def get_job_preferences():
    resume = db.get_latest_resume()
    job_preferences = []
    if resume and resume.get("job_preferences"):
        print("Found resume with job_preferences:", resume["job_preferences"])
        job_preferences = resume["job_preferences"]
    return {"job_preferences": job_preferences}

@app.post("/job-preferences")
async def update_job_preferences(request: Request):
    data = await request.json()
    job_preferences = data.get("job_preferences", [])
    resume = db.get_latest_resume()
    if not resume:
        return {"error": "No resume found"}
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE resumes SET job_preferences = %s WHERE id = %s",
                (json.dumps(job_preferences), resume["id"])
            )
            conn.commit()
    return {"success": True}
# To run this FastAPI app, use: uvicorn app.api:app --reload