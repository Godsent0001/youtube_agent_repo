FROM python:3.11-slim

# Set environment variables
# MALLOC_ARENA_MAX=2 helps limit RAM fragmentation
# OMP_NUM_THREADS=1 prevents CPU/RAM spikes from parallel processing in MoviePy/ffmpeg
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MALLOC_ARENA_MAX=2 \
    OMP_NUM_THREADS=1 \
    DEBUG=False \
    PORT=8000

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements from backend/ because Render Root Directory is empty
COPY backend/requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend files into the current WORKDIR (/app)
COPY backend/ .

# Start FastAPI app using Gunicorn with Uvicorn workers
# -k uvicorn.workers.UvicornWorker: use uvicorn workers
# --timeout 600: increase timeout for long-running video generation (5-10 mins)
# --workers 1: stay within 512MB RAM limits
CMD gunicorn app.main:app \
    --bind 0.0.0.0:${PORT} \
    -k uvicorn.workers.UvicornWorker \
    --workers 1 \
    --timeout 600
