import os
import base64
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the scope for Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Specify sender's email address
SENDER_EMAIL = 'alerts@hdfcbank.net'

def authenticate_gmail():
    """Authenticate and build Gmail API service."""
    creds = None
    # Load credentials from file
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no valid credentials, authenticate using the credentials file
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
    return service

def get_emails_from_sender(service, sender_email):
    """Retrieve all emails from the specified sender."""
    try:
        # Query to get emails from a specific sender
        query = f'from:{sender_email}'
        # Call the Gmail API
        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])

        emails = []

        # Process each message
        for message in messages:
      
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            msg_data = msg['payload']['headers']

            # Extract subject and snippet
            subject = next(header['value'] for header in msg_data if header['name'] == 'Subject')
            snippet = msg.get('snippet', '')

            emails.append({'subject': subject, 'snippet': snippet,"ID":message["id"]})
        return emails

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def main():
    # Authenticate and get the Gmail API service
    service = authenticate_gmail()

    # Get all emails from the specified sender
    emails = get_emails_from_sender(service, SENDER_EMAIL)

    # Display email subjects and snippets
   
    for email in emails:
        val = email['snippet']
        val = val.split("If")[0]
        val = val.split("Thank")[0]
        val = val.split()
        amount,status,ref_id = val[2][3:],val[5],val[-1][:-1]
     
        print(email["ID"],amount,status,ref_id)
   
if __name__ == '__main__':
    main()
