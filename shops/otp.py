from __future__ import print_function

import africastalking 

class SMS:
    def __init__(self):
        self.username = "skakey"
        self.api_key = "71b5fbfdb6fdf9e96551e34e3f4807ac115b112894dbc8e567a2cd03178226dd"
        
        africastalking.initialize(self.username, self.api_key)
        
        self.sms = africastalking.SMS 
        
    def send(self, message, receiver):
        recipients = receiver
        message = message
        sender="AFRICASTKNG"
        
        try:
            response = self.sms.send(message, recipients)
            print (response)
        except Exception as e:
            print('Encountered an error while sending: %s' % str(e))
            
if __name__ == '__main__':
    SMS().send()