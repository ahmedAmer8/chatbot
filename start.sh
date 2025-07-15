#!/bin/bash
echo "Starting FastAPI server..."
python -m uvicorn main:app --host 0.0.0.0 --port 8000 &

echo "Waiting for API to start..."
sleep 5

echo "Starting Gradio frontend..."
python frontend/gradio_app.py