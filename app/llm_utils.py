import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def build_prompt(resume, job):
    return (
        f"Given the following resume and job description, explain in 2-3 short, direct bullet points why this job is a good match for the candidate. "
        "Focus only on the most relevant skills, experience, or preferences that make this job a fit. "
        "Be concise and convincing, as if explaining to the candidate. "
        "Do not include extra text, just the bullet points.\n\n"
        f"Resume:\n{resume}\n\nJob Description:\n{job}\n"
        "Output as a plain text bullet list."
    )

def get_explanation(resume, job):
    prompt = build_prompt(resume, job)
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        max_tokens=256,
    )
    return chat_completion.choices[0].message.content


def extract_resume_info(resume_text):
    """
    Uses the LLM to extract structured info from a resume.
    Returns a dict with keys: skills, experience_level, tech_stack, locations, job_preferences.
    """
    prompt = (
        "Extract the following information from this resume. "
        "Respond ONLY with a valid JSON object, no markdown, no explanation, no extra text., "
        "Keys: skills (list), experience_level (string), tech_stack (list), locations (list), job_preferences (list of desired job titles/roles)."
        "Resume:\n"
        f"{resume_text}\n"
    )
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        max_tokens=512,
    )
    import json
    # Try to parse the LLM output as JSON
    try:
        return json.loads(chat_completion.choices[0].message.content)
    except Exception:
        # If parsing fails, return the raw output for debugging
        return {"raw_output": chat_completion.choices[0].message.content}