import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('attendance.db')  # Update the path if your database is in a different location

# Create a cursor object
cursor = conn.cursor()

# Function to delete a user by username
def delete_user(username):
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    print(f"User '{username}' deleted successfully.")

# Function to update a user's password by username
def update_user_password(username, new_password):
    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
    conn.commit()
    print(f"Password for user '{username}' updated successfully.")

# Get user input for the operation
operation = input("Enter the operation (delete/update): ").strip().lower()
username = input("Enter the username: ").strip()

if operation == 'delete':
    delete_user(username)
elif operation == 'update':
    new_password = input("Enter the new password: ").strip()
    update_user_password(username, new_password)
else:
    print("Invalid operation. Please enter 'delete' or 'update'.")

# Close the connection
conn.close()
