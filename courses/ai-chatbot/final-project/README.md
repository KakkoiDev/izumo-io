# AI Chatbot - Final Project

A full-stack AI chatbot application with local LLM integration, conversation history, and persistent storage.

## Features

### Core Functionality
- **Chat Interface**: Clean, intuitive messaging interface with modern UI
- **AI Integration**: Local AI responses via Ollama (qwen2.5:0.5b model)
- **Conversation Management**: Create, rename, and delete conversations
- **Persistent Storage**: SQLite database for all chat data
- **Auto-generated Titles**: AI-powered conversation titles
- **Context Menu**: Modern Popover API + CSS Anchor Positioning for conversation actions

### Technical Highlights
- **Zero Framework Backend**: Bare Node.js HTTP server (no Express)
- **Built-in SQLite**: Uses Node.js experimental SQLite (no native dependencies)
- **Modern CSS**: Popover API, CSS Anchor Positioning (Chrome 125+ / Safari TP)
- **Hot Reload**: Native `node --watch` for development
- **Environment Config**: dotenv for configuration management

## Technology Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript (ES6+)
- **Backend**: Bare Node.js HTTP server (no frameworks)
- **Database**: Node.js built-in SQLite (`node:sqlite`)
- **AI/ML**: Ollama (local LLM - qwen2.5:0.5b)
- **Dev Tools**: node --watch, concurrently

## Prerequisites

- **Node.js**: v24+ (for built-in SQLite support)
- **Ollama**: Installed and running locally
- **Browser**: Chrome 125+ or Safari Technology Preview (for Popover API)

## Installation

### 1. Install Dependencies

```bash
npm install
```

This installs only 2 dependencies:
- `concurrently` - Run multiple dev processes
- `dotenv` - Environment variable management

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` if you need custom configuration:

```env
PORT=3000                    # Server port
OLLAMA_HOST=127.0.0.1:8081  # Ollama server address
OLLAMA_MODEL=qwen2.5:0.5b   # AI model to use
DB_PATH=./chatbot.db        # Database file path
```

### 3. Setup AI Model (One-time)

```bash
npm run setup
```

This pulls the qwen2.5:0.5b model from Ollama. Only needs to run once.

### 4. Start Development

**Option A - Node server only** (when Ollama already running system-wide):
```bash
npm run dev
```

**Option B - Everything together** (Node + Ollama):
```bash
npm run dev:all
```

**Option C - Just Ollama server**:
```bash
npm run ollama
```

### 5. Open Application

Navigate to: **http://localhost:3000**

## Usage

### Starting a Conversation
1. Type your message in the input field
2. Press **Enter** or click **Send**
3. AI responds using local Ollama model
4. Conversation title is auto-generated after first exchange

### Managing Conversations
- **View History**: Click the **≡** button to toggle sidebar
- **Switch Conversations**: Click any conversation in the sidebar
- **Rename**: Click **⋮** → select title → edit → press Enter
- **Delete**: Click **⋮** → Delete (with confirmation)
- **New Conversation**: Click **+ New Chat** in sidebar

## Project Structure

```
ai-chatbot/final-project/
├── public/                 # Frontend files
│   ├── index.html         # Main HTML
│   ├── styles.css         # Styles (with Popover API CSS)
│   └── script.js          # Frontend logic
├── src/                   # Backend source
│   ├── server.js          # HTTP server (120 lines)
│   └── database.js        # SQLite operations (93 lines)
├── .env.example           # Environment template
├── .env                   # Local config (gitignored)
├── package.json           # Dependencies & scripts
├── chatbot.db             # SQLite database (auto-created)
└── README.md             # This file
```

## API Documentation

### REST Endpoints

#### Conversations

**GET /api/conversations**
```json
Response: {
  "conversations": [
    {
      "id": "string",
      "title": "string",
      "created_at": 1234567890,
      "messages": [
        {"id": 1, "role": "user", "content": "...", "created_at": 1234567890}
      ]
    }
  ]
}
```

**POST /api/conversations**
```json
Request: {"id": "uuid", "title": "Untitled"}
Response: {"conversation": {...}}
```

**GET /api/conversations/:id**
```json
Response: {"conversation": {...}}
```

**PUT /api/conversations/:id**
```json
Request: {"title": "New Title"}
Response: {"success": true}
```

**DELETE /api/conversations/:id**
```json
Response: {"success": true}
```

#### Messages

**POST /api/messages**
```json
Request: {
  "conversationId": "uuid",
  "role": "user|assistant",
  "content": "message text"
}
Response: {"message": {...}}
```

#### AI Proxy

**POST /api/chat** (Ollama proxy)
```json
Request: {
  "model": "qwen2.5:0.5b",
  "messages": [{"role": "user", "content": "..."}],
  "stream": false
}
Response: {
  "message": {"role": "assistant", "content": "..."}
}
```

**POST /api/generate** (Ollama proxy)
```json
Request: {
  "model": "qwen2.5:0.5b",
  "prompt": "...",
  "stream": false
}
Response: {"response": "..."}
```

## Database Schema

### conversations
```sql
CREATE TABLE conversations (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  created_at INTEGER NOT NULL
)
```

### messages
```sql
CREATE TABLE messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  conversation_id TEXT NOT NULL,
  role TEXT NOT NULL,
  content TEXT NOT NULL,
  created_at INTEGER NOT NULL,
  FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
)
```

## npm Scripts

- `npm run setup` - Pull AI model (one-time setup)
- `npm run dev` - Start Node.js server only (hot-reload enabled)
- `npm run dev:all` - Start Node.js + Ollama together
- `npm run start` - Start Node.js server (production mode)
- `npm run ollama` - Start Ollama server only
- `npm run model:pull` - Update/re-pull AI model

## Troubleshooting

### Ollama Connection Failed

**Symptom**: "Ollama connection failed" error in console

**Solutions**:
1. Check Ollama is running: `ollama list`
2. Verify model installed: `ollama pull qwen2.5:0.5b`
3. Check OLLAMA_HOST in `.env` matches Ollama server

### Port Already in Use

**Symptom**: `EADDRINUSE: address already in use :::3000`

**Solutions**:
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Or change PORT in .env
PORT=3001
```

