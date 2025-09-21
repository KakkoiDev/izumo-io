// elements
const messagesDiv = document.body.querySelector('#messages')
const chatInput = document.body.querySelector('#chat-input')
const sendButton = document.body.querySelector('#send-button')

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
  messageDiv.innerText = "Thinking"

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

  // parse reponse to JS object
  const assistantData = await assistantResponse.json()
  const assistantMessage = assistantData.message

  // add assistant message to messages list
  messages.push(assistantMessage)
  removeAssistantThinkingMessage()
  addMessage(assistantMessage)
  localStorage.setItem('messages', JSON.stringify(messages))
  scrollToBottom()
}

// array containing all the messages of the conversation
const messages = localStorage.getItem('messages')
  ? JSON.parse(localStorage.getItem('messages'))
  : []

// generate the divs of all the messages in the conversation
for (const message of messages) {
  addMessage(message)
}

scrollToBottom()

// when click send button, send new user message
sendButton.addEventListener('click', () => {
  sendMessage(chatInput, messages)
})
// when press "enter" key, send new user message
document.addEventListener('keydown', (event) => {
  if (event.key !== 'Enter') return

  sendMessage(chatInput, messages)
})