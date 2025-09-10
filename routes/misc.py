from flask import Blueprint, jsonify, request
from dotenv import load_dotenv
import os, sqlitecloud

load_dotenv()
misc = Blueprint('misc', __name__)

@misc.route('/ping', methods = ['GET'])
def ping():
    '''
    A simple route to wake the application up.  It'll be used by a Cronjob.
    '''
    return(jsonify({'status' : 200, 'message' : 'the application has been woken up!'}), 200)

@misc.route('/wake_database', methods = ['POST'])
def wake_database():
    '''
    Given a password of our own choosing and a POST request, wake the database
    up if and only if the password sent over matches the one provided in the 
    application's .env file.
    '''
    data = request.json 
    if data.get('authorization') is None:
        return(jsonify({'message' : "Missing 'authorization' parameter"}, 400))
    if data['authorization'].get('password') != os.getenv('DB_PASSWORD'):
        return(jsonify({'message' : "Incorrect password provided"}, 400))
    
    conn = sqlitecloud.connect(os.getenv('SQLITE_CONNECTOR'))
    cursor, dummy_values = conn.cursor(), tuple(['?'] * 4)
    cursor.execute(f"INSERT INTO {os.getenv('TABLE_NAME')} VALUES ({', '.join(dummy_values)});", 
                   ['TEST'] * len(dummy_values))
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {os.getenv('TABLE_NAME')} WHERE id = 'TEST';")
    return(jsonify({'message' : 'Database service woken up!'}), 200)