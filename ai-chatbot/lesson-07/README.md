# Lesson 07: Database Integration with SQLite

## Theme: "Memory Matters - Preserving and Organizing Information"

## Learning Objectives
By the end of this lesson, you will:
- Understand database concepts and why we need them
- Learn SQL basics (SELECT, INSERT, UPDATE, DELETE)
- Set up SQLite with Node.js
- Design database schema for chat application
- Implement persistent chat history storage
- Perform CRUD operations from your server

## What We're Learning This Week

### Technical Concepts
- **Databases**: Persistent data storage
- **Relational Databases**: Tables, rows, columns, relationships
- **SQL**: Structured Query Language for database operations
- **SQLite**: Lightweight, file-based database
- **Schema Design**: Planning database structure
- **CRUD Operations**: Create, Read, Update, Delete
- **Database Integration**: Connecting Node.js to SQLite

### SQL & Database Concepts Focus
- `CREATE TABLE` - Define database structure
- `INSERT INTO` - Add new records
- `SELECT` - Query data
- `UPDATE` - Modify existing records
- `DELETE` - Remove records
- `WHERE` clauses - Filtering data
- Primary keys and relationships

## This Week's Tasks

### 1. Database Fundamentals
- [ ] Understand what databases solve (vs. storing in files)
- [ ] Learn basic SQL syntax
- [ ] Install DBeaver or another database viewer
- [ ] Understand database design principles

### 2. SQLite Setup
- [ ] Use Node.js built-in sqlite module (Node 22.5+)
- [ ] Create database file
- [ ] Design schema for conversations and messages
- [ ] Create tables with appropriate columns

### 3. Chatbot Database Integration
- [ ] Create database.js module
- [ ] Implement functions: createConversation, saveMessage, getMessages
- [ ] Update API endpoints to use database
- [ ] Load chat history on page load
- [ ] Test data persistence (server restart retains history)

## Career Lesson: "Keep learning everyday to not become obsolete - The technology landscape changes rapidly"

### Why This Matters
Technology evolves at breakneck pace:
- New frameworks and tools emerge constantly
- Yesterday's best practices become outdated
- Skills depreciate without maintenance
- AI is changing the development landscape rapidly

### Real-World Application

**Make Learning a Habit**:
- Dedicate time regularly (even 20 min/day)
- Follow tech news and release notes
- Read code written by others
- Contribute to open source projects

**Learn Strategically**:
- Focus on fundamentals that transfer across technologies
- Learn adjacent skills (backend dev learns DevOps)
- Deep knowledge in one area + broad knowledge in others
- Follow your curiosity but align with career goals

**Learning Sources**:
- Official documentation (most accurate)
- Technical blogs and tutorials
- Conference talks and podcasts
- Books for deep understanding
- Hands-on projects (best learning method)

**Balance Breadth and Depth**:
- **T-shaped skills**: Deep in one area, broad understanding in others
- Don't chase every new trend
- Evaluate if new tech solves real problems
- Master current tools before jumping to new ones

**Stay Relevant with AI**:
- Learn to work WITH AI tools (GitHub Copilot, Claude, ChatGPT)
- Focus on skills AI can't replace (architecture, communication, critical thinking)
- Understand AI capabilities and limitations
- Use AI to accelerate learning, not replace it

### Signs You're Falling Behind
- Job postings require skills you don't have
- Younger developers know tools you've never heard of
- Your solutions feel outdated compared to modern practices
- Fear or resistance to new technologies

### Continuous Learning Isn't Optional
This isn't about pressure - it's about career survival and growth in a rapidly evolving field. Make learning a sustainable, enjoyable part of your routine.

## Project State After This Lesson
```
chatbot-project/
├── public/
│   ├── index.html
│   ├── styles.css
│   └── script.js (UPDATED: load history)
├── src/
│   ├── server.js (UPDATED: database endpoints)
│   └── database.js (NEW: database operations)
├── chatbot.db (NEW: SQLite database file)
├── package.json
├── README.md
└── .git/
```

