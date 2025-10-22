# Lesson 08 - Code Reference

This directory contains the code reference for Lesson 08 (AI Integration with Ollama).

## Files

- `package.json` - Node.js project configuration with Ollama scripts
- `src/server.js` - HTTP server with Ollama proxy
- `src/database.js` - SQLite database operations
- `public/` - Frontend files with AI integration
- `scripts/` - Helper scripts for Ollama setup

## What You'll Learn

- Setting up Ollama for local LLM
- Proxying API requests through your server
- Streaming AI responses
- Markdown parsing for AI output
- Error handling for AI requests
- Environment configuration

## Running the Project

```bash
# Install dependencies
npm install

# Run development server (includes Ollama setup)
npm run dev
```

This will:
1. Start your Node.js server
2. Start Ollama on port 8081
3. Download the Qwen2.5:0.5b model

Then open http://localhost:3000 in your browser.

## API Endpoints

All previous endpoints plus:
- `POST /api/chat` - Send message to AI and get response
