import sqlite3
from . import my_mail  # Ensure the `mail` module is in the same package

# Function to create an SQLite database and table
def create_db(db_name='emails.db'):
    conn = sqlite3.connect(db_name)  # Connect to the SQLite database (or create it)
    cursor = conn.cursor()

    # Create a table to store email data
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

# Function to save data in the SQLite database
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
    except Exception as e:
        print(f"Error occurred: {e}")
        conn.close()
        return 1
    
    conn.close()
    return 0

# Function to process emails and save data
def process_emails(sender_email, db_name='emails.db'):
    # Authenticate and get emails
    service = my_mail.authenticate_gmail()
    emails = my_mail.get_emails_from_sender(service, sender_email)

    # Create database and table if not exists
    create_db(db_name)

    # Loop through emails and save data in the database
    for email in emails:
        val = email['snippet']
        val = val.split("If")[0]
        val = val.split("Thank")[0]
        val = val.split()
        
        # Check if the list has enough elements before extracting data
        if len(val) < 6:
            print(f"Skipping email with ID {email['ID']} due to insufficient data.")
            continue
        
        amount = val[2][3:]  # Extract amount
        status = val[5]  # Extract status
        ref_id = val[-1][:-1]  # Extract reference ID

        # Save extracted data into the SQLite database
        if save_email_data(email["ID"], amount, status, ref_id, db_name):
            break

    print("Data successfully saved to the database.")

# Main execution block (optional, for standalone use)
if __name__ == "__main__":
    sender_email = "alerts@hdfcbank.net"  # Replace with the email address you want to process
    process_emails(sender_email)
