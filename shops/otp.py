from __future__ import print_function
import os
import africastalking 

class SMS:
    def __init__(self):
        self.username =  os.environ.get('AFRICASTALKING_USERNAME')
        self.api_key = os.environ.get('AFRCASTALKING_MYAPIKEY')
        
        africastalking.initialize(self.username, self.api_key)
        
        self.sms = africastalking.SMS 
        
    def send(self, message, receiver):
        recipients = receiver
        message = message
        sender="AFRICASTKNG"
        
        try:
            response = self.sms.send(message, recipients)
            # print (response)
        except Exception as e:
            return e
            
if __name__ == '__main__':
    SMS().send()