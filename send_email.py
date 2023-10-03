from __future__ import print_function
import base64
import os.path
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import json

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']

creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())


service = build('gmail', 'v1', credentials=creds)


def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except Exception as error:
        print(error)









# Open the JSON file for reading
with open('emails.json', 'r') as json_file:
    # Read the JSON-like string from the file
    json_str = json_file.read()

# Parse the JSON-like string
parsed_data = json.loads(json_str)

# Access and print the values
for key, value in parsed_data.items():
    print(f"{key}: {value}")
    message = create_message('me', value, 'A possible reservation a spot', '''
                         
Hello,

Dear Madam/Sir,

I am writing you to clarify whether we can reserve a spot at your nursery for our son, who is 2 years old. 

We're a family, we have a National Visa D and will be relocating to Poland soon from Uzbekistan. We would like to enroll our son in one of your nursery groups. 

Your location is the nearest to the apartment we are going to stay so we think it would be comfortable for us and our son.

However, The Embassy of Poland has required an invitation from the nursery for our son, which will be a confirmation that he will be enrolled in one of the nursery groups.

Would we possibly reserve a spot at your nursery, if you have an available one, and get such invitation/confirmation for the Poland Embassy in Tashkent, from you that you can enroll him?
                             
We look forward to hearing from you.

                         
                         ''' )
    print(send_message(service=service, user_id='me', message=message))