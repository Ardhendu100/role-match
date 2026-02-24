# orchestration/nodes.py
"""
Defines each node (step) in the LangGraph workflow.
Each node is a function that takes and returns a context dict.
"""

from app.database import Database
from app.match_utils import get_top_matches
from dotenv import load_dotenv
import os
from scripts.send_mail import send_email
from scripts.job_fetchers import RemoteOKFetcher, aggregate_jobs
from app.embeddings import EmbeddingModel

load_dotenv()
CONNECTION_STRING = os.getenv("CONNECTION_STRING")

def fetch_jobs_node(context):
    print("[LangGraph] Fetching jobs...")
    try:
        db = Database(CONNECTION_STRING)
        fetchers = [RemoteOKFetcher(db)]
        jobs = aggregate_jobs(fetchers)
        context["jobs"] = jobs
        model = EmbeddingModel()
        for job in jobs:
            embedding = model.encode(job["description"])
            # Add url and source if your db.insert_job supports them
            db.insert_job(
                job["title"],
                job["description"],
                embedding,
                url=job.get("url"),
                source="RemoteOK",
            )

        print(f"[LangGraph] Jobs fetched: {len(jobs)}")

    except Exception as e:
        print(f"[LangGraph] Error fetching jobs: {e}")
        context["jobs"] = []
    return context

def match_jobs_node(context):
    print("[LangGraph] Matching jobs...")
    try:
        db = Database(CONNECTION_STRING)
        matches = get_top_matches(db, top_n=5)
        context["matches"] = matches
        print(f"[LangGraph] Jobs matched: {len(matches)}")
    except Exception as e:
        print(f"[LangGraph] Error matching jobs: {e}")
        context["matches"] = []
    return context

def notify_node(context):
    print("[LangGraph] Notifying user...")
    matches = context.get("matches", [])
    if not matches:
        print("[LangGraph] No matches to notify.")
        context["email_sent"] = False
        return context
    try:
        all_content = "\n".join([
            f"{m['title']} (Score: {m['distance']:.2f})\nWhy fit: {m['explanation']}\nURL: {m.get('url', 'N/A')}\n-----------------------------" for m in matches
        ])
        print("[LangGraph] Email content:\n", all_content)
        send_email("Your Job Matches", all_content, "ardhendusekharsahoo31@gmail.com")
        context["email_sent"] = True
        print("[LangGraph] Email sent successfully.")
    except Exception as e:
        print(f"[LangGraph] Error sending email: {e}")
        context["email_sent"] = False
    return context