import tkinter as tk
from tkinter import messagebox
import logging
from db_connection import get_connection
import datetime

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def open_patient_window():
    window = tk.Toplevel()
    window.title("🧍 Register Patient")
    window.geometry("800x650")

    # Labels & Entries
    labels = [
        "First Name", "Last Name", "DOB (YYYY-MM-DD)", "Gender (Male/Female)",
        "Street", "City", "State", "Zip Code", "Phone Number",
        "Email", "Emergency Phone"
    ]
    entries = {}

    for idx, label in enumerate(labels):
        tk.Label(window, text=label).grid(row=idx, column=0, padx=10, pady=5, sticky="e")
        if label != "Gender (Male/Female)":  # Skip gender entry field
            entry = tk.Entry(window, width=30)
            entry.grid(row=idx, column=1, pady=5, padx=10)
            entries[label] = entry

    # Gender selection using radio buttons
    gender_var = tk.StringVar()
    gender_var.set("Male")  # Default selection

    gender_frame = tk.Frame(window)
    gender_frame.grid(row=3, column=1, pady=5, padx=10, sticky="w")  # Proper grid position for gender

    male_rb = tk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="Male")
    male_rb.grid(row=0, column=0, padx=5)
    female_rb = tk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="Female")
    female_rb.grid(row=0, column=1, padx=5)

    # Ensure no entry widget for gender
    # gender_entry = gender_var  # No entry widget for gender

    def register_patient():
        # Get all data from entries
        data = {label: entries[label].get().strip() for label in labels if label != "Gender (Male/Female)"}
        data["Gender (Male/Female)"] = gender_var.get() # Get gender from radio button

        if not data["First Name"] or not data["Last Name"] or not data["DOB (YYYY-MM-DD)"] or not data["Gender (Male/Female)"]:
            messagebox.showwarning("Missing Info", "Please fill in required fields: First Name, Last Name, DOB, and Gender.")
            window.lift()  # Bring the registration window to the front
            return

        # Validate DOB format and ensure it's not in the future
        try:
            dob = datetime.datetime.strptime(data["DOB (YYYY-MM-DD)"], "%Y-%m-%d")
            if dob > datetime.datetime.now():
                messagebox.showwarning("Invalid Date", "DOB cannot be in the future!")
                window.lift()
                entries["DOB (YYYY-MM-DD)"].focus_set()
                return
        except ValueError:
            messagebox.showwarning("Invalid Date Format", "Please enter DOB in YYYY-MM-DD format.")
            window.lift()
            window.focus_force()
            entries["DOB (YYYY-MM-DD)"].focus_set()
            window.attributes('-topmost', 1)
            window.after(2000,lambda:window.attributes, ('-topmost', 0))

        # Try to save data to the database
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO Patients (
                    First_Name, Last_Name, DOB, Gender, Street, City, State, Zip_Code,
                    Phone_Number, Email, Emergency_Phone
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data["First Name"], data["Last Name"], data["DOB (YYYY-MM-DD)"], data["Gender (Male/Female)"],
                data["Street"], data["City"], data["State"], data["Zip Code"], data["Phone Number"],
                data["Email"], data["Emergency Phone"]
            ))

            conn.commit()

        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")
            logging.error(f"Database error: {e}")

        finally:
            conn.close()
            messagebox.showinfo("Success ✅", f"Patient {data['First Name']} {data['Last Name']} registered successfully!")
            for entry in entries.values():
                if isinstance(entry, tk.Entry):
                    entry.delete(0, tk.END)

    def cancel_registration():
        confirm = messagebox.askyesno("Cancel", "Are you sure you want to cancel registration?")
        if confirm:
            window.destroy()  # Close the registration window if Yes is clicked
        else:
            window.lift()  # Bring the registration window to the front if No is clicked

    # Buttons
    tk.Button(window, text="Register ✅", command=register_patient, bg="lightgreen", width=20).grid(row=len(labels), columnspan=2, pady=10)
    tk.Button(window, text="Cancel ❌", command=cancel_registration, bg="red", fg="white", width=20).grid(row=len(labels)+1, columnspan=2, pady=5)
