#!/bin/bash
set -e

echo "Starting AI Video Agent Background Worker..."

# Ensure storage directories exist
mkdir -p storage/audio storage/images storage/videos

# Run worker
exec python worker.py
