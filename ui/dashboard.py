import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")  # Use env variable for deployed backend

st.title("Role Match Dashboard")

# Fetch all jobs (you may want to create a FastAPI endpoint for this)
@st.cache_data
def fetch_jobs():
    resp = requests.get(f"{API_URL}/jobs")
    return resp.json().get("jobs", [])

# Fetch matches (top matches for your resume)
@st.cache_data
def fetch_matches():
    resp = requests.post(f"{API_URL}/match")
    return resp.json().get("matches", [])

tab1, tab2, tab3 = st.tabs(["Job Preferences", "All Jobs", "Top Matches"])


with tab1:
    st.subheader("Job Preferences")
    # Use session state to persist changes
    if "job_preferences" not in st.session_state:
        resp = requests.get(f"{API_URL}/job-preferences")
        st.session_state.job_preferences = resp.json().get("job_preferences", [])

    job_preferences = st.session_state.job_preferences

    new_pref = st.text_input("Add a new job preference")
    if st.button("Add Preference") and new_pref:
        job_preferences.append(new_pref)
        st.session_state.job_preferences = job_preferences  # Update session state
        st.rerun()  # Rerun to clear input

    remove_indices = []
    for i, pref in enumerate(job_preferences):
        col1, col2 = st.columns([8, 1])
        with col1:
            st.write(pref)
        with col2:
            if st.button("❌", key=f"remove_{i}"):
                remove_indices.append(i)
    for i in sorted(remove_indices, reverse=True):
        job_preferences.pop(i)
        st.session_state.job_preferences = job_preferences  # Update session state
        st.rerun()

    if st.button("Save Preferences"):
        resp = requests.post(f"{API_URL}/job-preferences", json={"job_preferences": job_preferences})
        if resp.status_code == 200:
            st.success("Job preferences updated!")
        else:
            st.error("Failed to update preferences.")

with tab2:
    if st.button("Load All Jobs"):
        jobs = fetch_jobs()
        st.subheader("All Jobs")
        for job in jobs:
            st.markdown(f"**{job['title']}**")
            st.markdown(job['description'], unsafe_allow_html=True)
            st.markdown(f"URL: {job.get('url', 'N/A')}")
            st.markdown("---")

with tab3:
    if st.button("Load Top Matches"):
        matches = fetch_matches()
        st.subheader("Top Matches")
        for match in matches:
            st.markdown(f"**{match['title']}** (Score: {match['distance']:.2f})")
            # st.markdown(match['description'], unsafe_allow_html=True)
            st.markdown("**LLM Explanation:**")
            st.markdown(match['explanation'], unsafe_allow_html=True)
            st.markdown(f"URL: {match.get('url', 'N/A')}")
            st.markdown("---")


# To run this dashboard, save it as `dashboard.py` and run `streamlit run dashboard.py` in your terminal. Make sure your FastAPI server is running and accessible at the specified `API_URL`.