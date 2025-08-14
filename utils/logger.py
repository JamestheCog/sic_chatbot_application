'''
A module to contain utilities related to the logging of messages (so that it can be sent to the SQLitecloud database).
'''

import random, string

'''
A class to log messages from the user AND the Chatbot.
'''
class Logger():
    def __init__(self):
        self.message_history = []
        self.id = self._generate_id()
    
    def log_message(self, message: str, role: str):
        self.message_history.append({'role' : role, 'content' : message})
    
    def reset(self):
        self.message_history = []
        self.id = self._generate_id()
    
    @staticmethod
    def _generate_id():
        letters = list(string.ascii_lowercase) + list(string.ascii_uppercase)
        numbers = list(range(10)) 
        id = random.sample(letters, 5) + random.sample(numbers, 5)
        random.shuffle(id)
        return(''.join([str(i) for i in id]))

