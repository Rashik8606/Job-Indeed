let currentReceiverId = null;
const currentUserId = {{ request.user.id }};

// Load users
function loadUsers() {
    fetch(`/api/inbox/${currentUserId}/`)
        .then(response => response.json())
        .then(data => {
            const contactList = document.getElementById('contact-list');
            contactList.innerHTML = '';

            const uniqueUsers = new Set();

            data.forEach(message => {
                const otherUser = message.sender === currentUserId ? message.receiver : message.sender;
                const otherUsername = message.sender === currentUserId ? message.receiver_username : message.sender_username;

                if (!uniqueUsers.has(otherUser)) {
                    uniqueUsers.add(otherUser);

                    const contactDiv = document.createElement('div');
                    contactDiv.className = 'contact-item';
                    contactDiv.onclick = () => selectUser(otherUser, otherUsername);

                    contactDiv.innerHTML = `
                        <img src="/static/default-avatar.png" class="user-avatar" alt="${otherUsername}">
                        <div class="user-details">
                            <h4>${otherUsername}</h4>
                            <p>${message.message.substring(0, 30)}${message.message.length > 30 ? '...' : ''}</p>
                        </div>
                    `;

                    contactList.appendChild(contactDiv);
                }
            });
        });
}

// Select user to chat with
function selectUser(userId, username) {
    currentReceiverId = userId;

    // Update UI
    document.getElementById('selected-user-name').textContent = username;
    document.getElementById('user-status').textContent = 'Online';
    document.getElementById('message-input').disabled = false;
    document.getElementById('send-button').disabled = false;

    // Load messages
    loadMessages();

    // Update active state
    document.querySelectorAll('.contact-item').forEach(item => {
        item.classList.remove('active');
        if (item.querySelector('h4').textContent === username) {
            item.classList.add('active');
        }
    });
}

// Load messages
function loadMessages() {
    if (!currentReceiverId) return;

    fetch(`/api/messages/${currentUserId}/${currentReceiverId}/`)
        .then(response => response.json())
        .then(data => {
            const messagesContainer = document.getElementById('messages-container');
            messagesContainer.innerHTML = '';

            data.forEach(message => {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${message.sender === currentUserId ? 'sent' : 'received'}`;
                messageDiv.innerHTML = `
                    ${message.message}
                    <div class="message-time">
                        ${new Date(message.date).toLocaleTimeString()}
                    </div>
                `;
                messagesContainer.appendChild(messageDiv);
            });

            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        });
}

// Send message
document.getElementById('message-form').onsubmit = function(e) {
    e.preventDefault();

    if (!currentReceiverId) return;

    const messageInput = document.getElementById('message-input');
    const message = messageInput.value.trim();

    if (message) {
        fetch('/api/messages/send/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({
                receiver: currentReceiverId,
                message: message
            })
        })
        .then(response => response.json())
        .then(data => {
            messageInput.value = '';
            loadMessages();
            loadUsers(); // Refresh user list to update last message
        });
    }
};

// Search users
document.getElementById('search-input').oninput = function(e) {
    const searchTerm = e.target.value.trim();
    if (searchTerm) {
        fetch(`/searchuser/${searchTerm}/`)
            .then(response => response.json())
            .then(data => {
                const contactList = document.getElementById('contact-list');
                contactList.innerHTML = '';

                data.forEach(user => {
                    const contactDiv = document.createElement('div');
                    contactDiv.className = 'contact-item';
                    contactDiv.onclick = () => selectUser(user.user, user.username);

                    contactDiv.innerHTML = `
                        <img src="${user.profile_picture || '/static/default-avatar.png'}" class="user-avatar" alt="${user.username}">
                        <div class="user-details">
                            <h4>${user.username}</h4>
                            <p>${user.bio || 'No bio available'}</p>
                        </div>
                    `;

                    contactList.appendChild(contactDiv);
                });
            });
    } else {
        loadUsers();
    }
};

// Initial load
loadUsers();

// Refresh messages periodically
setInterval(() => {
    if (currentReceiverId) {
        loadMessages();
    }
}, 5000);