import tkinter as tk
from tkinter import messagebox
from db_connection import get_connection

def open_doctor_window(root):
    window = tk.Toplevel(root)
    window.title("🩺 Add Doctor")
    window.geometry("500x400")

    labels = [
        "First Name", "Last Name", "Specialization", "Phone Number"
    ]
    entries = {}

    for idx, label in enumerate(labels):
        tk.Label(window, text=label).grid(row=idx, column=0, padx=10, pady=5, sticky="e")
        entry = tk.Entry(window, width=30)
        entry.grid(row=idx, column=1, padx=10, pady=5)
        entries[label] = entry

    def register_doctor():
        data = {label: entries[label].get().strip() for label in labels}

        # Validate that First Name and Last Name are provided
        if not data["First Name"] or not data["Last Name"]:
            messagebox.showwarning("Missing Info", "First and Last Name are required.")
            window.lift() # Bring the window to the front
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO Doctors (
                    First_Name, Last_Name, Specialization, Phone_Number)
                VALUES (?, ?, ?, ?)
            """, (
                data["First Name"], data["Last Name"],
                data["Specialization"], data["Phone Number"]
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success ✅", f"Doctor {data['First Name']} {data['Last Name']} added successfully!")
            # Keep the window open, do not destroy yet
            # After adding a doctor, you can choose whether to reset fields or leave them as is.
            # For now, keeping the window open
            # window.destroy() # This is not called yet

        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def cancel():
        # Confirm cancel action
        if messagebox.askyesno("Confirm Cancel", "Are you sure you want to cancel?"):
            window.destroy()  # Close the window and return to the main menu

    # Add Doctor Button
    tk.Button(window, text="Add Doctor ✅", command=register_doctor, bg="lightblue", width=20).grid(row=len(labels), columnspan=2, pady=10)

    # Cancel Button (returns to main menu)
    tk.Button(window, text="Cancel ❌", command=cancel, bg="lightcoral", width=20).grid(row=len(labels) + 1, columnspan=2, pady=10)
