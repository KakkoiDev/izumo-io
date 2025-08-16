# AI Chatbot - Final Project

## Overview
This is the complete AI chatbot application built throughout the 10-week course. It demonstrates a full-stack web application with local AI integration, featuring a modern chat interface with conversation history.

## Features

### Core Functionality
- **Chat Interface**: Clean, intuitive messaging interface
- **AI Integration**: Local AI responses via Ollama
- **Conversation History**: Toggle sidebar showing previous conversations
- **Data Persistence**: SQLite database storing all chat sessions
- **Responsive Design**: Works on desktop and mobile devices

### Technical Features
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Node.js with Express.js
- **Database**: SQLite for conversation storage
- **AI**: Local LLM integration via Ollama
- **Local Deployment**: No cloud dependencies required

## Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Node.js, Express.js
- **Database**: SQLite3
- **AI/ML**: Ollama (local LLM)
- **Tools**: VS Code, Git, npm

## Installation & Setup

### Prerequisites
- Node.js (version 14 or higher)
- npm (comes with Node.js)
- Ollama installed and running
- Git (for version control)

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd final-project
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Initialize the database**
   ```bash
   npm run setup-db
   ```

5. **Start Ollama (in a separate terminal)**
   ```bash
   ollama serve
   ollama pull llama2  # or your preferred model
   ```

6. **Start the application**
   ```bash
   npm start
   ```

7. **Open your browser**
   ```
   Navigate to http://localhost:3000
   ```

## Usage

### Starting a Conversation
1. Type your message in the input field at the bottom
2. Press Enter or click the Send button
3. The AI will respond using the local Ollama model

### Managing Conversations
1. Click the sidebar toggle button (≡) to view conversation history
2. Click on any previous conversation to continue it
3. Start a new conversation anytime by sending a new message

### Features Overview
- **Real-time messaging** with immediate AI responses
- **Conversation persistence** - your chats are saved locally
- **History navigation** - easily switch between past conversations
- **Responsive design** - works on all screen sizes

## Project Structure

```
final-project/
├── public/                 # Frontend assets
│   ├── index.html         # Main HTML file
│   ├── style.css          # Styles
│   └── script.js          # Frontend JavaScript
├── src/                   # Backend source code
│   ├── server.js          # Express server
│   ├── database.js        # Database operations
│   └── routes/            # API routes
├── database/              # SQLite database files
├── package.json           # Dependencies and scripts
├── .env.example          # Environment variables template
└── README.md             # This file
```

## API Endpoints

### Chat Operations
- `POST /api/messages` - Send a new message
- `GET /api/conversations` - Get all conversations
- `GET /api/conversations/:id` - Get specific conversation
- `POST /api/conversations` - Create new conversation

### Database Schema
- **conversations**: id, title, created_at, updated_at
- **messages**: id, conversation_id, sender, content, timestamp

## Development

### Running in Development Mode
```bash
npm run dev  # Starts with nodemon for auto-restart
```

### Running Tests
```bash
npm test
```

### Database Management
```bash
npm run reset-db  # Reset database (WARNING: deletes all data)
npm run backup-db # Create database backup
```

## Troubleshooting

### Common Issues

**Ollama not responding**
- Ensure Ollama is running: `ollama serve`
- Check if model is installed: `ollama list`
- Verify model name in configuration

**Database errors**
- Run database setup: `npm run setup-db`
- Check file permissions in database/ directory
- Verify SQLite is installed

**Port already in use**
- Change port in .env file
- Kill process using the port: `lsof -ti:3000 | xargs kill`

**Frontend not loading**
- Check that server is running on correct port
- Verify static file serving is configured
- Check browser console for errors

## Performance Considerations

- **Database**: SQLite performs well for local development
- **AI Responses**: Response time depends on your hardware and model size
- **Memory Usage**: Monitor Node.js memory usage with large conversation histories
- **Storage**: Regular database cleanup recommended for long-term use

## Security Notes

- This application is designed for local use only
- No authentication system implemented
- All data stored locally on your machine
- No external API keys or cloud services required

## Future Enhancements

Potential improvements for this project:
- User authentication and profiles
- Conversation export/import functionality
- Custom AI model selection
- Advanced conversation search
- Message editing and deletion
- Chat themes and customization
- File attachment support
- Voice input integration

## Learning Outcomes

This project demonstrates:
- Full-stack web development skills
- Database design and operations
- API development and integration
- Frontend/backend communication
- Local AI integration
- Professional code organization
- Documentation and presentation skills

## Contributing

This is a learning project, but if you'd like to contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes. Feel free to use it as a learning resource or starting point for your own projects.

## Acknowledgments

- Built as part of the 10-week AI Chatbot Development Course
- Uses Ollama for local AI integration
- Inspired by modern chat applications like ChatGPT and Claude

---

**Course Completion Date**: [Your completion date]
**Developer**: [Your name]
**Course**: 10-Week AI Chatbot Development