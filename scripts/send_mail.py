import yagmail, os
from app.database import Database
from app.match_utils import get_top_matches
from dotenv import load_dotenv
load_dotenv()

def send_email(subject, body, to_email):
    yag = yagmail.SMTP(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
    yag.send(to=to_email, subject=subject, contents=body)

def notify_new_matches():
    CONNECTION_STRING = os.getenv("CONNECTION_STRING")
    db = Database(CONNECTION_STRING)
    matches = get_top_matches(db, top_n=5)
    notified_ids = set(db.get_notified_jobs())

    new_matches = []
    for match in matches:
        job_id = match["job_id"]
        # If job_id is UUID, store as string
        if isinstance(job_id, bytes):
            job_id = job_id.hex
        elif not isinstance(job_id, str):
            job_id = str(job_id)
        if job_id not in notified_ids:
            # Compose concise content for this job
            subject = f"Job Match: {match['title']} (Score: {match['distance']:.2f})"
            short_expl = match['explanation'].replace("\n", " ")  # Make explanation one line
            url = match.get('url', 'N/A')
            content = (
                f"{subject}\n"
                f"Why fit: {short_expl}\n"
                f"URL: {url}\n"
                "-----------------------------\n"
            )
            new_matches.append(content)
            db.mark_job_as_notified(job_id)

    # Send all new match notifications in one email
    if new_matches:
        all_content = "\n".join(new_matches)
        send_email("Your Job Matches", all_content, "ardhendusekharsahoo31@gmail.com")


if __name__ == "__main__":
    notify_new_matches()