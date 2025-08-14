import dotenv, os
from flask import Flask, render_template
from utils import logger
from routes.conversation import conversation
from cryptography import fernet

dotenv.load_dotenv()
app = Flask(__name__)
app.conversation_logger = logger.Logger()
with open('./prompts/sic_bot_prompt.txt', 'rb') as prompt:
    decryptor = fernet.Fernet(rf"{os.getenv('FERNET_TOKEN')}")
    bot_prompt = decryptor.decrypt(prompt.read()).decode('utf-8')
app.bot_prompt = bot_prompt

# Register the routes here plus define a starter route:
app.register_blueprint(conversation)
@app.route('/')
def main():
    return(render_template('main.html'))

if __name__ == '__main__':
    app.run()