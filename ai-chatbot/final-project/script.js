// elements
const messagesDiv = document.body.querySelector('#messages')
const chatInput = document.body.querySelector('#chat-input')
const sendButton = document.body.querySelector('#send-button')
const openMenuButton = document.body.querySelector('#open-menu')
const closeMenuButton = document.body.querySelector('#close-menu')
const menuPanelDiv = document.body.querySelector('#menu-panel')

// variables
// array containing all the messages of the conversation
const messages = localStorage.getItem('messages')
  ? JSON.parse(localStorage.getItem('messages'))
  : []


// scroll to page bottom
const scrollToBottom = () => window.scrollTo(0, document.body.scrollHeight)
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
// input: the input element used to send the message
// messages: the array of messages
const sendMessage = async (input, messages) => {
  const inputValue = input.value

  // if no text in input, don't send
  if (!inputValue) return

  // new message
  const message = {
    role: 'user',
    content: input.value
  }

  // add to messages list
  messages.push(message)

  // add new message to messages div
  addMessage(message)

  addAssistantThinkingMessage()
  scrollToBottom()

  // clear input
  input.value = ''

  // save messages in local storage
  localStorage.setItem('messages', JSON.stringify(messages))

  // send the query to the AI model
  const assistantResponse = await fetch('http://localhost:8081/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: 'qwen2.5:0.5b',
      messages: messages,
      stream: false
    })
  });

  // parse response to JS object
  const assistantData = await assistantResponse.json()
  const assistantMessage = assistantData.message

  // add assistant message to messages list
  messages.push(assistantMessage)
  removeAssistantThinkingMessage()
  addMessage(assistantMessage)
  localStorage.setItem('messages', JSON.stringify(messages))
  scrollToBottom()
}

// INIT
// generate the divs of all the messages in the conversation
for (const message of messages) {
  addMessage(message)
}

// Double requestAnimationFrame technique for accurate scrolling
// Why: Browsers need time to calculate layout after DOM changes before scrollHeight is accurate
// How it works:
//   1st rAF: Waits for next paint cycle after DOM manipulation
//   2nd rAF: Ensures layout calculations are complete
// This adds ~16-32ms delay (1-2 frames) but guarantees reliable scrolling
// Reference: https://nolanlawson.com/2018/09/25/accurately-measuring-layout-on-the-web/
requestAnimationFrame(() => {
  requestAnimationFrame(() => {
    scrollToBottom()
  })
})

// EVENTS
// when click send button, send new user message
sendButton.addEventListener('click', () => {
  sendMessage(chatInput, messages)
})

// when press "enter" key, send new user message
document.addEventListener('keydown', (event) => {
  if (event.key !== 'Enter') return

  sendMessage(chatInput, messages)
})

// when click on open-menu button, open the menu
openMenuButton.addEventListener('click', () => {
  menuPanelDiv.classList.add('show-menu-panel')
})

// when click on close-menu button, close the menu
closeMenuButton.addEventListener('click', () => {
  menuPanelDiv.classList.remove('show-menu-panel')
})
