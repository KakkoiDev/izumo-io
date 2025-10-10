# Lesson 08: AI Integration - Local with Ollama

## Theme: "Intelligence Amplified - Working with AI as a Partner"

## Learning Objectives
By the end of this lesson, you will:
- Understand Large Language Models (LLMs) basics
- Set up and configure Ollama for local AI
- Learn about different LLM models and their characteristics
- Integrate Ollama with your chatbot backend
- Understand prompt engineering fundamentals
- Handle streaming responses from AI

## What We're Learning This Week

### Technical Concepts
- **Large Language Models**: AI trained on text to generate responses
- **Local vs Cloud AI**: Trade-offs and use cases
- **Ollama**: Tool for running LLMs locally
- **Model Selection**: Choosing appropriate models for your needs
- **Prompt Engineering**: Crafting effective prompts
- **Streaming Responses**: Handling real-time AI output
- **API Integration**: Connecting to Ollama's HTTP API

### AI & Integration Concepts Focus
- Ollama CLI commands
- Ollama HTTP API endpoints (`/api/generate`, `/api/chat`)
- Model management (pull, list, remove)
- Streaming vs non-streaming responses
- System prompts and conversation context
- Token limits and response quality

## This Week's Tasks

### 1. Ollama Setup & Exploration
- [ ] Install Ollama
- [ ] Pull a small model (qwen2.5:0.5b for testing)
- [ ] Test models via CLI
- [ ] Understand model sizes and speed trade-offs
- [ ] Explore Ollama API documentation

### 2. Backend Integration
- [ ] Create proxy endpoint to Ollama in server.js
- [ ] Send user messages to Ollama
- [ ] Receive and format AI responses
- [ ] Handle errors and timeouts
- [ ] Add conversation context to requests

### 3. Chatbot AI Enhancement
- [ ] Connect frontend to new AI endpoint
- [ ] Display AI-generated responses
- [ ] Add loading states for AI thinking
- [ ] Handle streaming responses (optional advanced)
- [ ] Save both user messages and AI responses to database

## Career Lesson: "AI is changing the game - Adapt your skills to work WITH AI, not against it"

### Why This Matters
AI is fundamentally changing software development:
- AI coding assistants are now standard tools
- Many routine coding tasks are automated
- The role of developers is evolving rapidly
- Resistance to AI will limit career growth

### Real-World Application

**Embrace AI as a Tool**:
- Use AI coding assistants (GitHub Copilot, Cursor, etc.)
- Let AI handle boilerplate and repetitive code
- Focus on architecture, design, and complex problem solving
- Use AI to learn faster and explore new technologies

**Skills That Matter More Now**:
- **Critical Thinking**: Evaluate AI suggestions for correctness
- **Architecture**: Design systems AI can help implement
- **Communication**: Translate requirements into prompts
- **Domain Knowledge**: Understand the problem space deeply
- **Code Review**: Verify and improve AI-generated code

**Skills AI Can't Replace (Yet)**:
- Understanding business requirements and user needs
- Making architectural decisions with trade-offs
- Debugging complex cross-system issues
- Team collaboration and mentorship
- Creative problem solving for novel situations
- Ethical considerations and security awareness

**How to Adapt**:
- **Learn prompt engineering**: Get better results from AI
- **Understand AI limitations**: Know when to trust it
- **Focus on human skills**: Empathy, creativity, judgment
- **Move up the abstraction ladder**: Let AI handle details
- **Become a force multiplier**: Use AI to 10x your output

**Mindset Shift**:
- From "I write code" to "I architect solutions"
- From "AI will take my job" to "AI makes me more valuable"
- From "I know everything" to "I know how to find answers"
- From "Lone coder" to "AI-augmented developer"

### The Future is Collaborative
The best developers will be those who can effectively collaborate with both humans AND AI systems. This lesson is your first step in learning that collaboration.

## Project State After This Lesson
```
chatbot-project/
├── public/
│   ├── index.html
│   ├── styles.css
│   └── script.js (UPDATED: real AI responses)
├── src/
│   ├── server.js (UPDATED: Ollama proxy endpoints)
│   └── database.js
├── scripts/
│   └── pull-model.sh (NEW: helper for model management)
├── chatbot.db
├── package.json
├── .env (NEW: OLLAMA_HOST config)
├── README.md
└── .git/
```

