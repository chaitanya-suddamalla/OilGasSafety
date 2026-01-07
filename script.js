// ============================================
// Oil & Gas Safety Bot - Frontend JavaScript
// ============================================

const API_BASE_URL = 'http://localhost:5000/api';
let isConnected = false;
let isLoading = false;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    checkConnectionStatus();
    setupEventListeners();
});

// ============================================
// Event Listeners
// ============================================

function setupEventListeners() {
    const queryForm = document.getElementById('queryForm');
    const queryInput = document.getElementById('queryInput');

    if (queryForm) {
        queryForm.addEventListener('submit', sendQuery);
    }

    // Allow Ctrl+Enter to send message
    if (queryInput) {
        queryInput.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'Enter') {
                sendQuery(e);
            }
        });
    }
}

// ============================================
// Connection Status
// ============================================

function checkConnectionStatus() {
    fetch(`${API_BASE_URL}/health`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'connected') {
                setConnected(true);
            }
        })
        .catch(() => {
            setConnected(false);
            console.log('Backend not available');
        });
}

function setConnected(connected) {
    isConnected = connected;
    const statusDot = document.getElementById('statusDot');
    const statusText = document.getElementById('statusText');

    if (statusDot) {
        if (connected) {
            statusDot.classList.add('connected');
            statusText.textContent = 'Connected';
        } else {
            statusDot.classList.remove('connected');
            statusText.textContent = 'Disconnected';
        }
    }
}

// ============================================
// Query Handling
// ============================================

async function sendQuery(event) {
    event.preventDefault();

    const queryInput = document.getElementById('queryInput');
    const query = queryInput.value.trim();

    if (!query) {
        alert('Please enter a question');
        return;
    }

    if (!isConnected) {
        alert('Bot is not connected. Make sure the server is running.');
        return;
    }

    if (isLoading) {
        return;
    }

    // Clear input
    queryInput.value = '';

    // Add user message to chat
    addMessage(query, 'user');

    // Set loading state
    setLoadingState(true);

    try {
        // Send query to backend
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Add bot response to chat
        if (data.response) {
            addMessage(data.response, 'bot');
        } else {
            addMessage('Sorry, I could not generate a response. Please try again.', 'bot');
        }

    } catch (error) {
        console.error('Error:', error);
        addMessage(
            'Error communicating with the server. Please make sure the backend is running on port 5000.',
            'bot'
        );
    } finally {
        setLoadingState(false);
        queryInput.focus();
    }
}

function askQuestion(question) {
    const queryInput = document.getElementById('queryInput');
    queryInput.value = question;
    queryInput.focus();
}

// ============================================
// Chat Display
// ============================================

function addMessage(text, sender) {
    const chatContainer = document.getElementById('chatContainer');

    // Remove welcome message on first real message
    if (chatContainer.querySelector('.welcome-message')) {
        const welcomeMsg = chatContainer.querySelector('.welcome-message');
        if (welcomeMsg && chatContainer.children.length === 1) {
            welcomeMsg.remove();
        }
    }

    // Create message element
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);

    // Create message content
    const contentDiv = document.createElement('div');
    contentDiv.classList.add('message-content');

    // Format and display the text
    if (sender === 'bot') {
        // Format bot response with better readability
        contentDiv.innerHTML = formatBotResponse(text);
    } else {
        contentDiv.textContent = text;
    }

    messageDiv.appendChild(contentDiv);

    // Add timestamp
    const timeDiv = document.createElement('div');
    timeDiv.classList.add('message-time');
    timeDiv.textContent = getCurrentTime();
    messageDiv.appendChild(timeDiv);

    // Add to chat
    chatContainer.appendChild(messageDiv);

    // Scroll to bottom
    scrollToBottom();
}

function addLoadingMessage() {
    const chatContainer = document.getElementById('chatContainer');

    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', 'bot');
    messageDiv.id = 'loading-message';

    const loadingDiv = document.createElement('div');
    loadingDiv.classList.add('loading');
    loadingDiv.innerHTML = '<span></span><span></span><span></span>';

    messageDiv.appendChild(loadingDiv);
    chatContainer.appendChild(messageDiv);

    scrollToBottom();
}

function removeLoadingMessage() {
    const loadingMsg = document.getElementById('loading-message');
    if (loadingMsg) {
        loadingMsg.remove();
    }
}

function formatBotResponse(text) {
    // Add line breaks for better readability
    let formatted = text
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>');

    // Split by common section markers and add formatting
    const sections = formatted.split(/<br>/);
    const processed = sections.map(section => {
        if (section.includes(':') && !section.includes('<strong>')) {
            return section.replace(/^([^:]+):/, '<strong>$1:</strong>');
        }
        return section;
    });

    return processed.join('<br>');
}

function scrollToBottom() {
    const chatContainer = document.getElementById('chatContainer');
    setTimeout(() => {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }, 100);
}

function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// ============================================
// Loading State
// ============================================

function setLoadingState(loading) {
    isLoading = loading;
    const sendBtn = document.getElementById('sendBtn');
    const sendBtnText = document.getElementById('sendBtnText');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const queryInput = document.getElementById('queryInput');

    if (loading) {
        sendBtn.disabled = true;
        queryInput.disabled = true;
        sendBtnText.style.display = 'none';
        loadingSpinner.style.display = 'inline';
        addLoadingMessage();
    } else {
        sendBtn.disabled = false;
        queryInput.disabled = false;
        sendBtnText.style.display = 'inline';
        loadingSpinner.style.display = 'none';
        removeLoadingMessage();
    }
}

// ============================================
// Utilities
// ============================================

function clearChat() {
    const chatContainer = document.getElementById('chatContainer');
    chatContainer.innerHTML = `
        <div class="welcome-message">
            <h2>Welcome to Safety Bot</h2>
            <p>Ask any safety-related questions about oil & gas operations.</p>
            <p class="disclaimer">⚠️ <strong>Educational Information Only:</strong> Always consult certified professionals for operational decisions.</p>
        </div>
    `;
}

// Health check periodically
setInterval(() => {
    checkConnectionStatus();
}, 30000); // Every 30 seconds
