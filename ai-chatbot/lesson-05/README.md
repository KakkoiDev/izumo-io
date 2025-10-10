# Lesson 05: Advanced JavaScript & API Concepts

## Theme: "Connected Thinking - Understanding How Systems Work Together"

## Learning Objectives
By the end of this lesson, you will:
- Understand asynchronous programming with Promises and async/await
- Learn how to make HTTP requests to APIs
- Handle JSON data format
- Implement error handling and loading states
- Prepare chatbot for external AI service integration

## What We're Learning This Week

### Technical Concepts
- **Asynchronous Programming**: Understanding non-blocking code
- **Promises**: Handling operations that take time
- **async/await**: Modern syntax for async code
- **fetch() API**: Making HTTP requests
- **JSON**: JavaScript Object Notation for data exchange
- **Error Handling**: try/catch blocks and error states
- **Loading States**: Providing feedback during async operations

### JavaScript Concepts Focus
- `Promise` - Representing future values
- `async`/`await` - Writing async code that looks synchronous
- `fetch()` - Making network requests
- `JSON.parse()`, `JSON.stringify()` - Working with JSON
- `try...catch` - Handling errors gracefully

## This Week's Tasks

### 1. Async JavaScript Fundamentals
- [ ] Understand the event loop and async behavior
- [ ] Learn about Promises and how they work
- [ ] Master async/await syntax
- [ ] Practice error handling with try/catch

### 2. API Integration Preparation
- [ ] Learn about REST APIs and HTTP methods
- [ ] Understand request/response cycle
- [ ] Practice with fetch() on public APIs
- [ ] Handle JSON data parsing

### 3. Chatbot Enhancement
- [ ] Create mock API response function (simulates AI)
- [ ] Add loading indicator while "thinking"
- [ ] Display mock AI responses in chat
- [ ] Implement error handling for failed requests
- [ ] Add timeout handling for slow responses

## Career Lesson: "Managing back-stabbing in the office - Navigating workplace politics and protecting your work"

### Why This Matters
Workplace politics exists in every organization:
- Colleagues may take credit for your work
- Competition for promotions can get ugly
- Information sharing can be weaponized
- Trust is earned, not automatic

### Real-World Application

**Protect Yourself**:
- Document your contributions (commit messages, emails, project notes)
- CC relevant people on important communications
- Keep a work journal of accomplishments
- Present your work in team meetings

**Build Alliances**:
- Form genuine relationships with colleagues
- Help others succeed (reciprocity matters)
- Find mentors who advocate for you
- Build reputation through consistent quality

**Navigate Politics**:
- Don't engage in gossip or backstabbing yourself
- Focus on results and measurable impact
- Communicate achievements without bragging
- Know when to escalate issues to management

**Red Flags**:
- Someone consistently takes credit for team work
- Your ideas appear as others' proposals
- Information you share is used against you
- Lack of recognition despite clear contributions

**When to Leave**:
- Toxic culture that rewards politics over performance
- Your mental health is suffering
- No path forward despite your efforts
- Better opportunities align with your values

## Project State After This Lesson
```
chatbot-project/
├── index.html
├── styles.css
├── script.js (ENHANCED: async, fetch, mock AI responses)
├── README.md
└── .git/
```

Your chatbot should now:
- Show "Thinking..." indicator when processing
- Simulate AI responses with mock data
- Handle async operations properly
- Display loading states to user
- Gracefully handle errors
- Work with JSON data structures

## Additional Resources

### Essential Reading
- [MDN Promises Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises)
- [MDN async/await](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Async_await)
- [MDN Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)
- [JSON.org](https://www.json.org/) - Understanding JSON format

### Video Tutorials
- "Async JavaScript in 100 Seconds"
- "Promises vs Async/Await"
- "Fetch API Crash Course"
- "Understanding the Event Loop"

### Practice Challenges
1. **API Explorer**: Build interface to test public APIs (like dog.ceo or cat facts)
2. **Loading States**: Create different loading animations (spinner, dots, skeleton)
3. **Error Scenarios**: Handle different error types (network, timeout, invalid data)
4. **Data Transformation**: Fetch data from API and transform it for display

## Common Mistakes to Avoid
- Not handling promise rejections (unhandled promise errors)
- Forgetting `await` keyword with async functions
- Not providing loading feedback to users
- Parsing JSON without try/catch
- Mixing callbacks with promises/async-await
- Not checking response status before parsing JSON

## Troubleshooting Common Issues

### Promise Never Resolves
```javascript
// Always handle both success and error
async function getData() {
  try {
    const response = await fetch(url)
    if (!response.ok) throw new Error('Failed')
    return await response.json()
  } catch (error) {
    console.error('Error:', error)
    // Handle error appropriately
  }
}
```

### CORS Errors
- CORS errors occur when calling APIs from different domains
- For learning, use public APIs that allow CORS
- Later, you'll proxy requests through your own server (Lesson 06)

### JSON Parse Errors
```javascript
// Always validate before parsing
try {
  const data = JSON.parse(responseText)
} catch (error) {
  console.error('Invalid JSON:', error)
}
```

## Code Example Structure

Your enhanced script.js should include:
```javascript
// Mock AI response function (simulates API call)
async function getMockAIResponse(userMessage) {
  // Simulate network delay
  await new Promise(resolve => setTimeout(resolve, 1000))

  // Return mock response
  return {
    message: `I received: "${userMessage}". This is a mock response!`
  }
}

// Enhanced send message with async
async function sendMessage() {
  const messageText = input.value.trim()
  if (!messageText) return

  // Add user message
  addMessageToChat('user', messageText)
  input.value = ''

  // Show loading indicator
  showLoadingIndicator()

  try {
    // Get AI response
    const response = await getMockAIResponse(messageText)

    // Hide loading and show response
    hideLoadingIndicator()
    addMessageToChat('assistant', response.message)
  } catch (error) {
    hideLoadingIndicator()
    addMessageToChat('error', 'Sorry, something went wrong!')
    console.error('Error:', error)
  }
}
```

## Next Week Preview
In Lesson 06, we'll set up a Node.js server to handle our backend logic. You'll learn about server-side JavaScript, Express.js, and how to create API endpoints for your chatbot.

## Homework
1. Implement mock AI response with async/await
2. Add loading indicator ("Thinking..." or spinner)
3. Handle errors gracefully with try/catch
4. Test with public API (optional: weather, jokes, quotes)
5. Add 1-2 second delay to mock responses to simulate real API
6. Commit your work
7. Share your async chatbot on Discord
