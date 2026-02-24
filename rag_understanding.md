How RAG Is Used in Your Script
Retrieve:

You extract the full text from your resume PDF.
(Optionally, you could also retrieve a list of common skills, tech stacks, or job titles from a knowledge base or database to provide as context.)
Augment:

You pass the resume text (and any retrieved context, if you add it) to your LLM via the extract_resume_info function.
Generate:

The LLM processes the input and outputs structured information (skills, experience, preferences, etc.) as a dictionary.
Store:

You store the raw text, embedding, and (optionally) the structured info in your database for future use.