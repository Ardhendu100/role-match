import requests
from datetime import datetime, timezone, timedelta
import os, json
from app.embeddings import EmbeddingModel
from app.database import Database
from dotenv import load_dotenv

load_dotenv()

class JobFetcher:
    def fetch_jobs(self):
        raise NotImplementedError("Subclasses must implement fetch_jobs")
    
    # It defines a method fetch_jobs that every job source must implement.
    # If you try to use JobFetcher directly, it will raise an error—forcing you to create a subclass for each job source.

class RemoteOKFetcher(JobFetcher):
    def __init__(self, db):
        self.db = db

    def fetch_jobs(self):
        url = "https://remoteok.com/api"
        jobs = requests.get(url).json()
        job_list = []
        today = (datetime.now(timezone.utc) - timedelta(days=1)).date()
        resume = self.db.get_latest_resume()
        job_preferences = []
        if resume and resume.get("job_preferences"):
            print("Found resume with job_preferences:", resume["job_preferences"])
            job_preferences = resume["job_preferences"]
        print("Filtering jobs using job_preferences:", job_preferences)
        for job in jobs[1:]:
            title = job.get("position", "")
            description = job.get("description", "")
            date_str = job.get("date", "")
            url = job.get("url", "")
            # Parse date
            try:
                job_date = datetime.fromisoformat(date_str).date()
            except Exception:
                continue  # Skip if date is invalid
            # Filter: keyword and today only
            # Extract keywords from preferences (e.g., 'developer', 'engineer', etc.)
            preference_keywords = [word.lower() for pref in job_preferences for word in pref.split()]
            if any(keyword in title.lower() for keyword in preference_keywords) and job_date == today:
                job_list.append({
                    "title": title,
                    "description": description,
                    "url": url,
                    "date": date_str
                })
        print(f"Fetched {len(job_list)} software jobs from RemoteOK posted today.")
        return job_list

def aggregate_jobs(fetchers):
    all_jobs = []
    for fetcher in fetchers:
        jobs = fetcher.fetch_jobs()
        all_jobs.extend(jobs)
    return all_jobs

if __name__ == "__main__":
    CONNECTION_STRING = os.getenv("CONNECTION_STRING")
    print(f"Connecting to database with URI: {CONNECTION_STRING}")
    db = Database(CONNECTION_STRING)

    fetchers = [RemoteOKFetcher(db)]
    jobs = aggregate_jobs(fetchers)
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
        print(f"Inserted: {job['title']}")







# 🏆 Interview-Ready Insight
# “I designed my job aggregation pipeline with a base fetcher class and source-specific subclasses, so it’s easy to add new APIs or feeds in the future. This modular approach is scalable and maintainable.”