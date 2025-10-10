# Lesson 07 - Code Reference

This directory contains the code reference for Lesson 07 (Database Integration with SQLite).

## Files

- `package.json` - Node.js project configuration
- `src/server.js` - HTTP server with API endpoints
- `src/database.js` - SQLite database operations
- `public/` - Frontend files (HTML, CSS, JS)
- `.gitignore` - Git ignore rules (excludes database file)

## What You'll Learn

- SQLite database setup
- Creating tables and schema
- CRUD operations (Create, Read, Update, Delete)
- SQL queries with prepared statements
- API endpoints for database operations
- Foreign keys and relationships

## Running the Project

```bash
# Run development server
npm run dev
```

The database file `chatbot.db` will be created automatically when you first run the server.

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/conversations` - Get all conversations
- `POST /api/conversations` - Create new conversation
- `GET /api/conversations/:id` - Get conversation by ID
- `PUT /api/conversations/:id` - Update conversation title
- `DELETE /api/conversations/:id` - Delete conversation
- `POST /api/messages` - Add message to conversation
