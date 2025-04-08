# view_patients.py

import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import get_connection

def view_patients_window():
    # Create a new top-level window
    window = tk.Toplevel()
    window.title("👀 View Patients")
    window.geometry("800x400")

    # Create a Treeview widget to display patient data
    tree = ttk.Treeview(window, columns=("ID", "First Name", "Last Name", "DOB", "Gender", "Phone", "Email"), show="headings")

    # Define the column headings
    tree.heading("ID", text="ID")
    tree.heading("First Name", text="First Name")
    tree.heading("Last Name", text="Last Name")
    tree.heading("DOB", text="DOB")
    tree.heading("Gender", text="Gender")
    tree.heading("Phone", text="Phone")
    tree.heading("Email", text="Email")

    # Set column width
    tree.column("ID", width=50, anchor="center")
    tree.column("First Name", width=150, anchor="center")
    tree.column("Last Name", width=150, anchor="center")
    tree.column("DOB", width=100, anchor="center")
    tree.column("Gender", width=100, anchor="center")
    tree.column("Phone", width=150, anchor="center")
    tree.column("Email", width=200, anchor="center")

    # Place the Treeview in the window
    tree.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

    try:
        # Connect to the database and fetch all patient records
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Patients")
        rows = cursor.fetchall()

        # Insert the patient records into the Treeview widget
        for row in rows:
            tree.insert("", "end", values=row)

        conn.close()

    except Exception as e:
        # Handle any database errors
        messagebox.showerror("Error", f"Failed to retrieve patient records: {e}")
        print(f"Error: {e}")
    
    # Add a button to close the window
    tk.Button(window, text="Close", command=window.destroy, bg="lightcoral", width=20).pack(pady=10)
