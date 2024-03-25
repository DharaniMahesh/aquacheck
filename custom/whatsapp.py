import os
from twilio.rest import Client
from custom.credentials import token, account


def whatsapp_message(token, account, to_number, message, image_url=None):
    client = Client(account, token)
    from_number = 'whatsapp:+14155238886'
    to_number = 'whatsapp:+91' + to_number
    
    media_list = []
    if image_url:
        media_list.append(image_url)
    
    # Send the message with or without the image
    if media_list:
        message = client.messages.create(body=message, from_=from_number, to=to_number, media_url=media_list)
    else:
        message = client.messages.create(body=message, from_=from_number, to=to_number)
    
    print(message.sid)

