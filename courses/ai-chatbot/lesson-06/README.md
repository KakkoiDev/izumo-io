# Lesson 06: Node.js & Server Development

## Theme: "Building the Engine - Backend Thinking"

## Learning Objectives
By the end of this lesson, you will:
- Understand what Node.js is and why we use it
- Learn to create a simple HTTP server
- Understand routing and serving static files
- Learn about npm and package management
- Create API endpoints for your chatbot
- Understand the difference between frontend and backend code

## What We're Learning This Week

### Technical Concepts
- **Node.js**: JavaScript runtime for server-side code
- **npm**: Package manager for installing dependencies
- **HTTP Server**: Serving web pages and handling requests
- **Routing**: Directing requests to appropriate handlers
- **Static Files**: Serving HTML, CSS, JavaScript to browsers
- **API Endpoints**: Creating routes for data exchange
- **Environment Setup**: package.json and project configuration

### Node.js Concepts Focus
- `http` module - Creating servers
- `fs` module - Reading/writing files
- `path` module - Working with file paths
- Request/Response objects
- URL routing
- Serving static content

## This Week's Tasks

### 1. Node.js Fundamentals
- [ ] Install Node.js and npm
- [ ] Understand what Node.js is and how it differs from browser JavaScript
- [ ] Learn npm basics (init, install, run)
- [ ] Create package.json file

### 2. Server Creation
- [ ] Create a basic HTTP server using Node.js
- [ ] Serve HTML, CSS, and JavaScript files
- [ ] Implement basic routing
- [ ] Handle different HTTP methods (GET, POST)
- [ ] Test server locally on localhost

### 3. Chatbot Backend Integration
- [ ] Move chatbot files to proper project structure
- [ ] Create server.js or index.js entry point
- [ ] Serve chatbot interface from server
- [ ] Create API endpoint for mock chat responses
- [ ] Update frontend to call local API instead of mock function

## Career Lesson: "Enjoy your free time after work - Maintaining work-life balance to sustain a long career"

### Why This Matters
Software development can be all-consuming:
- It's intellectually engaging and easy to lose track of time
- Remote work blurs the line between work and personal life
- Constant learning feels like it should happen 24/7
- Burnout is real and career-ending if not managed

### Real-World Application

**Set Boundaries**:
- Define work hours and stick to them
- Create physical separation (dedicated workspace)
- Turn off work notifications after hours
- Communicate your boundaries clearly

**Invest in Life Outside Code**:
- Hobbies unrelated to technology
- Physical exercise and health
- Relationships with family and friends
- Rest and mental recovery time

**Sustainable Learning**:
- Learning is part of the job, not always extra
- Quality learning > quantity of hours
- Schedule specific learning time
- It's okay to not learn every evening/weekend

**Career is a Marathon**:
- 40+ year careers require sustainable pace
- Rested developers are more productive
- Creativity requires mental space
- Life experiences make you a better developer

**Signs of Imbalance**:
- Dreading Monday or work in general
- No hobbies or interests outside work
- Strained relationships due to work
- Physical health declining
- Mental exhaustion even after vacation

## Project State After This Lesson
```
chatbot-project/
├── public/              (NEW: frontend files)
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── src/                 (NEW: backend code)
│   └── server.js
├── package.json         (NEW: project config)
├── package-lock.json
├── node_modules/
├── README.md
└── .git/
```

Your chatbot now has:
- Proper frontend/backend separation
- Node.js server running on localhost
- API endpoint for chat responses
- Static file serving for HTML/CSS/JS
- Package.json with dependencies and scripts

## Additional Resources

### Essential Reading
- [Node.js Official Docs](https://nodejs.org/en/docs/)
- [npm Documentation](https://docs.npmjs.com/)
- [MDN HTTP Overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)

### Video Tutorials
- "Node.js in 100 Seconds"
- "Build a Web Server with Node.js"
- "Understanding npm and package.json"

### Practice Challenges
1. **File Server**: Create server that serves different HTML files based on route
2. **JSON API**: Build API that returns data in JSON format
3. **Request Logging**: Log all requests with timestamp and URL
4. **Error Pages**: Create custom 404 Not Found page

## Common Mistakes to Avoid
- Not handling server errors properly
- Hardcoding file paths instead of using `path` module
- Forgetting to set correct Content-Type headers
- Not validating request data
- Committing node_modules to git (.gitignore)
- Using port numbers that require sudo/admin

## Troubleshooting Common Issues

### Port Already in Use
```bash
# Find process using port 3000
lsof -i :3000
# Kill the process
kill -9 <PID>
```

### Module Not Found
```bash
# Install dependencies from package.json
npm install

# Install specific package
npm install <package-name>
```

### Cannot GET /
- Check if server is serving correct directory
- Verify file paths are correct
- Ensure index.html exists in public folder

## Code Example Structure

Basic server.js structure:
```javascript
const http = require('http')
const fs = require('fs')
const path = require('path')

const PORT = 3000

const server = http.createServer((req, res) => {
  // API route
  if (req.url === '/api/chat' && req.method === 'POST') {
    // Handle chat API
    res.writeHead(200, { 'Content-Type': 'application/json' })
    res.end(JSON.stringify({ message: 'Hello from server!' }))
    return
  }

  // Serve static files
  let filePath = path.join(__dirname, 'public', req.url === '/' ? 'index.html' : req.url)

  fs.readFile(filePath, (err, content) => {
    if (err) {
      res.writeHead(404)
      res.end('Not Found')
    } else {
      res.writeHead(200, { 'Content-Type': getContentType(filePath) })
      res.end(content)
    }
  })
})

server.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`)
})
```

Package.json scripts:
```json
{
  "scripts": {
    "start": "node src/server.js",
    "dev": "node --watch src/server.js"
  }
}
```

## Next Week Preview
In Lesson 07, we'll add database functionality with SQLite. You'll learn how to persist chat history, store conversations, and implement full CRUD operations.

## Homework
1. Create Node.js server that serves your chatbot
2. Implement `/api/chat` endpoint with mock responses
3. Update frontend fetch() to call your local API
4. Add proper error handling on server
5. Test server start/stop and request handling
6. Create npm scripts for running server
7. Commit your work with clear separation of frontend/backend
8. Document how to run your server in README
