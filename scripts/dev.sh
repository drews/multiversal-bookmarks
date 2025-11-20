#!/bin/bash
# Development server with auto-reload

echo "🚀 Starting Connections development server..."
uv run uvicorn backend.main:app --reload --port 8000
