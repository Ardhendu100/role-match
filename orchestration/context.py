# orchestration/context.py
"""
Defines the context object for LangGraph orchestration.
This is a simple dict that holds all data passed between nodes.
You can extend it to a class if you want more structure.
"""

def create_initial_context():  #Use create_initial_context() to start your workflow with a clean context.
    return {
        "resume": None,
        "jobs": [],
        "matches": [],
        "notified_job_ids": set(),
        "email_sent": False,
    }