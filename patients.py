import tkinter as tk
from tkinter import messagebox
import logging
from db_connection import get_connection

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

def open_patient_window():
    window = tk.Toplevel()
    window.title("🧍 Register Patient")
    window.geometry("500x600")

    # Labels & Entries
    labels = [
        "First Name", "Last Name", "DOB (YYYY-MM-DD)", "Gender (Male/Female)",
        "Street", "City", "State", "Zip Code", "Phone Number",
        "Email", "Emergency Phone"
    ]
    entries = {}

    for idx, label in enumerate(labels):
        tk.Label(window, text=label).grid(row=idx, column=0, padx=10, pady=5, sticky="e")
        entry = tk.Entry(window, width=30)
        entry.grid(row=idx, column=1, pady=5, padx=10)
        entries[label] = entry

    def register_patient():
        data = {label: entries[label].get().strip() for label in labels}

        # Simple validation
        if not data["First Name"] or not data["Last Name"] or not data["DOB (YYYY-MM-DD)"] or not data["Gender (Male/Female)"] :
            messagebox.showwarning("Missing Info", "Please fill in required fields: First Name, Last Name, DOB,")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Log the SQL query before executing it
            sql_query = f"""
                INSERT INTO Patients (
                    First_Name, Last_Name, DOB, Gender, Street, City, State, Zip_Code,
                    Phone_Number, Email, Emergency_Phone
                )
                VALUES ('{data["First Name"]}', '{data["Last Name"]}', '{data["DOB (YYYY-MM-DD)"]}', '{data["Gender (Male/Female)"]}',
                        '{data["Street"]}', '{data["City"]}', '{data["State"]}', '{data["Zip Code"]}', 
                        '{data["Phone Number"]}', '{data["Email"]}', '{data["Emergency Phone"]}')
            """
            logging.debug(f"Executing SQL query: {sql_query}")

            # Insert patient data into the database using a prepared statement
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
            # Handle any database errors
            messagebox.showerror("Error", f"Database error: {e}")
            logging.error(f"Database error: {e}")  # Log the error

        finally:
            conn.close()  # Ensure connection is always closed
            messagebox.showinfo("Success ✅", f"Patient {data['First Name']} {data['Last Name']} registered successfully!")

            # Clear the form fields after successful registration
            for entry in entries.values():
                entry.delete(0, tk.END)

    # Submit Button
    tk.Button(window, text="Register ✅", command=register_patient, bg="lightgreen", width=20).grid(row=len(labels), columnspan=2, pady=20)
