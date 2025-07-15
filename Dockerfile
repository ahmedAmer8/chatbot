# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create utils directory (in case it doesn't exist)
RUN mkdir -p utils

# Expose ports
EXPOSE 8000 7860

# Create startup script
RUN echo '#!/bin/bash\n\
echo "Starting FastAPI server..."\n\
python -m uvicorn main:app --host 0.0.0.0 --port 8000 &\n\
\n\
echo "Waiting for API to start..."\n\
sleep 5\n\
\n\
echo "Starting Gradio frontend..."\n\
python frontend/gradio_app.py\n\
' > start.sh && chmod +x start.sh

# Run the startup script
CMD ["./start.sh"]