Your chatbot now has:
- Persistent chat history stored in SQLite
- Conversations preserved across server restarts
- Ability to view previous conversations
- Database schema for messages and conversations
- CRUD operations for managing chat data

## Additional Resources

### Essential Reading
- [SQLite Official Docs](https://www.sqlite.org/docs.html)
- [SQL Tutorial - W3Schools](https://www.w3schools.com/sql/)
- [Node.js sqlite module](https://nodejs.org/api/sqlite.html)
- [Database Design Basics](https://www.guru99.com/database-design.html)

### Tools
- **DBeaver**: Universal database viewer (free, open source)
- **DB Browser for SQLite**: SQLite-specific GUI tool

### Video Tutorials
- "SQL in 100 Seconds"
- "Database Design Tutorial"
- "SQLite with Node.js"

### Practice Challenges
1. **Todo App DB**: Build todo list with SQLite persistence
2. **User Management**: Create users table with CRUD operations
3. **Data Relationships**: Link tables with foreign keys
4. **Search Feature**: Implement full-text search in messages

## Common Mistakes to Avoid
- Not closing database connections properly
- SQL injection vulnerabilities (use parameterized queries!)
- Not handling database errors
- Poor schema design requiring major refactors
- Forgetting to add .db files to .gitignore
- Not backing up database files

## Troubleshooting Common Issues

### Database Locked
- Close other applications accessing the database
- Ensure previous connections are closed
- Check for uncommitted transactions

### Table Already Exists
```javascript
// Use IF NOT EXISTS
CREATE TABLE IF NOT EXISTS messages (...)
```

### SQL Syntax Error
- Check SQL syntax carefully
- Use proper quotes (single for strings, none for numbers)
- Verify column names match schema
- Use parameterized queries for safety

## Code Example Structure

database.js:
```javascript
import { DatabaseSync } from 'node:sqlite'

const db = new DatabaseSync('./chatbot.db')

// Create tables
db.exec(`
  CREATE TABLE IF NOT EXISTS conversations (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    created_at INTEGER DEFAULT (strftime('%s', 'now'))
  )
`)

db.exec(`
  CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at INTEGER DEFAULT (strftime('%s', 'now')),
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
  )
`)

// Database operations
export const conversations = {
  create(id, title) {
    const stmt = db.prepare('INSERT INTO conversations (id, title) VALUES (?, ?)')
    stmt.run(id, title)
    return { id, title }
  },

  getAll() {
    return db.prepare('SELECT * FROM conversations ORDER BY created_at DESC').all()
  }
}

export const messages = {
  create(conversationId, role, content) {
    const stmt = db.prepare(
      'INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)'
    )
    stmt.run(conversationId, role, content)
  },

  getByConversation(conversationId) {
    return db.prepare(
      'SELECT * FROM messages WHERE conversation_id = ? ORDER BY created_at'
    ).all(conversationId)
  }
}
```

## Database Schema Design

```sql
-- Conversations table
CREATE TABLE conversations (
  id TEXT PRIMARY KEY,           -- Unique conversation ID
  title TEXT NOT NULL,           -- Conversation title
  created_at INTEGER             -- Unix timestamp
)

-- Messages table
CREATE TABLE messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  conversation_id TEXT NOT NULL, -- Links to conversations.id
  role TEXT NOT NULL,            -- 'user' or 'assistant'
  content TEXT NOT NULL,         -- Message text
  created_at INTEGER,            -- Unix timestamp
  FOREIGN KEY (conversation_id) REFERENCES conversations(id)
)
```

## Next Week Preview
In Lesson 08, we'll integrate real AI! You'll connect your chatbot to Ollama for local AI responses, learning about LLM models, prompt engineering, and AI integration patterns.

## Homework
1. Set up SQLite database with conversations and messages tables
2. Implement all CRUD operations in database.js
3. Update server endpoints to use database
4. Test data persistence across server restarts
5. Load previous conversations on page load
6. Use DBeaver to view your database
7. Commit your work
8. Share your persistent chatbot on Discord
