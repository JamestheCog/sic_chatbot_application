'''
A module to contain helper functions for responding to user inputs.
'''

import os, requests, dotenv

def respond(user_message_history, base_prompt):
    dotenv.load_dotenv()
    API_URL = 'https://openrouter.ai/api/v1/chat/completions'
    HEADER = {'Authorization' : f"Bearer {os.getenv('OPENROUTER_TOKEN')}", 'Content-Type' : 'application/json'}
    payload = {
        'messages': [{'role' : 'system', 'content' : base_prompt}] + user_message_history,
        'model' : 'meta-llama/llama-3.3-70b-instruct:free'
    }
    response = requests.post(API_URL, headers = HEADER, json = payload)
    message = response.json()
    if 'error' in message:
        message = {'content' : 'An error happened with the bot on the backend!'}
    else:
        message = message['choices'][0]['message']
    return(message)
