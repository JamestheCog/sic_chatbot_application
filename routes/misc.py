from flask import Blueprint, jsonify

misc = Blueprint('misc', __name__)

@misc.route('/ping', methods = ['GET'])
def ping():
    '''
    A simple route to wake the application up.  It'll be used by a Cronjob.
    '''
    return(jsonify({'status' : 200, 'message' : 'the application has been woken up!'}), 200)