document.getElementById('send-message').addEventListener('click', async () => {
    const message = document.getElementById('user-message').value;
    if (message.trim() === '') return;

    const chatMessages = document.getElementById('chat-messages');

    // 显示用户消息
    const userMessageDiv = document.createElement('div');
    userMessageDiv.className = 'chat-message user';
    userMessageDiv.innerHTML = `
        <div>${message}</div>
        <img src="../static/images/user-icon.svg" alt="User">
    `;
    chatMessages.appendChild(userMessageDiv);

    // 清空输入框
    document.getElementById('user-message').value = '';

    // 向服务器发送消息
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({message})
        });

        const data = await response.json();

        // 调试时记录服务器响应
        console.log(data);

        // 显示AI的响应
        const aiMessageDiv = document.createElement('div');
        aiMessageDiv.className = 'chat-message ai';
        aiMessageDiv.innerHTML = `
            <img src="../static/images/ai-icon.png" alt="AI">
            <div>${data.reply}</div>
        `;
        chatMessages.appendChild(aiMessageDiv);
    } catch (error) {
        console.error('Error:', error);
    }
});

document.getElementById('new-chat').addEventListener('click', () => {
    // 清空聊天消息
    document.getElementById('chat-messages').innerHTML = '';
});

async function loadChatHistory() {
            try {
                const response = await fetch(`/get_chat_history?username=${user_info}`);
                const data = await response.json();
                const chatHistory = document.getElementById('chat-history');

                if (data.messages) {
                    chatHistory.innerHTML = ''; // 清空之前的历史记录
                    data.messages.forEach((message, index) => {
                        if (message.sender === 'user') {
                            const date = new Date(message.timestamp);
                            const formattedDate = date.toISOString().split('T')[0];

                            const messageLi = document.createElement('li');
                            messageLi.className = 'list-group-item d-flex justify-content-between align-items-center';
                            messageLi.innerHTML = `
                                <div>
                                    <span class="timestamp">${formattedDate}</span>
                                    <span class="message">${message.message}</span>
                                </div>
                                <div class="dropdown">
                                    <button class="btn btn-link dropdown-toggle" type="button" id="dropdownMenuButton${index}" data-bs-toggle="dropdown" aria-expanded="false">
                                        ...
                                    </button>
                                    <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton${index}">
                                        <li><a class="dropdown-item" href="#" onclick="viewResponse(${index})">查看</a></li>
                                        <li><a class="dropdown-item" href="#" onclick="deleteMessage(${index})">删除</a></li>
                                    </ul>
                                </div>
                            `;
                            chatHistory.appendChild(messageLi);
                        }
                    });
                } else {
                    console.error('No messages found:', data);
                }
            } catch (error) {
                console.error('Error fetching chat history:', error);
            }
        }

        function viewResponse(index) {
            fetch(`/get_chat_history?username=${user_info}`)
                .then(response => response.json())
                .then(data => {
                    if (data.messages) {
                        const userMessage = data.messages[index * 2];
                        const aiReply = data.messages[index * 2 + 1];
                        alert(`AI的回答: ${aiReply.message}`);
                    } else {
                        console.error('No messages found:', data);
                    }
                })
                .catch(error => {
                    console.error('Error fetching chat history:', error);
                });
        }

        function deleteMessage(index) {
            fetch(`/delete_message`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({username: user_info, index: index})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    loadChatHistory(); // 重新加载聊天历史记录
                } else {
                    console.error('Failed to delete message:', data);
                }
            })
            .catch(error => {
                console.error('Error deleting message:', error);
            });
        }

        // 页面加载时加载聊天历史记录
        window.addEventListener('load', loadChatHistory);
