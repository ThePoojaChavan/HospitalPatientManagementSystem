import tkinter as tk
from tkinter import messagebox
import db_connection

def open_availability_menu():
    """Open a window with options to Add, Delete, or View doctor availability."""
    availability_window = tk.Tk()
    availability_window.title("Doctor Availability Menu")
    availability_window.geometry("300x200")

    # Add button for adding availability
    add_button = tk.Button(availability_window, text="Add Availability", command=open_add_availability_window)
    add_button.pack(padx=10, pady=10)

    # Add button for viewing availability records
    view_button = tk.Button(availability_window, text="View Availability", command=open_view_availability_window)
    view_button.pack(padx=10, pady=10)

    # Add button for deleting availability
    delete_button = tk.Button(availability_window, text="Delete Availability", command=open_delete_availability_window)
    delete_button.pack(padx=10, pady=10)

    availability_window.mainloop()

def open_add_availability_window():
    """Open a window to add availability."""
    add_window = tk.Tk()
    add_window.title("Add Doctor Availability")
    add_window.geometry("300x200")

    # Add necessary input fields for doctor availability
    doctor_id_label = tk.Label(add_window, text="Doctor ID:")
    doctor_id_label.pack(pady=5)
    doctor_id_entry = tk.Entry(add_window)
    doctor_id_entry.pack(pady=5)

    date_label = tk.Label(add_window, text="Date:")
    date_label.pack(pady=5)
    date_entry = tk.Entry(add_window)
    date_entry.pack(pady=5)

    # Add more fields as needed...

    def save_availability():
        """Save the availability details to the database."""
        doctor_id = doctor_id_entry.get()
        date = date_entry.get()

        query = "INSERT INTO doctor_availability (doctor_id, date) VALUES (?, ?)"
        db_connection.execute_query(query, (doctor_id, date))
        messagebox.showinfo("Success", "Availability added successfully!")
        add_window.destroy()

    save_button = tk.Button(add_window, text="Save", command=save_availability)
    save_button.pack(pady=10)

    add_window.mainloop()

def open_view_availability_window():
    """Open a window to view doctor availability records."""
    view_window = tk.Tk()
    view_window.title("View Availability")
    view_window.geometry("400x300")

    query = "SELECT * FROM doctor_availability"
    availability_list = db_connection.execute_select_query(query)

    for availability in availability_list:
        availability_info = f"ID: {availability[0]}, Doctor ID: {availability[1]}, Date: {availability[2]}"
        availability_label = tk.Label(view_window, text=availability_info)
        availability_label.pack()

    view_window.mainloop()

def open_delete_availability_window():
    """Open a window to delete doctor availability."""
    delete_window = tk.Tk()
    delete_window.title("Delete Doctor Availability")
    delete_window.geometry("300x200")

    id_label = tk.Label(delete_window, text="Enter Availability ID to Delete:")
    id_label.pack(pady=10)
    id_entry = tk.Entry(delete_window)
    id_entry.pack(pady=5)

    def delete_availability():
        """Delete availability from the database."""
        availability_id = id_entry.get()

        # Check if the ID exists before attempting to delete
        query = "SELECT * FROM doctor_availability WHERE id = ?"
        result = db_connection.execute_select_query(query, (availability_id,))

        if result:
            delete_query = "DELETE FROM doctor_availability WHERE id = ?"
            db_connection.execute_query(delete_query, (availability_id,))
            messagebox.showinfo("Success", "Availability deleted successfully!")
            delete_window.destroy()
        else:
            messagebox.showerror("Error", "Availability ID not found!")

    delete_button = tk.Button(delete_window, text="Delete", command=delete_availability)
    delete_button.pack(pady=10)

    delete_window.mainloop()