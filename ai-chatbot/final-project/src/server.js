import http from 'node:http'
import fs from 'node:fs/promises'
import path from 'node:path'
import { conversations, messages } from './database.js'

// Server configuration
const PORT = 3000

// MIME types for static files (charset=utf-8 fixes emoji/unicode display)
const TYPES = {
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
        reject(new Error(`Invalid JSON: ${error.message}`))
      }
    })
    req.on('error', reject)
  })
}

// Create HTTP server
const server = http.createServer(async (req, res) => {
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
      try {
        const { id, title } = await parseBody(req)
        const conversation = conversations.create(id, title)
        res.end(JSON.stringify({ conversation }))
      } catch (error) {
        res.statusCode = 400
        res.end(JSON.stringify({ error: error.message }))
      }
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
      try {
        const id = req.url.split('/')[3]
        const { title } = await parseBody(req)
        conversations.updateTitle(id, title)
        res.end(JSON.stringify({ success: true }))
      } catch (error) {
        res.statusCode = 400
        res.end(JSON.stringify({ error: error.message }))
      }
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
      try {
        const { conversationId, role, content } = await parseBody(req)
        const message = messages.create(conversationId, role, content)
        res.end(JSON.stringify({ message }))
      } catch (error) {
        res.statusCode = 400
        res.end(JSON.stringify({ error: error.message }))
      }
      return
    }

    // Proxy to Ollama chat endpoint
    if (req.url === '/api/chat' && req.method === 'POST') {
      try {
        const body = await parseBody(req)

        const ollamaReq = http.request('http://localhost:8081/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        }, (ollamaRes) => {
          res.statusCode = ollamaRes.statusCode
          res.setHeader('Content-Type', 'application/json; charset=utf-8')
          ollamaRes.pipe(res)
        })

        ollamaReq.on('error', (error) => {
          res.statusCode = 500
          res.end(JSON.stringify({ error: 'Ollama connection failed', details: error.message }))
        })

        ollamaReq.write(JSON.stringify(body))
        ollamaReq.end()
      } catch (error) {
        res.statusCode = 400
        res.end(JSON.stringify({ error: error.message }))
      }
      return
    }

    // Proxy to Ollama generate endpoint
    if (req.url === '/api/generate' && req.method === 'POST') {
      try {
        const body = await parseBody(req)

        const ollamaReq = http.request('http://localhost:8081/api/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        }, (ollamaRes) => {
          res.statusCode = ollamaRes.statusCode
          res.setHeader('Content-Type', 'application/json; charset=utf-8')
          ollamaRes.pipe(res)
        })

        ollamaReq.on('error', (error) => {
          res.statusCode = 500
          res.end(JSON.stringify({ error: 'Ollama connection failed', details: error.message }))
        })

        ollamaReq.write(JSON.stringify(body))
        ollamaReq.end()
      } catch (error) {
        res.statusCode = 400
        res.end(JSON.stringify({ error: error.message }))
      }
      return
    }

    // API endpoint not found
    res.statusCode = 404
    res.end(JSON.stringify({ error: 'Not found' }))
    return
  }

  // Handle static files (HTML, CSS, JS)
  // Map '/' to 'index.html', everything else to its path in public/
  const filePath = path.join(import.meta.dirname, '../public', req.url === '/' ? 'index.html' : req.url)

  try {
    // Read file from disk
    const content = await fs.readFile(filePath)
    const ext = path.extname(filePath)
    // Set correct Content-Type header based on file extension
    res.setHeader('Content-Type', TYPES[ext] || 'text/plain; charset=utf-8')
    res.end(content)
  } catch {
    // File not found
    res.statusCode = 404
    res.end('Not Found')
  }
})

// Start server
server.listen(PORT, () => {
  console.log(`Server: http://localhost:${PORT}`)
})
