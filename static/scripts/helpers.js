// Function for resetting the chat application MANUALLY.  The user should be the one 
// saying that they want the application to be reset.
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

        setTimeout(() => {send_welcome_message()});
    }
}

// Ditto, but for automatic deletion:
const auto_reset_conversation = () => {
    fetch('/reset_conversation', {
        method : 'POST', headers : {'Content-Type' : 'application/json'}
    })
    .then(response => response.json())
    .then(data => {
        if (data['status'] === 200) {
            chat_messages.innerHTML = '';
        }
    })
    .catch(error => console.error(`Error: ${error}`))
}