### Database Locked

**Symptom**: "database is locked" error

**Solutions**:
1. Close other connections to `chatbot.db`
2. Restart the server
3. Delete `chatbot.db` (data will be lost)

### Popover API Not Working

**Symptom**: Context menu (⋮) doesn't work

**Solutions**:
- Use **Chrome 125+** or **Safari Technology Preview**
- Or add Popover API polyfill for older browsers

### Unicode Characters Display Wrong

**Symptom**: Emojis show as �� or random characters

**Solution**: This should be fixed (charset=utf-8 in MIME types). If still broken, check browser encoding settings.

## Development Notes

### Why Bare Node.js?

We chose bare Node.js over Express because:
- **Simplicity**: 120 lines vs 200+ with Express
- **Zero Dependencies**: No framework overhead (50+ deps avoided)
- **Learning**: Understand HTTP fundamentals
- **Modern**: Leverage Node.js platform features

### Why Built-in SQLite?

We use Node.js experimental SQLite instead of better-sqlite3 because:
- **No Native Compilation**: Avoids node-gyp build issues
- **Zero Dependencies**: Built into Node.js v22+
- **Same API**: Similar to better-sqlite3
- **Perfect for Local Apps**: Stable enough for personal projects

### Browser Compatibility

The app uses modern web APIs:
- **Popover API**: Chrome 125+, Safari TP, Firefox (polyfill available)
- **CSS Anchor Positioning**: Chrome 125+, Safari TP
- **ES6 Modules**: All modern browsers

For older browsers, consider adding polyfills.

## Performance

- **API Response Time**: <10ms (excluding AI generation)
- **AI Response Time**: 3-15s (depends on hardware and model)
- **Database Queries**: Indexed for fast lookups
- **Memory Usage**: ~50MB (server) + model memory (Ollama)

## Security Notes

⚠️ **This app is for LOCAL USE ONLY**

- No authentication system
- No input sanitization (trust local user)
- SQLite injection prevented via prepared statements
- CORS disabled (same-origin only)
- Not production-ready for public deployment

## Future Enhancements

Potential improvements:
- [ ] Streaming AI responses (SSE or WebSockets)
- [ ] Message editing and deletion
- [ ] Conversation search and filtering
- [ ] Export conversations (JSON/Markdown)
- [ ] Multiple model selection
- [ ] Custom system prompts
- [ ] Dark mode toggle
- [ ] Message timestamps display
- [ ] Code syntax highlighting

## Learning Outcomes

This project demonstrates:
- ✅ Full-stack development (frontend + backend + database)
- ✅ RESTful API design and implementation
- ✅ SQLite database operations with foreign keys
- ✅ Local AI integration (Ollama)
- ✅ Modern web APIs (Popover, Anchor Positioning)
- ✅ Environment-based configuration
- ✅ Error handling and edge cases
- ✅ Clean code organization and documentation

## License

MIT License - Free for educational and personal use.

## Acknowledgments

- **Ollama** - Local LLM runtime
- **Qwen2.5** - Fast and efficient language model
- **Node.js Team** - Built-in SQLite support
- **Open Source Community** - For modern web APIs

---

**Status**: ✅ Complete (Phases 1-3)
**Last Updated**: 2025-10-05
**Node.js Version**: v24.9.0+
