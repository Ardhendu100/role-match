# Dockerfile for FastAPI backend
# 1. Use official Python image
FROM python:3.12-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of the code
COPY ./app ./app
COPY ./scripts ./scripts
COPY ./orchestration ./orchestration

# 5. Expose port (FastAPI default is 8000)
EXPOSE 8000

# 6. Run FastAPI with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


# for local run ----   docker run -p 8000:8000 --env-file .env rolematch-backend
