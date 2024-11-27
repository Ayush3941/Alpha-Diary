import sqlite3
import os

# Get the base directory of the Django project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Adjust if needed to your project's root directory
DB_PATH = os.path.join(BASE_DIR, '../emails.db')  # Adjust relative path as needed

# Function to fetch unvisited records and mark them as visited
def process_unvisited_records():
    try:
        # Connect to the SQLite database using the corrected path
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Fetch all records where visited = 0
        cursor.execute('SELECT * FROM email_data WHERE visited = 0')
        unvisited_records = cursor.fetchall()

        if not unvisited_records:
            print("No unvisited records found.")
            return []

        # Print the unvisited records (for debugging)
        print("Unvisited Records:")
        for record in unvisited_records:
            print(record)


        return unvisited_records

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        # Close the database connection
        conn.close()
def mark_as_visited(record_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Update the record's visited status
        cursor.execute('UPDATE email_data SET visited = 1 WHERE id = ?', (record_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error marking record as visited: {e}")
        return False
    finally:
        conn.close()

# Function to delete a record
def delete_record(record_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Delete the record from the database
        cursor.execute('DELETE FROM email_data WHERE id = ?', (record_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting record: {e}")
        return False
    finally:
        conn.close()

# Test function to ensure it works (useful for standalone testing)
if __name__ == "__main__":
    records = process_unvisited_records()
    print("Returned Records:", records)
