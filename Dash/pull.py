import os
import sqlite3
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import time
from pushbullet import Pushbullet
API_KEY = "o.9QimAOJozQVEwyRHUhT64O8o2svKiHob"
pb = Pushbullet(API_KEY)


def create_db(db_name='emails.db'):
    conn = sqlite3.connect(db_name)  # Connect to the SQLite database (or create it)
    cursor = conn.cursor()

    # create a table to store email data
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS email_data (
        id TEXT PRIMARY KEY,
        amount TEXT,
        status TEXT,
        ref_id TEXT,
        visited BOOLEAN DEFAULT 0
    )
    ''')

    conn.commit()
    conn.close()
def save_email_data(email_id, amount, status, ref_id, db_name='emails.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
  
    try:
        # Use INSERT OR REPLACE to avoid conflicts with primary key
        cursor.execute('''
        INSERT INTO email_data (id, amount, status, ref_id, visited)
        VALUES (?, ?, ?, ?, ?)
        ''', (email_id, amount, status, ref_id, 0))

        conn.commit()  # Commit the transaction
        conn.close()
        return 0
    except Exception as e:

        conn.close()
        return 1
    
    

# Define the scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    """Authenticate with Gmail API and return the service object."""
    
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build the Gmail API service
    service = build('gmail', 'v1', credentials=creds)
    return service

def fetch_emails_from_hdfc(service):
    """Fetch emails from 'alerts@hdfcbank.net' and print their ID and snippet content."""
    
    try:
        # List messages from the sender 'alerts@hdfcbank.net'
        query = "from:alerts@hdfcbank.net"
        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])
        
        if not messages:
            print('No messages from alerts@hdfcbank.net.')
        else:
            print(f"Found {len(messages) } message(s) from alerts@hdfcbank.net.")
            # Process each message
            for message in messages:
                email_id = message['id']
                # Get the message details
                msg = service.users().messages().get(userId='me', id=email_id).execute()
                msg_data = msg['payload']['headers']
                
                # Extract subject and snippet
                subject = next(header['value'] for header in msg_data if header['name'] == 'Subject')
                val = msg.get('snippet', '')
              
                val = val.split("If")[0]
                val = val.split("Thank")[0]
                val = val.split()
                # Print email ID and snippet (body)
                if len(val) < 6:
                    print(f"Skipping email with ID {email['ID']} due to insufficient data.")
                    continue
        
                amount = val[2][3:]  # Extract amount
                status = val[5]  # Extract status
                ref_id = val[-1][:-1]  # Extract reference ID

        # Save extracted data into the SQLite database
                create_db(db_name='../emails.db')
                if save_email_data(email_id, amount, status, ref_id, db_name='../emails.db'):
                    print("Skipping this data as it is already stored")
                    break
                else:
                    push = pb.push_note('Alpha Diary',f"An amount of {amount} is {status} from your bank account")
                    print("New data successfully saved")
    except HttpError as error:
        print(f"HUH I QUIT")

def main():
    """Main function to authenticate and fetch emails."""
    # Authenticate and create Gmail API service
    service = authenticate_gmail()
    
    while True:  # Run continuously
        # Fetch emails from 'alerts@hdfcbank.net'
        fetch_emails_from_hdfc(service)
        
        # Sleep for a specified time before checking again (e.g., 60 seconds)
        print("Waiting for the next check...")
        time.sleep(30)

# Only run the script when executed as a standalone program
if __name__ == '__main__':
    main()
