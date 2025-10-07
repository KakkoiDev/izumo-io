#!/bin/bash

# Pull qwen2.5:0.5b model for Ollama
# This script is run after npm install to ensure the model is available

# Load environment variables from .env if it exists
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Use environment variable or default
OLLAMA_HOST=${OLLAMA_HOST:-127.0.0.1:8081}
OLLAMA_MODEL=${OLLAMA_MODEL:-qwen2.5:0.5b}

echo "Checking if Ollama model '$OLLAMA_MODEL' is available..."

# Check if ollama is installed
if ! command -v ollama &> /dev/null; then
  echo "⚠️  Ollama is not installed. Skipping model pull."
  echo "   Install Ollama from: https://ollama.ai"
  exit 0
fi

# Check if Ollama server is running
if ! OLLAMA_HOST=$OLLAMA_HOST ollama list &> /dev/null; then
  echo "⚠️  Ollama server is not running. Skipping model pull."
  echo "   Start Ollama with: ollama serve"
  exit 0
fi

# Check if model is already pulled
if OLLAMA_HOST=$OLLAMA_HOST ollama list | grep -q "$OLLAMA_MODEL"; then
  echo "✅ Model '$OLLAMA_MODEL' is already available"
  exit 0
fi

# Pull the model
echo "📥 Pulling model '$OLLAMA_MODEL'..."
OLLAMA_HOST=$OLLAMA_HOST ollama pull "$OLLAMA_MODEL"

if [ $? -eq 0 ]; then
  echo "✅ Model '$OLLAMA_MODEL' pulled successfully"
else
  echo "❌ Failed to pull model '$OLLAMA_MODEL'"
  exit 1
fi
