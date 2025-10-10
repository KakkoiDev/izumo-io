import { DatabaseSync } from 'node:sqlite'
import path from 'node:path'

// Database file location
const DB_PATH = path.join(import.meta.dirname, '../chatbot.db')

// Initialize database connection
const db = new DatabaseSync(DB_PATH)

// Create tables if they don't exist
function initializeSchema() {
  db.exec(`
    CREATE TABLE IF NOT EXISTS conversations (
      id TEXT PRIMARY KEY,
      title TEXT NOT NULL,
      created_at INTEGER NOT NULL
    )
  `)

  db.exec(`
    CREATE TABLE IF NOT EXISTS messages (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      conversation_id TEXT NOT NULL,
      role TEXT NOT NULL,
      content TEXT NOT NULL,
      created_at INTEGER NOT NULL,
      FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
    )
  `)
}

// Initialize database on module load
initializeSchema()

// Conversation operations
export const conversations = {
  // Get all conversations with their messages
  getAll() {
    const convStmt = db.prepare('SELECT * FROM conversations ORDER BY created_at DESC')
    const convs = convStmt.all()

    // Load messages for each conversation
    const msgStmt = db.prepare('SELECT * FROM messages WHERE conversation_id = ? ORDER BY created_at ASC')
    return convs.map(conv => ({
      ...conv,
      messages: msgStmt.all(conv.id)
    }))
  },

  // Get single conversation with messages
  getById(id) {
    const convStmt = db.prepare('SELECT * FROM conversations WHERE id = ?')
    const conversation = convStmt.get(id)

    if (!conversation) return null

    const msgStmt = db.prepare('SELECT * FROM messages WHERE conversation_id = ? ORDER BY created_at ASC')
    conversation.messages = msgStmt.all(id)

    return conversation
  },

  // Create new conversation
  create(id, title) {
    const stmt = db.prepare('INSERT INTO conversations (id, title, created_at) VALUES (?, ?, ?)')
    stmt.run(id, title, Date.now())
    return { id, title }
  },

  // Update conversation title
  updateTitle(id, title) {
    const stmt = db.prepare('UPDATE conversations SET title = ? WHERE id = ?')
    stmt.run(title, id)
  },

  // Delete conversation (cascade deletes messages)
  delete(id) {
    const stmt = db.prepare('DELETE FROM conversations WHERE id = ?')
    stmt.run(id)
  }
}

// Message operations
export const messages = {
  // Add message to conversation
  create(conversationId, role, content) {
    const stmt = db.prepare('INSERT INTO messages (conversation_id, role, content, created_at) VALUES (?, ?, ?, ?)')
    const result = stmt.run(conversationId, role, content, Date.now())
    return { id: result.lastInsertRowid, conversation_id: conversationId, role, content }
  },

  // Get messages for conversation
  getByConversationId(conversationId) {
    const stmt = db.prepare('SELECT * FROM messages WHERE conversation_id = ? ORDER BY created_at ASC')
    return stmt.all(conversationId)
  }
}
