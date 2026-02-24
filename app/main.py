from app.embeddings import EmbeddingModel
import numpy as np
from app.database import Database
from dotenv import load_dotenv
from app.llm_utils import get_explanation
import os

def cosine_similarity(vec1, vec2):  # Cosine similarity is a measure of similarity between two non-zero vectors in an inner product space. It is defined as the cosine of the angle between them, which ranges from -1 to 1. A value of 1 indicates that the vectors are identical, while a value of -1 indicates that they are completely opposite. A value of 0 indicates that the vectors are orthogonal (i.e., they have no similarity).
    return np.dot(vec1, vec2) / (
        np.linalg.norm(vec1) * np.linalg.norm(vec2)
    )



if __name__ == "__main__":
    model = EmbeddingModel()
    CONNECTION_STRING = os.getenv("CONNECTION_STRING")
    print(f"Connecting to database with URI: {CONNECTION_STRING}")
    db = Database(CONNECTION_STRING)
    # 3. Your resume text
    resume = "Python backend developer with FastAPI experience."
    # 4. Convert resume to embedding
    resume_embedding = model.encode(resume)

    # 5. Query the database for similar jobs
    top_jobs = db.find_similar_jobs(resume_embedding, top_n=3)

    # 6. Print the results
    for job in top_jobs:
        job_id, title, description, embedding, distance = job
        explanation = get_explanation(resume, description)
        print(f"Job: {title}\nDescription: {description}\nDistance: {distance:.4f}")
        print(f"Why this matches: {explanation}\n")
#     ("Frontend Engineer", "Seeking a frontend engineer skilled in React and TypeScript."),
#     ("Data Scientist", "Data scientist needed with experience in Python and machine learning."),
#     ("Graphic Designer", "Graphic designer skilled in Photoshop and Illustrator."),
#     ("Backend Developer (Node.js)", "Backend developer with Node.js and MongoDB experience."),
#    ]

#     for title, description in jobs:
#         embedding = model.encode(description)
#         db.insert_job(title, description, embedding)
#         print(f"Inserted: {title}")


    # print("Job inserted into database with embedding.")