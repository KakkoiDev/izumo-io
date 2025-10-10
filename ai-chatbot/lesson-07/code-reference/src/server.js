import http from 'node:http'
import fs from 'node:fs/promises'
import path from 'node:path'
import { conversations, messages } from './database.js'

// Server configuration
const PORT = 3000

// MIME types for static files
const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8'
}

// Helper: Parse JSON request body
async function parseBody(req) {
  return new Promise((resolve, reject) => {
    let body = ''
    req.on('data', chunk => { body += chunk.toString() })
    req.on('end', () => {
      try {
        resolve(body ? JSON.parse(body) : {})
      } catch (error) {
        reject(error)
      }
    })
    req.on('error', reject)
  })
}

// Create HTTP server
const server = http.createServer(async (req, res) => {
  console.log(`${req.method} ${req.url}`)

  // Handle API routes (JSON responses)
  if (req.url.startsWith('/api/')) {
    res.setHeader('Content-Type', 'application/json; charset=utf-8')

    // Health check endpoint
    if (req.url === '/api/health' && req.method === 'GET') {
      res.end(JSON.stringify({ status: 'ok' }))
      return
    }

    // Get all conversations
    if (req.url === '/api/conversations' && req.method === 'GET') {
      const convs = conversations.getAll()
      res.end(JSON.stringify({ conversations: convs }))
      return
    }

    // Create new conversation
    if (req.url === '/api/conversations' && req.method === 'POST') {
      const { id, title } = await parseBody(req)
      const conversation = conversations.create(id, title)
      res.end(JSON.stringify({ conversation }))
      return
    }

    // Get conversation by ID
    if (req.url.match(/^\/api\/conversations\/[^/]+$/) && req.method === 'GET') {
      const id = req.url.split('/')[3]
      const conversation = conversations.getById(id)
      if (!conversation) {
        res.statusCode = 404
        res.end(JSON.stringify({ error: 'Conversation not found' }))
        return
      }
      res.end(JSON.stringify({ conversation }))
      return
    }

    // Update conversation title
    if (req.url.match(/^\/api\/conversations\/[^/]+$/) && req.method === 'PUT') {
      const id = req.url.split('/')[3]
      const { title } = await parseBody(req)
      conversations.updateTitle(id, title)
      res.end(JSON.stringify({ success: true }))
      return
    }

    // Delete conversation
    if (req.url.match(/^\/api\/conversations\/[^/]+$/) && req.method === 'DELETE') {
      const id = req.url.split('/')[3]
      conversations.delete(id)
      res.end(JSON.stringify({ success: true }))
      return
    }

    // Add message to conversation
    if (req.url === '/api/messages' && req.method === 'POST') {
      const { conversationId, role, content } = await parseBody(req)
      const message = messages.create(conversationId, role, content)
      res.end(JSON.stringify({ message }))
      return
    }

    // API endpoint not found
    res.statusCode = 404
    res.end(JSON.stringify({ error: 'Not found' }))
    return
  }

  // Handle static files (HTML, CSS, JS)
  const filePath = path.join(import.meta.dirname, '../public', req.url === '/' ? 'index.html' : req.url)

  try {
    const content = await fs.readFile(filePath)
    const ext = path.extname(filePath)
    res.setHeader('Content-Type', MIME_TYPES[ext] || 'text/plain; charset=utf-8')
    res.statusCode = 200
    res.end(content)
  } catch (error) {
    console.error(`File not found: ${filePath}`)
    res.statusCode = 404
    res.end('404 - Not Found')
  }
})

// Start server
server.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`)
})
