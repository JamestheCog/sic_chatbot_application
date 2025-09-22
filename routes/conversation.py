'''
A module to contain helper functions related to the Chatbot's functionality.
'''

import dotenv, os, time, random, uuid
from utils import chat, database, logger
from flask import Blueprint, current_app, request, jsonify, session
from google import genai
from google.genai import types

# Initialize Google Gemini here:
from google import genai
from google.genai import types

dotenv.load_dotenv()
conversation = Blueprint('conversation', __name__, template_folder = 'templates')
items = {}

# ===
def initialize_items():
    if 'session_id' not in session:
        items['session_id'] = str(uuid.uuid4())
    if 'chat_assistant' not in session:
        chat_client = genai.Client(api_key = os.getenv('GEMINI_TOKEN'))
        items['chat_assistant'] = chat_client.chats.create(model = 'gemini-2.5-flash', 
                                                             config = types.GenerateContentConfig(system_instruction = current_app.bot_prompt))
    session_id = session.get('session_id')
    if session_id not in items:
        items[session_id] = logger.Logger()
    return(items[session_id], items['chat_assistant'])
# ===

# Define the routes here...
@conversation.route('/send_message', methods = ['POST'])
def send_message():
    '''
    Generate a response plus log the user's message.
    '''
    data, retry_times = request.json, 0
    user_logger, chat_client = initialize_items()
    if not isinstance(data, dict):
        return(jsonify({'error_message' : 'Invalid data sent', 'error_code' : 500,
                        'user_message' : 'ERROR: SOMETHING HAPPENED'}), 500)
    database.store_message(data['content'], 'user', user_logger.id)
    while retry_times < int(os.getenv('RETRY_RESPONSES')):
        response = chat_client.send_message(data['content'])
        if isinstance(response, dict):
            if response.get('error') is None:
                retry_times += 1
                print(f'Trying to re-fetch responses now (attempt {retry_times + 1})...')
                time.sleep(random.randint(4, 8))
        else:
            break
    database.store_message(response.text, 'assistant', user_logger.id)
    return(jsonify({'content' : response.text}), 200)

@conversation.route('/reset_conversation', methods = ['POST'])
def reset_conversation():
    '''
    Reset the conversation and by extension, the logger as part of the 
    current_app object's attributes.
    '''
    try:
        chat_client = genai.Client(api_key = os.getenv('GEMINI_TOKEN'))
        chat_client = chat_client.chats.create(model = 'gemini-2.5-flash',
                                            config = types.GenerateContentConfig(
                                                system_instruction = chat.load_base_prompt(os.getenv('FERNET_TOKEN'))))
        current_app.chat_client = chat_client
        session['logger'].reset()
        return(jsonify({'status' : 200}), 200)
    except Exception as e:
        print(f'An error happened: "{e}"')