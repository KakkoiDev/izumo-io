#!/bin/bash

# Start Ollama server with custom configuration
# Reads OLLAMA_HOST from .env if available

# Load environment variables from .env if it exists
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Use environment variable or default
OLLAMA_HOST=${OLLAMA_HOST:-127.0.0.1:8081}

# Check if ollama is installed
if ! command -v ollama &> /dev/null; then
  echo "❌ Ollama is not installed"
  echo "   Install Ollama from: https://ollama.ai"
  exit 1
fi

echo "🚀 Starting Ollama server on $OLLAMA_HOST..."
echo "   (Allow all origins for local development)"

# Start Ollama with CORS enabled
OLLAMA_ORIGINS=* OLLAMA_HOST=$OLLAMA_HOST ollama serve
