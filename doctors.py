import tkinter as tk
from tkinter import messagebox
from db_connection import get_connection

def open_doctor_window():
    window = tk.Toplevel()
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

        if not data["First Name"] or not data["Last Name"]:
            messagebox.showwarning("Missing Info", "First and Last Name are required.")
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
            window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")

    tk.Button(window, text="Add Doctor ✅", command=register_doctor, bg="lightblue", width=20).grid(row=len(labels), columnspan=2, pady=20)
