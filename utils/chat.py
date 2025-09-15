'''
A module to contain helper functions for responding to user inputs.
'''

import os, requests, dotenv
from cryptography import fernet

# Dependencies for Google
from google import genai
from google.genai import types

def respond(user_message_history, base_prompt):
    '''
    NOTE (Thursday, August 28th, 2025): this function is NOT currently being used.
    '''
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
        print(message)
        message = {'content' : 'An error happened with the bot on the backend!'}
    else:
        message = message['choices'][0]['message']
    return(message)

def respond_with_gemini(message, base_prompt):
    '''
    Does the same thing as the respond() function, but uses Gemini instead (since Gemini has a pretty generous
    limit for free-tier users like us)

    NOTE (Thursday, 28th August) --> this function is not being used in the time being!
    '''
    dotenv.load_dotenv()
    chat_client, num_attempts = genai.Client(api_key = os.getenv('GEMINI_TOKEN')), 1
    while num_attempts <= os.getenv('TIMEOUT_RESPONSES'):
        chat = chat_client.chats.create(model = 'gemini-2.5-flash', 
                                        config = types.GenerateContentConfig(system_instruction = base_prompt))
        response = chat.send_message(message)
        if 'error' in response:
            print('Trying again to generate response...') ; num_attempts += 1
        else:
            break
    return(response.text)

def load_base_prompt(fernet_key):
    '''
    Load in the base prompt that Gemini depends on to function as the bot:
    '''
    decryptor = fernet.Fernet(rf'{fernet_key}')
    with open('./prompts/sic_bot_prompt.txt', 'rb') as prompt:
        decrypted = decryptor.decrypt(prompt.read()).decode('utf-8')
    return(decrypted)

    