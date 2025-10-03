// elements
const messagesDiv = document.body.querySelector('#messages')
const chatInput = document.body.querySelector('#chat-input')
const sendButton = document.body.querySelector('#send-button')
const openMenuButton = document.body.querySelector('#open-menu')
const closeMenuButton = document.body.querySelector('#close-menu')
const menuPanelDiv = document.body.querySelector('#menu-panel')
const chatMain = document.body.querySelector('#chat')

// variables
let conversations = []
let currentConversationId = null

// constants
const DEFAULT_TITLE = 'Untitled'
const STORAGE_CONVERSATIONS = 'conversations'
const STORAGE_CURRENT_ID = 'currentConversationId'

// CONVERSATION MANAGEMENT FUNCTIONS
// Create a new conversation
const createNewConversation = () => {
  const newConversation = {
    id: Date.now().toString(),
    title: DEFAULT_TITLE,
    messages: []
  }
  conversations.push(newConversation)
  currentConversationId = newConversation.id
  saveConversations()
  renderConversationsList()
  clearChatDisplay()
  return newConversation
}

// Load current conversation messages
const loadCurrentConversation = () => {
  const conversation = conversations.find(c => c.id === currentConversationId)
  return conversation ? conversation.messages : []
}

// Save current conversation state
const saveCurrentConversation = () => {
  const conversation = conversations.find(c => c.id === currentConversationId)
  if (conversation) {
    saveConversations()
  }
}

// Save all conversations to localStorage
const saveConversations = () => {
  localStorage.setItem(STORAGE_CONVERSATIONS, JSON.stringify(conversations))
  localStorage.setItem(STORAGE_CURRENT_ID, currentConversationId)
}

// Switch to a different conversation
const switchConversation = (conversationId) => {
  currentConversationId = conversationId
  localStorage.setItem(STORAGE_CURRENT_ID, currentConversationId)
  renderConversationsList()
  displayConversation()
  menuPanelDiv.classList.remove('show-menu-panel')
}

// Delete a conversation
const deleteConversation = (conversationId) => {
  // Remove from conversations array
  conversations = conversations.filter(c => c.id !== conversationId)

  // If deleting current conversation, switch to another
  if (currentConversationId === conversationId) {
    if (conversations.length > 0) {
      currentConversationId = conversations[0].id
    } else {
      // Create a new conversation if none left
      createNewConversation()
      displayConversation()
      return
    }
  }

  saveConversations()
  renderConversationsList()
  displayConversation()
}

// Clear chat display
const clearChatDisplay = () => {
  messagesDiv.innerHTML = ''
}

// Display current conversation
const displayConversation = () => {
  clearChatDisplay()
  const messages = loadCurrentConversation()
  for (const message of messages) {
    addMessage(message)
  }
  // Use wrapper to ensure scroll happens after layout calculation
  afterLayout(() => {
    scrollToBottom()
    chatInput.focus()
  })
}

// Generate title for conversation using AI
const generateTitle = async (messages) => {
  try {
    const conversationContent = messages.slice(0, 4).map(m => `${m.role}: ${m.content}`).join('\n')

    const response = await fetch('http://localhost:8081/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: 'qwen2.5:0.5b',
        prompt: `Generate a short 3-5 word title for this conversation:\n${conversationContent}`,
        stream: false
      })
    })

    if (response.ok) {
      const data = await response.json()
      // Clean up the response - remove quotes, trim whitespace
      const title = data.response.replace(/['"]/g, '').trim().substring(0, 50)
      return title || DEFAULT_TITLE
    }
  } catch (error) {
    console.error('Error generating title:', error)
  }
  return DEFAULT_TITLE
}

// Render conversations list in menu
const renderConversationsList = () => {
  const conversationsList = document.querySelector('#conversations-list')
  conversationsList.innerHTML = ''

  conversations.forEach(conv => {
    const li = document.createElement('li')
    li.className = 'conversation'
    li.dataset.id = conv.id

    if (conv.id === currentConversationId) {
      li.classList.add('active')
    }

    li.innerHTML = `
      <span class="title">${conv.title || DEFAULT_TITLE}</span>
      <button class="options" popovertarget="options-${conv.id}">⋮</button>
      <div popover id="options-${conv.id}">
        <button class="rename-btn" data-id="${conv.id}" popovertarget="options-${conv.id}" popovertargetaction="hide">✏️ Rename</button>
        <button class="delete-btn" data-id="${conv.id}" popovertarget="options-${conv.id}" popovertargetaction="hide">🗑️ Delete</button>
      </div>
    `

    conversationsList.appendChild(li)
  })
}

// CHAT FUNCTIONS
// scroll to page bottom
const scrollToBottom = () => window.scrollTo(0, document.body.scrollHeight)

