import sqlite3
from tkinter import messagebox

#Function to connect to the SQLite database
def get_connection():
    """Create a connection to the SQLite database."""
    try:
        # Connect to the SQLite database (or create it if it doesn't exist)
        connection = sqlite3.connect("HospitalPatientManagementSystem.db")
        return connection
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database: {e}")
        return None
   

