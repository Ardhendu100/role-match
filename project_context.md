Project: AI Job Matching System
Constraints: 100% free
Stack:
- LLM: Groq (Llama 3)
- Embeddings: sentence-transformers/all-MiniLM-L6-v2 (local CPU)
- DB: Supabase Postgres + pgvector
- Backend: FastAPI
- Orchestration: LangGraph
- Deployment: Docker + Render Free
Goal: Learning-focused, understanding every line of code.



We Split Work Into Separate Threads

You create separate chats for:

1️⃣ Phase 1 – Embeddings Understanding
2️⃣ Phase 2 – Basic Matching Script
3️⃣ Phase 3 – LLM Integration (Groq)
4️⃣ Phase 4 – Database + pgvector
5️⃣ Phase 5 – FastAPI Integration
6️⃣ Phase 6 – Docker + Deployment

Each chat = one clean module.


📚 Your Complete Learning Roadmap
Based on where you are now, here's our phased approach:

Phase	What You'll Learn	Status
Phase 1	Embeddings & Similarity	✅ In Progress
Phase 2	Resume-Job Matching (Local Script)	🔜 Next
Phase 3	LLM Explanation (Groq)	📝 Planned
Phase 4	Database Vector Search	🟡 Partially Done
Phase 5	FastAPI REST API	📝 Planned
Phase 6	LangGraph Orchestration	📝 Planned
Phase 7	Docker + Deployment	📝 Planned



Phase 1 – Embedding Understanding (Very Important)

You will:

Load MiniLM model

Generate embedding for 2 sentences

Compare similarity

Understand cosine similarity

No database.
No API.
Just local script.



Phase 2 – Simple Resume Matching Script

Without FastAPI.

Just:

Hardcoded resume text

Hardcoded job descriptions

Compute similarity

Rank them

You will feel how semantic matching works.



Phase 3 – Add LLM (Groq)

Then we:

Send resume + job to Groq

Generate explanation

Understand prompt structure

Handle JSON output

You will understand:

What is system prompt?

Why structured output?

Why retry logic?


Phase 4 – Add Database

Then:

Store embeddings in Postgres

Use pgvector

Query similarity in SQL

You will understand:

Why store vector in DB?

Why not compute every time?

How indexing works?


Phase 5 – Add FastAPI

Then:

Build API endpoints

Connect all modules

Now it becomes system.

Phase 6 – Docker

Only after you fully understand local system.

Then containerize.













 How Your System Works (Personalized Flow)
Resume Parsing

You upload or point to your resume PDF.
The system extracts text and uses an LLM to parse your skills, experience, and preferences into structured data.
Automated Job Fetching (Cron)

A scheduled script (cron job) runs daily/weekly.
It fetches jobs from public APIs (e.g., RemoteOK), but only keeps jobs matching your extracted skills, locations, or preferences.
Semantic Matching & Explanation

For each new job, the system computes semantic similarity to your resume/profile.
It uses an LLM to generate a clear explanation of why each job is a good match for you.
Email Notification

The system compiles the top matches and explanations into a summary email.
You receive this email automatically, with links to apply.