// Double requestAnimationFrame wrapper for accurate DOM measurements
// Why: Browsers need time to calculate layout after DOM changes before measurements are accurate
// How it works:
//   1st rAF: Waits for next paint cycle after DOM manipulation
//   2nd rAF: Ensures layout calculations are complete
// This adds ~16-32ms delay (1-2 frames) but guarantees reliable DOM operations
// Reference: https://nolanlawson.com/2018/09/25/accurately-measuring-layout-on-the-web/
const afterLayout = (callback) => {
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      callback()
    })
  })
}

const addMessage = (message) => {
  // create message div
  const messageDiv = document.createElement('div')
  messageDiv.classList.add(message.role === 'assistant' ? 'assistant-message' : 'user-message')
  messageDiv.innerText = message.content

  // append message div to messages
  messagesDiv.appendChild(messageDiv)
}

// add temporary assistant thinking message
const addAssistantThinkingMessage = () => {
  // create message div
  const messageDiv = document.createElement('div')
  messageDiv.id = 'assistant-thinking-message'
  messageDiv.classList.add('assistant-message')
  messageDiv.innerText = "🤖 Thinking"

  // append message div to messages
  messagesDiv.appendChild(messageDiv)
}

// remove temporary assistant thinking message
const removeAssistantThinkingMessage = () => {
  const messageDiv = document.querySelector('#assistant-thinking-message')
  messageDiv.remove()
}

// send new message to AI
const sendMessage = async (input) => {
  const inputValue = input.value

  // if no text in input, don't send
  if (!inputValue) return

  // Get current conversation
  const conversation = conversations.find(c => c.id === currentConversationId)
  if (!conversation) return

  // new message
  const message = {
    role: 'user',
    content: input.value
  }

  // add to messages list
  conversation.messages.push(message)

  // add new message to messages div
  addMessage(message)

  addAssistantThinkingMessage()
  scrollToBottom()

  // clear input
  input.value = ''

  // save conversations
  saveConversations()

  // send the query to the AI model
  const assistantResponse = await fetch('http://localhost:8081/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: 'qwen2.5:0.5b',
      messages: conversation.messages,
      stream: false
    })
  });

  // parse response to JS object
  const assistantData = await assistantResponse.json()
  const assistantMessage = assistantData.message

  // add assistant message to messages list
  conversation.messages.push(assistantMessage)
  removeAssistantThinkingMessage()
  addMessage(assistantMessage)

  // Generate title on first AI response if untitled
  if (conversation.messages.length === 2 && conversation.title === DEFAULT_TITLE) {
    conversation.title = await generateTitle(conversation.messages)
    renderConversationsList()
  }

  saveConversations()
  scrollToBottom()
}

// INITIALIZATION
const initializeConversations = () => {
  // Try to load existing conversations
  const savedConversations = localStorage.getItem(STORAGE_CONVERSATIONS)
  const savedCurrentId = localStorage.getItem(STORAGE_CURRENT_ID)

  if (savedConversations) {
    conversations = JSON.parse(savedConversations)
    currentConversationId = savedCurrentId

    // Verify current conversation still exists
    if (!conversations.find(c => c.id === currentConversationId)) {
      currentConversationId = conversations.length > 0 ? conversations[0].id : null
    }
  }

  // Create first conversation if none exist
  if (conversations.length === 0) {
    createNewConversation()
  }

  // Ensure we have a current conversation
  if (!currentConversationId && conversations.length > 0) {
    currentConversationId = conversations[0].id
  }
}

// INIT
initializeConversations()
renderConversationsList()
displayConversation()

// EVENTS
// when click send button, send new user message
sendButton.addEventListener('click', () => {
  sendMessage(chatInput)
})

// when press "enter" key, send new user message
document.addEventListener('keydown', (event) => {
  if (event.key !== 'Enter') return
  sendMessage(chatInput)
})

// when click on open-menu button, open the menu
openMenuButton.addEventListener('click', () => {
  menuPanelDiv.classList.add('show-menu-panel')
})

// when click on close-menu button, close the menu
closeMenuButton.addEventListener('click', () => {
  menuPanelDiv.classList.remove('show-menu-panel')
})

// when click on the chat area when the menu is opened, close the menu
chatMain.addEventListener('click', () => {
  menuPanelDiv.classList.remove('show-menu-panel')
})

// Event delegation for conversation switching
document.querySelector('#conversations-list').addEventListener('click', (e) => {
  const conversationEl = e.target.closest('.conversation')
  if (conversationEl &&
      !e.target.closest('.options') &&
      !e.target.closest('[popover]')
     ) {
    const convId = conversationEl.dataset.id
    switchConversation(convId)
  }
})

// New conversation button event
document.addEventListener('click', (e) => {
  if (e.target.id === 'new-conversation-btn') {
    createNewConversation()
    displayConversation()
    menuPanelDiv.classList.remove('show-menu-panel')
  }

  // Delete conversation button
  if (e.target.classList.contains('delete-btn')) {
    const conversationId = e.target.dataset.id
    deleteConversation(conversationId)
  }
})
