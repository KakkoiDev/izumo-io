import http from 'node:http'
import fs from 'node:fs/promises'
import path from 'node:path'

// Server configuration
const PORT = 3000

// MIME types for static files (charset=utf-8 fixes emoji/unicode display)
const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8'
}

// Create HTTP server
const server = http.createServer(async (req, res) => {
  // Handle API routes (JSON responses)
  if (req.url.startsWith('/api/')) {
    res.setHeader('Content-Type', 'application/json; charset=utf-8')

    // Health check endpoint
    if (req.url === '/api/health') {
      res.end(JSON.stringify({ status: 'ok' }))
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
