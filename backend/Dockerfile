FROM python:3.11-slim

# Set environment variables
# MALLOC_ARENA_MAX=2 helps limit RAM fragmentation
# OMP_NUM_THREADS=1 prevents CPU/RAM spikes from parallel processing in MoviePy/ffmpeg
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MALLOC_ARENA_MAX=2 \
    OMP_NUM_THREADS=1 \
    DEBUG=False \
    PORT=8000 \
    PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    wget \
    curl \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install Piper TTS models (from Hugging Face)
RUN mkdir -p /app/models && \
    wget -O /app/models/en_US-lessac-medium.onnx https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx?download=true && \
    wget -O /app/models/en_US-lessac-medium.onnx.json https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json?download=true

# Set working directory
WORKDIR /app

# Copy requirements from backend/ because Render Root Directory is empty
COPY backend/requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend files into the current WORKDIR (/app)
COPY backend/ .

# Ensure storage directories exist
RUN mkdir -p storage/audio storage/images storage/videos

# Make scripts executable
RUN chmod +x scripts/*.sh

# Default to Web Service entrypoint
# Render users should override the CMD for the Worker service:
# ./scripts/start-worker.sh
CMD ["./scripts/start-web.sh"]
