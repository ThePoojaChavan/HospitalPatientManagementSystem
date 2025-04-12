import tkinter as tk
from tkinter import messagebox
import sqlite3
from db_connection import get_connection
from datetime import datetime

def open_billing_window(root):
    window = tk.Toplevel(root)
    window.title("💵 Billing Management")
    window.geometry("700x600")

    # Create a frame for the billing form
    frame = tk.Frame(window)
    frame.pack(pady=20)

    # Labels & Entries for Billing
    labels = [
        "Appointment ID", "Patient ID", "Amount", "Billing Date (YYYY-MM-DD)"
    ]
    entries = {}

    for idx, label in enumerate(labels):
        tk.Label(frame, text=label).grid(row=idx, column=0, padx=10, pady=5, sticky="e")
        entry = tk.Entry(frame, width=30)
        entry.grid(row=idx, column=1, pady=5, padx=10)
        entries[label] = entry

    app_id_entry = entries["Appointment ID"]
    patient_id_entry = entries["Patient ID"]
    amount_entry = entries["Amount"]
    billing_date_entry = entries["Billing Date (YYYY-MM-DD)"]

    def generate_bill():
        try:
            # Get the values from the input fields
            app_id = app_id_entry.get().strip()
            patient_id = patient_id_entry.get().strip()
            amount = amount_entry.get().strip()
            billing_date = billing_date_entry.get().strip()

            if not app_id or not patient_id or not amount or not billing_date:
                messagebox.showwarning("Missing Data", "All fields must be filled.")
                return

            # Convert amount to float
            amount = float(amount)

            # Check if Appointment ID exists
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Appointments WHERE Appointment_ID = ?", (app_id,))
            if cursor.fetchone()[0] == 0:
                messagebox.showwarning("Invalid Appointment ID", "Appointment ID does not exist.")
                conn.close()
                return

            # Check if Patient ID exists
            cursor.execute("SELECT COUNT(*) FROM Patients WHERE Patient_ID = ?", (patient_id,))
            if cursor.fetchone()[0] == 0:
                messagebox.showwarning("Invalid Patient ID", "Patient ID does not exist.")
                conn.close()
                return

            # Insert the bill into the Billing table
            cursor.execute(""" 
                INSERT INTO Billing (Appointment_ID, Patient_ID, Amount, Status, Bill_Date)
                VALUES (?, ?, ?, ?, ?)
            """, (app_id, patient_id, amount, "Pending", billing_date))

            conn.commit()
            conn.close()

            messagebox.showinfo("Bill Generated", "The bill has been successfully generated.")
            app_id_entry.delete(0, tk.END)
            patient_id_entry.delete(0, tk.END)
            amount_entry.delete(0, tk.END)
            billing_date_entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"Error generating bill: {e}")

    # Submit Button to generate the bill
    tk.Button(window, text="Generate Bill ✅", command=generate_bill, bg="lightgreen",width=25).pack(pady=10)

    # Listbox to show bills
    listbox = tk.Listbox(window, width=100, height=10)
    listbox.pack(pady=20)

    def load_bills():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT Patients.First_Name, Patients.Last_Name, Billing.Bill_ID, Billing.Appointment_ID, 
                       Billing.Patient_ID, Billing.Amount, Billing.Status, Billing.Bill_Date
                FROM Billing
                JOIN Patients ON Billing.Patient_ID = Patients.Patient_ID
                ORDER BY Billing.Bill_Date DESC
            """)
            bills = cursor.fetchall()
            listbox.delete(0, tk.END)
            for bill in bills:
                listbox.insert(tk.END, f"Patient: {bill[0]} {bill[1]} | Bill ID: {bill[2]} | Appointment ID: {bill[3]} | "
                                       f"Amount: {bill[5]} | Status: {bill[6]} | Date: {bill[7]}")
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load bills: {e}")

    def mark_as_paid():
        try:
            selected = listbox.curselection()
            if not selected:
                messagebox.showwarning("No selection", "Please select a bill to mark as paid.")
                return

            item_text = listbox.get(selected[0])
            bill_id = item_text.split("|")[0].split(":")[1].strip()

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE Billing SET Status = ? WHERE Bill_ID = ?", ("Paid", bill_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Paid", "Bill has been marked as Paid.")
            load_bills()  # Refresh the list of bills

        except Exception as e:
            messagebox.showerror("Error", f"Error marking bill as paid: {e}")

    def go_back_to_main_menu():
        window.destroy()  # Close the billing window
        root.deiconify()  # Unhide the main menu window (if using root as main window)

    # Mark as Paid Button
    tk.Button(window, text="Mark as Paid ✅", command=mark_as_paid, bg="lightblue", width=30).pack(pady=10)

    # Go Back Button
    tk.Button(window, text="Go Back to Main Menu ⬅️", command=go_back_to_main_menu, bg="lightblue", width=30).pack(pady=10)

    # Load the initial list of bills
    load_bills()
