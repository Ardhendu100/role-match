import numpy as np  # For vector math (cosine similarity)
from app.embeddings import EmbeddingModel

model = EmbeddingModel()

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


resume = "Python backend developer with FastAPI experience."  # Your resume as a string

jobs = [
    "Looking for a backend developer with FastAPI and PostgreSQL experience.",
    "Frontend engineer with React and TypeScript skills.",
    "Data scientist with experience in Python and machine learning.",
    "Graphic designer skilled in Photoshop and Illustrator.",
    "Backend developer with Node.js and MongoDB experience."
]

# resume_embedding = model.encode(resume)  # Converts resume to a vector
# job_embeddings = [model.encode(job) for job in jobs]  # Converts each job to a vector

# similarities = [cosine_similarity(resume_embedding, job_emb) for job_emb in job_embeddings]

# ranked_jobs = sorted(zip(jobs, similarities), key=lambda x: x[1], reverse=True)  # Sort by similarity, highest first

# for job, score in ranked_jobs:
#     print(f"Job: {job}\nSimilarity: {score:.2f}\n")


def get_top_jobs(resume, jobs, top_n=3):
    resume_embedding = model.encode(resume)  # Converts resume to a vector
    job_embeddings = [model.encode(job) for job in jobs]  # Converts each job to a vector
    similarities = [cosine_similarity(resume_embedding, job_emb) for job_emb in job_embeddings]  
    ranked_jobs = sorted(zip(jobs, similarities), key=lambda x: x[1], reverse=True)  # Sort by similarity, highest first
    
    return ranked_jobs[:top_n]  # return only top N jobs by default top 3


result = get_top_jobs(resume, jobs, 4)
print("Top matching jobs:")
for job, score in result:
    print(f"Job: {job}\nSimilarity: {score:.2f}\n")

# Output

# Job: Looking for a backend developer with FastAPI and PostgreSQL experience.
# Similarity: 0.70

# Job: Data scientist with experience in Python and machine learning.
# Similarity: 0.44

# Job: Backend developer with Node.js and MongoDB experience.
# Similarity: 0.42

# Job: Frontend engineer with React and TypeScript skills.
# Similarity: 0.30

# Job: Graphic designer skilled in Photoshop and Illustrator.
# Similarity: 0.15