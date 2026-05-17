#!/bin/bash
set -e

echo "Starting AI Video Agent Web Service..."

# Ensure storage directories exist
mkdir -p storage/audio storage/images storage/videos

# Start Gunicorn
exec gunicorn app.main:app \
    --bind 0.0.0.0:${PORT:-8000} \
    -k uvicorn.workers.UvicornWorker \
    --workers 1 \
    --timeout 600 \
    --access-logfile - \
    --error-logfile -
