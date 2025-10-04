// Configuration
const API_BASE_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : 'https://your-railway-app.up.railway.app'; // Replace with your Railway URL after deployment

// State management
let conversationHistory = [];
let isLoading = false;

// DOM elements
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const typingIndicator = document.getElementById('typing-indicator');

// Initialize the chat
async function initializeChat() {
    try {
        const response = await fetch(`${API_BASE_URL}/welcome`);

        if (!response.ok) {
            throw new Error('Failed to fetch welcome message');
        }

        const data = await response.json();
        addMessage('assistant', data.message);
    } catch (error) {
        console.error('Error initializing chat:', error);
        addMessage('assistant', 'Hello! I\'m an AI assistant representing Ruomu Shao. How can I help you today?');
    }
}

// Add message to chat
function addMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = role === 'user' ? 'You' : 'AI';

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = content;

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);

    chatMessages.appendChild(messageDiv);
    scrollToBottom();

    // Add to conversation history (exclude system messages)
    if (role !== 'system') {
        conversationHistory.push({ role, content });
    }
}

// Add error message
function addErrorMessage(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = `Error: ${message}`;
    chatMessages.appendChild(errorDiv);
    scrollToBottom();
}

// Show/hide typing indicator
function setTypingIndicator(visible) {
    typingIndicator.style.display = visible ? 'flex' : 'none';
    if (visible) {
        scrollToBottom();
    }
}

// Scroll to bottom of chat
function scrollToBottom() {
    chatMessages.parentElement.scrollTop = chatMessages.parentElement.scrollHeight;
}

// Send message to API
async function sendMessage() {
    const message = userInput.value.trim();

    if (!message || isLoading) {
        return;
    }

    // Add user message to chat
    addMessage('user', message);
    userInput.value = '';

    // Set loading state
    isLoading = true;
    sendButton.disabled = true;
    setTypingIndicator(true);

    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                conversation_history: conversationHistory.slice(-10) // Send last 10 messages
            })
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP error ${response.status}`);
        }

        const data = await response.json();

        // Add AI response to chat
        addMessage('assistant', data.response);

    } catch (error) {
        console.error('Error sending message:', error);

        let errorMessage = 'Failed to get response. Please try again.';

        if (error.message.includes('Failed to fetch')) {
            errorMessage = 'Cannot connect to the server. Please check if the backend is running.';
        } else if (error.message) {
            errorMessage = error.message;
        }

        addErrorMessage(errorMessage);

    } finally {
        // Reset loading state
        isLoading = false;
        sendButton.disabled = false;
        setTypingIndicator(false);
        userInput.focus();
    }
}

// Event listeners
sendButton.addEventListener('click', sendMessage);

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Prevent form submission if wrapped in a form
userInput.addEventListener('submit', (e) => {
    e.preventDefault();
});

// Focus input on load
userInput.focus();

// Initialize chat when page loads
document.addEventListener('DOMContentLoaded', initializeChat);
