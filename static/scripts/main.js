const send_button = document.querySelector('.send-button');
const chat_input = document.querySelector('textarea.chat-input');
const chat_messages = document.querySelector('.chat-messages');
const reset_button = document.querySelector('.reset-chat');

// Function for adding messages to the chat UI:
function add_message(text, sender) {
    let message_div = document.createElement('div');
    message_div.classList.add('message', `${sender}-message`);
    message_div.textContent = text;
    chat_messages.appendChild(message_div);
    chat_messages.scrollTop = chat_messages.scrollHeight;
    return message_div;
}

// Function for sending messages:
function send_message() {
    let message = chat_input.value.trim();
    if (message) {
        add_message(message, 'user')
        chat_input.value = '';

        // Add a typing indicator:
        let typing_indicator = add_message('...', 'assistant');
        typing_indicator.classList.add('typing');

        // Process the message with Flask:
        fetch('/send_message', {
            method : 'POST', headers : {'Content-Type' : 'application/json'},
            body : JSON.stringify({'content' : message})
        })
        .then(response => response.json())
        .then(data => {
            chat_messages.removeChild(typing_indicator);
            if (data['content'].trim() !== '') {
                add_message(data['content'], 'assistant');
            } else {
                add_message('Sorry - I couldn\'t process the request.  Could I trouble you to re-send your message?', 'assistant')
            }
        })
        .catch(error => {
            chat_messages.removeChild(typing_indicator);
            add_message('An error happened with the chatbot\'s backend!')
            console.error(`Error: ${error}`)
        })
    }
    
}
send_button.addEventListener('click', send_message);

// Also allow the user to send the message with the "Enter" key:
chat_input.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        send_message();
    }
})

// Reset the chat here...
function reset_chat() {
    if (confirm('Are you sure you want to reset the conversation?')) {
        fetch('/reset_conversation', {
            method : 'POST', 
            headers : {'Content-Type' : 'application/json'}
        })
        .then(response => response.json())
        .then(data => {
            if (data['status'] === 200) {
                chat_messages.innerHTML = '';
            }
        })
        .catch(error => console.error(`Error: ${error}`))
    }
}
reset_button.addEventListener('click', reset_chat);