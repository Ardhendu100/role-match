1️⃣ What is Pydantic?
Pydantic is a Python library for data validation and settings management using Python type annotations.
It lets you define data models (classes) that automatically check and parse input data (like JSON from an API request).


2️⃣ Why Do We Use Pydantic with FastAPI?
FastAPI uses Pydantic models to define the shape and types of data it expects in requests and responses.
When a user sends data (like a resume) to your API, Pydantic:
Validates the data (e.g., checks that a field is a string, not a number)
Converts it to a Python object you can use in your code
Returns clear errors if the data is missing or wrong

What About Body from FastAPI?
Body is used to declare that a parameter should come from the request body (not from the URL or query string).

🏆 Interview-Ready Insight
“Pydantic lets me define and validate the structure of my API’s input and output data, making my FastAPI endpoints safe, clear, and self-documenting.”