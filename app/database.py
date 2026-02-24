import psycopg
# psycopg is the PostgreSQL driver for Python. Without it, Python cannot talk to Postgres.
# The bridge between Python and your Supabase Postgres database.

class Database:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def connect(self):
        return psycopg.connect(self.connection_string)  #This opens a new connection to the database using the URI.

    def insert_job(self, title: str, description: str, embedding, url=None, source=None):
        with self.connect() as conn:  #Open connection, run block, auto-close connection. This is a context manager.
            with conn.cursor() as cur:  #Database connection gives you a cursor. The cursor is what you use to execute SQL commands.
                cur.execute(
                    """
                    INSERT INTO jobs (title, description, embedding, url, source)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (title, description, embedding.tolist(), url, source)
                )
                conn.commit()
    def insert_resume(self, name, content, embedding, skills=None, experience_level=None, tech_stack=None, locations=None, job_preferences=None):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO resumes (name, content, embedding, skills, experience_level, tech_stack, locations, job_preferences)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        name,
                        content,
                        embedding.tolist(),
                        skills,
                        experience_level,
                        tech_stack,
                        locations,
                        job_preferences
                    )
                )
                conn.commit()

    def fetch_jobs(self):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, title, description, url, embedding FROM jobs")
                return cur.fetchall()  #returns a list of tuples,

    def get_latest_resume(self):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, name, content, embedding, skills, experience_level, tech_stack, locations, job_preferences
                    FROM resumes
                    ORDER BY id DESC
                    LIMIT 1
                    """
                )
                row = cur.fetchone()
                if row is None:
                    return None
                return {
                    "id": row[0],
                    "name": row[1],
                    "content": row[2],
                    "embedding": row[3],
                    "skills": row[4],
                    "experience_level": row[5],
                    "tech_stack": row[6],
                    "locations": row[7],
                    "job_preferences": row[8],
                }

    def find_similar_jobs(self, embedding, top_n=3):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, title, description, url, embedding,
                    (embedding <#> %s::vector) AS distance
                    FROM jobs
                    ORDER BY distance ASC
                    LIMIT %s
                    """,
                    (embedding.tolist(), top_n)
                )
                results = cur.fetchall()  # Fetch all results while cursor is open
        return results  # Return after cursor/connection are closed
    
    def get_notified_jobs(self):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT job_id FROM notified_jobs")
                return cur.fetchall()

    def mark_job_as_notified(self, job_id):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO notified_jobs (job_id) VALUES (%s) ON CONFLICT DO NOTHING", (job_id,))
                conn.commit()
                return cur.rowcount > 0  # Returns True if a new row was inserted, False if it already existed
            
#Key part: %s::vector tells Postgres to treat the parameter as a vector type.