#!/bin/bash

echo "Starting Sentiment Analysis Backend..."
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt --quiet

# Start the FastAPI server
echo "Starting FastAPI server on http://localhost:8000"
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
