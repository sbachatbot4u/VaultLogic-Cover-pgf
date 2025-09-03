// VaultLogic Chat Interface JavaScript

(function() {
    'use strict';

    let chatMessages = [];
    let isTyping = false;

    document.addEventListener('DOMContentLoaded', function() {
        initializeChat();
    });

    function initializeChat() {
        const chatForm = document.getElementById('chatForm');
        const chatMessagesContainer = document.getElementById('chatMessages');
        const questionInput = document.getElementById('question');
        const sendButton = document.getElementById('sendButton');
        const typingIndicator = document.getElementById('typingIndicator');
        const predefinedButtons = document.querySelectorAll('.predefined-question');

        if (!chatForm || !chatMessagesContainer) {
            console.warn('Chat elements not found - chat functionality disabled');
            return;
        }

        // Initialize predefined questions
        initPredefinedQuestions(predefinedButtons, questionInput);
        
        // Handle form submission
        chatForm.addEventListener('submit', handleChatSubmission);
        
        // Handle enter key in input
        if (questionInput) {
            questionInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    chatForm.dispatchEvent(new Event('submit'));
                }
            });
            
            // Auto-resize textarea if needed
            questionInput.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = this.scrollHeight + 'px';
            });
        }

        // Scroll to bottom on page load
        scrollToBottom();
    }

    function initPredefinedQuestions(buttons, questionInput) {
        buttons.forEach(button => {
            button.addEventListener('click', function() {
                const question = this.getAttribute('data-question');
                if (questionInput && question) {
                    questionInput.value = question;
                    // Auto-submit the question
                    submitChatQuestion(question);
                }
            });
        });
    }

    function handleChatSubmission(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const question = formData.get('question');
        
        if (!question || question.trim() === '') {
            showAlert('Please enter a question.', 'warning');
            return;
        }

        submitChatQuestion(question.trim());
    }

    function submitChatQuestion(question) {
        if (isTyping) {
            showAlert('Please wait for the current response to complete.', 'info');
            return;
        }

        // Add user message to chat
        addMessage(question, 'user');
        
        // Clear input
        const questionInput = document.getElementById('question');
        if (questionInput) {
            questionInput.value = '';
            questionInput.style.height = 'auto';
        }

        // Show typing indicator
        showTypingIndicator();
        
        // Disable form
        setFormDisabled(true);

        // Send request to backend
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCSRFToken()
            },
            body: `question=${encodeURIComponent(question)}&csrf_token=${getCSRFToken()}`
        })
        .then(response => response.json())
        .then(handleChatResponse)
        .catch(handleChatError)
        .finally(() => {
            hideTypingIndicator();
            setFormDisabled(false);
        });
    }

    function handleChatResponse(data) {
        if (data.success) {
            const answer = data.answer;
            const sources = data.sources || [];
            
            // Add assistant response to chat
            addMessage(answer, 'assistant', sources);
            
            // Update chat statistics if elements exist
            updateChatStats();
        } else {
            const errorMessage = data.error || 'Sorry, I couldn\'t process your question. Please try again.';
            addMessage(errorMessage, 'assistant', [], true);
            showAlert('Failed to get response. Please try again.', 'danger');
        }
    }

    function handleChatError(error) {
        console.error('Chat request failed:', error);
        addMessage('I\'m experiencing technical difficulties. Please try again in a moment.', 'assistant', [], true);
        showAlert('Network error. Please check your connection and try again.', 'danger');
    }

    function addMessage(content, sender, sources = [], isError = false) {
        const chatMessagesContainer = document.getElementById('chatMessages');
        if (!chatMessagesContainer) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        if (isError) {
            messageContent.classList.add('text-danger');
            messageContent.innerHTML = `<i class="fas fa-exclamation-triangle me-2"></i>${content}`;
        } else {
            messageContent.innerHTML = formatMessageContent(content);
        }
        
        messageDiv.appendChild(messageContent);
        
        // Add sources if provided
        if (sources && sources.length > 0 && !isError) {
            const sourcesDiv = document.createElement('div');
            sourcesDiv.className = 'sources';
            sourcesDiv.innerHTML = `
                <strong>Sources:</strong><br>
                ${sources.map(source => `<i class="fas fa-file-alt me-1"></i>${source}`).join('<br>')}
            `;
            messageDiv.appendChild(sourcesDiv);
        }
        
        // Add timestamp for assistant messages
        if (sender === 'assistant' && !isError) {
            const timestamp = document.createElement('div');
            timestamp.className = 'text-muted small mt-1';
            timestamp.innerHTML = `<i class="fas fa-clock me-1"></i>${new Date().toLocaleTimeString()}`;
            messageDiv.appendChild(timestamp);
        }
        
        chatMessagesContainer.appendChild(messageDiv);
        
        // Add to messages array
        chatMessages.push({
            content,
            sender,
            sources,
            timestamp: new Date(),
            isError
        });
        
        // Scroll to bottom
        scrollToBottom();
    }

    function formatMessageContent(content) {
        // Basic markdown-like formatting
        let formatted = content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>')
            .replace(/\n/g, '<br>');
        
        // Auto-link URLs
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        formatted = formatted.replace(urlRegex, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>');
        
        return formatted;
    }

    function showTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.style.display = 'block';
            isTyping = true;
            scrollToBottom();
        }
    }

    function hideTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.style.display = 'none';
            isTyping = false;
        }
    }

    function setFormDisabled(disabled) {
        const chatForm = document.getElementById('chatForm');
        const questionInput = document.getElementById('question');
        const sendButton = document.getElementById('sendButton');
        
        if (chatForm) {
            chatForm.classList.toggle('loading', disabled);
        }
        
        if (questionInput) {
            questionInput.disabled = disabled;
        }
        
        if (sendButton) {
            sendButton.disabled = disabled;
            
            if (disabled) {
                sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            } else {
                sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
            }
        }
    }

    function scrollToBottom() {
        const chatMessagesContainer = document.getElementById('chatMessages');
        if (chatMessagesContainer) {
            setTimeout(() => {
                chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
            }, 100);
        }
    }

    function updateChatStats() {
        // Update any statistics on the page
        const statsElements = {
            totalQuestions: document.querySelector('[data-stat="total-questions"]'),
            responseTime: document.querySelector('[data-stat="response-time"]'),
            accuracy: document.querySelector('[data-stat="accuracy"]')
        };
        
        if (statsElements.totalQuestions) {
            const currentCount = parseInt(statsElements.totalQuestions.textContent) || 0;
            statsElements.totalQuestions.textContent = currentCount + 1;
        }
    }

    function getCSRFToken() {
        const csrfInput = document.querySelector('input[name="csrf_token"]');
        return csrfInput ? csrfInput.value : '';
    }

    function showAlert(message, type = 'info') {
        // Use the global alert function if available
        if (window.VaultLogic && window.VaultLogic.showAlert) {
            window.VaultLogic.showAlert(message, type);
        } else {
            alert(message);
        }
    }

    // Random predefined question feature
    function getRandomPredefinedQuestion() {
        fetch('/api/predefined-question')
            .then(response => response.json())
            .then(data => {
                if (data.question) {
                    const questionInput = document.getElementById('question');
                    if (questionInput) {
                        questionInput.value = data.question;
                        submitChatQuestion(data.question);
                    }
                }
            })
            .catch(error => {
                console.error('Failed to get predefined question:', error);
                showAlert('Failed to load example question.', 'warning');
            });
    }

    // Export chat functionality
    window.submitChatQuestion = submitChatQuestion;
    window.getRandomPredefinedQuestion = getRandomPredefinedQuestion;

    // Chat keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to submit
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const chatForm = document.getElementById('chatForm');
            if (chatForm) {
                chatForm.dispatchEvent(new Event('submit'));
            }
        }
        
        // Escape to clear input
        if (e.key === 'Escape') {
            const questionInput = document.getElementById('question');
            if (questionInput && questionInput === document.activeElement) {
                questionInput.value = '';
                questionInput.blur();
            }
        }
    });

    // Auto-save chat history to localStorage
    function saveChatHistory() {
        try {
            localStorage.setItem('vaultlogic_chat_history', JSON.stringify(chatMessages));
        } catch (e) {
            console.warn('Failed to save chat history:', e);
        }
    }

    function loadChatHistory() {
        try {
            const saved = localStorage.getItem('vaultlogic_chat_history');
            if (saved) {
                const history = JSON.parse(saved);
                // Only load recent messages (last 10)
                const recentMessages = history.slice(-10);
                recentMessages.forEach(msg => {
                    if (msg.sender !== 'assistant' || !msg.content.includes('Welcome to the VaultLogic')) {
                        addMessage(msg.content, msg.sender, msg.sources, msg.isError);
                    }
                });
            }
        } catch (e) {
            console.warn('Failed to load chat history:', e);
        }
    }

    // Save chat history when messages are added
    const originalAddMessage = addMessage;
    addMessage = function(content, sender, sources = [], isError = false) {
        originalAddMessage(content, sender, sources, isError);
        saveChatHistory();
    };

    // Load chat history on page load (commented out to avoid conflicts with demo)
    // loadChatHistory();

    // Clear chat history button (if exists)
    const clearChatButton = document.getElementById('clearChat');
    if (clearChatButton) {
        clearChatButton.addEventListener('click', function() {
            if (confirm('Are you sure you want to clear the chat history?')) {
                chatMessages = [];
                const chatMessagesContainer = document.getElementById('chatMessages');
                if (chatMessagesContainer) {
                    // Keep only the welcome message
                    const welcomeMessage = chatMessagesContainer.querySelector('.message.assistant');
                    chatMessagesContainer.innerHTML = '';
                    if (welcomeMessage) {
                        chatMessagesContainer.appendChild(welcomeMessage);
                    }
                }
                localStorage.removeItem('vaultlogic_chat_history');
                showAlert('Chat history cleared.', 'success');
            }
        });
    }

})();
