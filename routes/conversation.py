'''
A module to contain helper functions related to the Chatbot's functionality.
'''

import dotenv, os
from utils import chat, database
from flask import Blueprint, current_app, request, jsonify

dotenv.load_dotenv()
conversation = Blueprint('conversation', __name__, template_folder = 'templates')

# Define the routes here...
@conversation.route('/send_message', methods = ['POST'])
def send_message():
    '''
    Generate a response plus log the user's message.
    '''
    data = request.json 
    if not isinstance(data, dict):
        return(jsonify({'error_message' : 'Invalid data sent', 'error_code' : 500,
                        'user_message' : 'ERROR: SOMETHING HAPPENED'}), 500)
    database.store_message(data['content'], 'user', current_app.conversation_logger.id)
    current_app.conversation_logger.log_message(data['content'], 'user')
    response = chat.respond(current_app.conversation_logger.message_history, current_app.bot_prompt)
    current_app.conversation_logger.log_message(response['content'], 'assistant')
    database.store_message(response['content'], 'assistant', current_app.conversation_logger.id)
    return(jsonify({'content' : response.get('content')}), 200)

@conversation.route('/reset_conversation', methods = ['POST'])
def reset_conversation():
    '''
    Reset the conversation and by extension, the logger as part of the 
    current_app object's attributes.
    '''
    current_app.conversation_logger.reset()
    return(jsonify({'status' : 200}), 200)
