#!/bin/bash
# Install dependencies if not installed (uncomment if needed)
# pip install -r requirements.txt

# Run the FastAPI server via Uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
