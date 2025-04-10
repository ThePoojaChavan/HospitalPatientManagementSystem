# view_patients.py

import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import get_connection

def view_patients_window():
    # Create a new top-level window
    window = tk.Toplevel()
    window.title("👀 View Patients")
    window.geometry("800x400")

    window.state('zoomed')  # Maximize the window

    # Create a label with a larger font size
    label = tk.Label(window, text="View Patient Information", font=("Arial", 24))  # Font size 24
    label.pack(pady=30)  # Add some padding around the label

    # Create a Treeview widget to display patient data
    columns = ("ID", "First Name", "Last Name", "DOB", "Gender", "Street", "City", "State", "ZIP", "Phone", "Email", "Emergency Phone")
    tree = ttk.Treeview(window, columns=columns, show="headings")

    # Define the column headings
    tree.heading("ID", text="ID")
    tree.heading("First Name", text="First Name")
    tree.heading("Last Name", text="Last Name")
    tree.heading("DOB", text="DOB")
    tree.heading("Gender", text="Gender")
    tree.heading("Street", text="Street")
    tree.heading("City", text="City")
    tree.heading("State", text="State")
    tree.heading("ZIP", text="ZIP")
    tree.heading("Phone", text="Phone")
    tree.heading("Email", text="Email")
    tree.heading("Emergency Phone", text="Emergency Phone")

    # Set column width
    tree.column("ID", width=40, anchor="center")
    tree.column("First Name", width=80, anchor="center")
    tree.column("Last Name", width=80, anchor="center")
    tree.column("DOB", width=80, anchor="center")
    tree.column("Gender", width=40, anchor="center")
    tree.column("Street", width=120, anchor="center")
    tree.column("City", width=40, anchor="center")
    tree.column("State", width=40, anchor="center")
    tree.column("ZIP", width=40, anchor="center")
    tree.column("Phone", width=100, anchor="center")
    tree.column("Email", width=200, anchor="center")
    tree.column("Emergency Phone", width=100, anchor="center")

    # Apply a custom font to the Treeview text (for better readability)
    tree.tag_configure("big_font", font=("Arial", 16))  # Change the font to 16
    
    # Place the Treeview in the window
    tree.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

    try:
        # Connect to the database and fetch all patient records
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Patient_ID, First_Name, Last_Name, DOB, Gender, Street, City, State, ZIP_Code, Phone_Number, Email, Emergency_Phone FROM Patients")
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
    tk.Button(window, text="Close", command=window.destroy, bg="red", fg="white", width=20).pack(pady=10)
