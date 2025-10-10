// LocalStorage key for saving messages
const STORAGE_KEY = 'chatbot-messages'

// Function to load messages from localStorage
const loadMessages = () => {
  const stored = localStorage.getItem(STORAGE_KEY)
  return stored ? JSON.parse(stored) : []
}

// Function to save messages to localStorage
const saveMessages = (messages) => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(messages))
}

// Function to add a message to the chat
const addMessage = (message) => {
  const messagesDiv = document.getElementById('messages')

  // Create message div
  const messageDiv = document.createElement('div')
  messageDiv.className = message.sender === 'user' ? 'user-message' : 'ai-message'
  messageDiv.textContent = message.content

  // Append message to messages container
  messagesDiv.appendChild(messageDiv)

  // Scroll to bottom
  messagesDiv.scrollTop = messagesDiv.scrollHeight
}

// Mock AI response function (simulates API call)
const getAIResponse = async (userMessage) => {
  // Simulate network delay
  await new Promise(resolve => setTimeout(resolve, 1000))

  // Simple mock responses based on keywords
  const lowerMessage = userMessage.toLowerCase()

  if (lowerMessage.includes('hello') || lowerMessage.includes('hi')) {
    return 'Hello! How can I assist you today?'
  } else if (lowerMessage.includes('help')) {
    return 'I\'m here to help! You can ask me anything.'
  } else if (lowerMessage.includes('programming') || lowerMessage.includes('code')) {
    return 'Programming is a great skill to learn! What language are you interested in?'
  } else {
    return 'That\'s interesting! Tell me more.'
  }
}

// Function to send a new message
const sendMessage = async () => {
  const input = document.getElementById('chat-input')
  const sendButton = document.getElementById('send-button')
  const inputValue = input.value.trim()

  // If no text in input, don't send
  if (!inputValue) return

  // Disable input while processing
  input.disabled = true
  sendButton.disabled = true

  // Create new user message object
  const userMessage = {
    sender: 'user',
    content: inputValue
  }

  // Add message to messages array
  messages.push(userMessage)

  // Display the message
  addMessage(userMessage)

  // Clear input
  input.value = ''

  // Save messages to localStorage
  saveMessages(messages)

  // Get AI response
  try {
    const aiResponseText = await getAIResponse(inputValue)

    const aiMessage = {
      sender: 'ai',
      content: aiResponseText
    }

    // Add AI response to messages array
    messages.push(aiMessage)

    // Display AI response
    addMessage(aiMessage)

    // Save messages to localStorage
    saveMessages(messages)
  } catch (error) {
    console.error('Error getting AI response:', error)

    const errorMessage = {
      sender: 'ai',
      content: 'Sorry, I encountered an error. Please try again.'
    }

    messages.push(errorMessage)
    addMessage(errorMessage)
    saveMessages(messages)
  }

  // Re-enable input
  input.disabled = false
  sendButton.disabled = false
  input.focus()
}

// Load messages from localStorage
const messages = loadMessages()

// Get elements
const chatInput = document.getElementById('chat-input')
const sendButton = document.getElementById('send-button')

// Display existing messages or add welcome message
if (messages.length === 0) {
  const welcomeMessage = {
    sender: 'ai',
    content: 'Hello! I\'m your AI assistant. How can I help you today?'
  }
  messages.push(welcomeMessage)
  saveMessages(messages)
  addMessage(welcomeMessage)
} else {
  // Display all saved messages
  messages.forEach(message => addMessage(message))
}

// Send message when button is clicked
sendButton.addEventListener('click', sendMessage)

// Send message when Enter key is pressed
chatInput.addEventListener('keypress', (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    sendMessage()
  }
})

// Focus input on page load
chatInput.focus()
