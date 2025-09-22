import dotenv, os, uuid
from flask import Flask, render_template
from routes import conversation, misc
from google import genai
from google.genai import types
from utils import chat

dotenv.load_dotenv()
bot_prompt = chat.load_base_prompt(os.getenv('FERNET_TOKEN'))
chat_client = genai.Client(api_key = os.getenv('GEMINI_TOKEN'))
chat_client = chat_client.chats.create(model = 'gemini-2.5-flash',
                                       config = types.GenerateContentConfig(system_instruction = bot_prompt))

# Set the application-specific constants:
app = Flask(__name__)
app.bot_prompt = bot_prompt
app.chat_client = chat_client
app.secret_key = str(uuid.uuid4())

# Register the routes here plus define a starter route:
app.register_blueprint(conversation.conversation)
app.register_blueprint(misc.misc)
@app.route('/')
def main():
    return(render_template('main.html'))

if __name__ == '__main__':
    app.run()