Your chatbot now has:
- Real AI responses powered by local LLM
- Integration with Ollama API
- Conversation context maintained
- Model configuration via environment variables
- Both user and AI messages saved to database

## Additional Resources

### Essential Reading
- [Ollama Official Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Ollama Model Library](https://ollama.com/library)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

### Video Tutorials
- "What is a Large Language Model?"
- "Running LLMs Locally with Ollama"
- "Prompt Engineering Best Practices"

### Model Recommendations
- **Small/Fast** (for testing): qwen2.5:0.5b (0.4GB)
- **Balanced**: llama3.2:1b (1.3GB), phi3:3.8b (2.2GB)
- **Quality** (if you have RAM/GPU): llama3.1:8b (4.7GB)

### Practice Challenges
1. **Multi-Model Comparison**: Try 3 different models, compare responses
2. **System Prompts**: Give AI different personas (teacher, comedian, expert)
3. **Prompt Templates**: Create reusable prompt formats
4. **Streaming Implementation**: Add real-time streaming responses

## Common Mistakes to Avoid
- Using models too large for your hardware
- Not handling Ollama connection errors
- Forgetting to maintain conversation context
- Not limiting token usage (costs/performance)
- Sending sensitive data to cloud AI without consent
- Not validating AI responses before displaying

## Troubleshooting Common Issues

### Ollama Connection Failed
```bash
# Check if Ollama is running
ollama list

# Start Ollama if needed
ollama serve

# Check Ollama host in .env
OLLAMA_HOST=127.0.0.1:11434
```

### Model Not Found
```bash
# List available models
ollama list

# Pull required model
ollama pull qwen2.5:0.5b
```

### Slow Responses
- Try a smaller model
- Check system resources (RAM/CPU usage)
- Reduce max_tokens in requests
- Consider GPU acceleration if available

### Memory Issues
```bash
# Remove unused models
ollama rm <model-name>

# Check model sizes before pulling
ollama show <model-name>
```

## Code Example Structure

.env configuration:
```bash
OLLAMA_HOST=127.0.0.1:11434
OLLAMA_MODEL=qwen2.5:0.5b
PORT=3000
```

Server.js Ollama integration:
```javascript
// Proxy to Ollama chat endpoint
if (req.url === '/api/chat' && req.method === 'POST') {
  try {
    const body = await parseBody(req)

    const ollamaReq = http.request(`http://${OLLAMA_HOST}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    }, (ollamaRes) => {
      res.statusCode = ollamaRes.statusCode
      res.setHeader('Content-Type', 'application/json')
      ollamaRes.pipe(res)
    })

    ollamaReq.on('error', (error) => {
      res.statusCode = 500
      res.end(JSON.stringify({
        error: 'Ollama connection failed',
        details: error.message
      }))
    })

    ollamaReq.write(JSON.stringify(body))
    ollamaReq.end()
  } catch (error) {
    res.statusCode = 400
    res.end(JSON.stringify({ error: error.message }))
  }
  return
}
```

Frontend API call:
```javascript
const response = await fetch('/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    model: 'qwen2.5:0.5b',
    messages: conversationHistory,
    stream: false
  })
})

const data = await response.json()
const aiMessage = data.message
```

## Prompt Engineering Tips

### Basic Structure
```
[System Prompt] You are a helpful assistant...
[User Message] Explain quantum computing
[Context] Previous conversation...
```

### Effective Prompts
- Be specific and clear
- Provide context when needed
- Use examples (few-shot learning)
- Specify desired format
- Iterate and refine

### Example System Prompts
```
"You are a helpful coding assistant. Provide clear, concise answers."
"You are a patient teacher explaining concepts to beginners."
"You are an expert in [domain]. Give detailed technical responses."
```

## Next Week Preview
In Lesson 09, we'll add professional features to the chatbot: conversation history sidebar, conversation management, better UX, and polish the entire application. You'll learn about state management, UI patterns, and creating a complete user experience.

## Homework
1. Install Ollama and pull qwen2.5:0.5b model
2. Test model via Ollama CLI
3. Create proxy endpoint in server for Ollama
4. Connect frontend to real AI responses
5. Save AI responses to database
6. Add error handling for Ollama connection issues
7. Experiment with different system prompts
8. Test with at least 2 different models
9. Commit your work
10. Share your AI-powered chatbot on Discord!

**Congratulations!** You now have a fully functional AI chatbot running entirely on your local machine!
