import requests
from dotenv import load_dotenv
import os
import json
from app.learning.resume_job_matching import get_top_jobs
from groq import Groq


load_dotenv()


client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def build_prompt(resume, job):
    return (
        f"Resume: {resume}\n"
        f"Job Description: {job}\n"
        "Explain in 2-3 bullet points why this job matches the resume. Output as JSON list."
    )


def get_explanation(resume, job):
    prompt = build_prompt(resume, job)
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        max_tokens=256,
    )
    return chat_completion.choices[0].message.content


# --- Example usage ---
resume = "Python backend developer with FastAPI experience."
jobs = [
    "Looking for a backend developer with FastAPI and PostgreSQL experience.",
    "Frontend engineer with React and TypeScript skills.",
    "Data scientist with experience in Python and machine learning.",
    "Graphic designer skilled in Photoshop and Illustrator.",
    "Backend developer with Node.js and MongoDB experience."
]

top_jobs = get_top_jobs(resume, jobs, top_n=3)

for job, score in top_jobs:
    explanation = get_explanation(resume, job)
    print(f"Job: {job}\nSimilarity: {score:.2f}")
    print(f"Explanation: {explanation}\n")