FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for manim, manimpango, etc.
RUN apt-get update && apt-get install -y \
    ffmpeg \
    gcc \
    libcairo2-dev \
    libpango1.0-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependency list
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app source
COPY app.py ./

# Expose renderer service on port 8001
EXPOSE 8001

# Run the FastAPI app with Uvicorn
