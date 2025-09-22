import dotenv, os, uuid
from flask import Flask, render_template
from routes import conversation, misc
from utils import chat

dotenv.load_dotenv()
bot_prompt = chat.load_base_prompt(os.getenv('FERNET_TOKEN'))

# Set the application-specific constants:
app = Flask(__name__)
app.bot_prompt = bot_prompt
app.secret_key = str(uuid.uuid4())

# Register the routes here plus define a starter route:
app.register_blueprint(conversation.conversation)
app.register_blueprint(misc.misc)
@app.route('/')
def main():
    return(render_template('main.html'))

if __name__ == '__main__':
    app.run()