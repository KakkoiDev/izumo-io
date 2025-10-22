# Lesson 10 - Code Reference

This directory contains the code reference for Lesson 10 (Production & Documentation).

## Files

- `package.json` - Complete project configuration
- `src/` - Server and database modules
- `public/` - Frontend files
- `scripts/` - Helper scripts (Ollama setup, livereload)
- `.env.example` - Environment variables template
- `.gitignore` - Git ignore rules

## What You'll Learn

- Environment variables configuration
- Production vs development setup
- Project documentation
- Helper scripts organization
- Security best practices
- Performance optimization

## Running the Project

```bash
# Install dependencies
npm install

# Copy environment template
cp .env.example .env

# Run development server with live reload
npm run dev

# Or run in production mode
npm start
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
PORT=3000
OLLAMA_HOST=127.0.0.1:8081
```

## Scripts

- `scripts/pull-qwen-0.5b.sh` - Download AI model
- `scripts/start-ollama.sh` - Start Ollama server
- `scripts/livereload.sh` - Live reload for development

## Production Checklist

- ✅ Environment variables configured
- ✅ Database schema initialized
- ✅ AI model downloaded
- ✅ All dependencies installed
- ✅ Documentation complete
- ✅ Git repository clean
