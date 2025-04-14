document.addEventListener('DOMContentLoaded', () => {
    const conversationList = document.querySelector('.conversation-list');
    const messageDisplay = document.getElementById('message-display');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const otherUserName = document.getElementById('other-user-name');
    const otherUserAvatar = document.getElementById('other-user-avatar');

    // Sample conversation data (replace with your backend data)
    const conversations = [
        { id: 1, name: 'John Doe', lastMessage: 'Hey, is this still available?', time: '10:30 AM', avatar: 'user1.jpg' },
        { id: 2, name: 'Jane Smith', lastMessage: 'Sure, when can you pick it up?', time: '11:00 AM', avatar: 'user2.jpg' },
    ];

    // Sample messages (replace with your backend data)
    let messages = [];

    // Function to render conversations
    function renderConversations() {
        conversationList.innerHTML = '';
        conversations.forEach(conversation => {
            const item = document.createElement('div');
            item.classList.add('conversation-item');
            item.innerHTML = `
                <img src="${conversation.avatar}" alt="${conversation.name}">
                <div class="conversation-details">
                    <span class="user-name">${conversation.name}</span>
                    <p class="last-message">${conversation.lastMessage}</p>
                    <span class="message-time">${conversation.time}</span>
                </div>
            `;
            item.addEventListener('click', () => loadConversation(conversation.id));
            conversationList.appendChild(item);
        });
    }

    // Function to load conversation messages
    function loadConversation(conversationId) {
        const selectedConversation = conversations.find(c => c.id === conversationId);
        otherUserName.textContent = selectedConversation.name;
        otherUserAvatar.src = selectedConversation.avatar;

        // Replace with your backend fetch for messages
        messages = [
            { sender: 'other', text: 'Hi there!', conversationId: conversationId },
            { sender: 'me', text: 'Hello!', conversationId: conversationId },
        ];

        renderMessages(conversationId);
    }

    // Function to render messages
    function renderMessages(conversationId) {
        messageDisplay.innerHTML = '';
        messages.filter(msg => msg.conversationId === conversationId).forEach(message => {
            const messageElement = document.createElement('div');
            messageElement.classList.add('message', message.sender === 'me' ? 'sent' : 'received');
            messageElement.textContent = message.text;
            messageDisplay.appendChild(messageElement);
        });
        messageDisplay.scrollTop = messageDisplay.scrollHeight; // Scroll to bottom
    }

    // Function to send a message
    function sendMessage() {
        const text = messageInput.value.trim();
        if (text) {
            messages.push({ sender: 'me', text: text, conversationId: conversations[0].id }); // Assuming first conversation
            renderMessages(conversations[0].id); // Assuming first conversation
            messageInput.value = '';

            // TODO: Send message to backend
        }
    }

    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    renderConversations();
    if (conversations.length > 0){
        loadConversation(conversations[0].id);
    }
});
