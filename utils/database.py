'''
Module to contain helper functions and constants pertaining to she 
'''
import sqlitecloud, dotenv, os
from datetime import datetime

def store_message(message, role, id, db_connector = os.getenv('SQLITE_CONNECTOR')):
    '''
    Given a user message, a role (for the message), and the chat ID for 
    the chat session, store it in the remote database. 
    '''
    dotenv.load_dotenv()
    conn = sqlitecloud.connect(db_connector)
    cursor = conn.cursor() ; time = datetime.now()
    current_time = f'{time.day}/{time.month}/{time.year} {time.hour}:{time.minute}:{time.second}'
    cursor.execute('INSERT INTO patient_conversations VALUES (?, ?, ?, ?);', (id, current_time, role, message))
    conn.close()