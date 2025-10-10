import http from 'node:http'
import fs from 'node:fs/promises'
import path from 'node:path'

// Server configuration
const PORT = 3000

// MIME types for static files
const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8'
}

// Create HTTP server
const server = http.createServer(async (req, res) => {
  console.log(`${req.method} ${req.url}`)

  // Map '/' to 'index.html', everything else to its path in public/
  const filePath = path.join(import.meta.dirname, '../public', req.url === '/' ? 'index.html' : req.url)

  try {
    // Read file from disk
    const content = await fs.readFile(filePath)
    const ext = path.extname(filePath)

    // Set correct Content-Type header based on file extension
    res.setHeader('Content-Type', MIME_TYPES[ext] || 'text/plain; charset=utf-8')
    res.statusCode = 200
    res.end(content)
  } catch (error) {
    // File not found
    console.error(`File not found: ${filePath}`)
    res.statusCode = 404
    res.end('404 - Not Found')
  }
})

// Start server
server.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`)
})
