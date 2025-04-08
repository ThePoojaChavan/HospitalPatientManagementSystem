import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime
from db_connection import get_connection

def open_appointments_window(root):
    window = tk.Toplevel()
    window.title("📅 Appointments Management")
    window.geometry("800x650")

    frame = tk.Frame(window)
    frame.pack(pady=20)

    # Fetch Patients and Doctors
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT Patient_ID, First_Name || ' ' || Last_Name FROM Patients")
    patients = cursor.fetchall()

    cursor.execute("SELECT Doctor_ID, First_Name || ' ' || Last_Name || ' (' || Specialization || ')' FROM Doctors")
    doctors = cursor.fetchall()

    conn.close()

    # Variables
    selected_patient = tk.StringVar()
    selected_doctor = tk.StringVar()
    selected_day = tk.StringVar()
    selected_time = tk.StringVar()
    app_date_var = tk.StringVar()

    # Patient Dropdown
    tk.Label(frame, text="Patient").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    patient_dropdown = ttk.Combobox(frame, textvariable=selected_patient, width=40, values=[
        f"{p[0]} - {p[1]}" for p in patients
    ])
    patient_dropdown.grid(row=0, column=1, padx=10, pady=5)

    # Doctor Dropdown
    tk.Label(frame, text="Doctor").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    doctor_dropdown = ttk.Combobox(frame, textvariable=selected_doctor, width=40, values=[
        f"{d[0]} - {d[1]}" for d in doctors
    ])
    doctor_dropdown.grid(row=1, column=1, padx=10, pady=5)

    # Appointment Date
    tk.Label(frame, text="Appointment Date (YYYY-MM-DD)").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    app_date_entry = tk.Entry(frame, textvariable=app_date_var, width=30)
    app_date_entry.grid(row=2, column=1, pady=5, padx=10)

    # Available Days Dropdown
    tk.Label(frame, text="Available Day").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    day_dropdown = ttk.Combobox(frame, textvariable=selected_day, width=40)
    day_dropdown.grid(row=3, column=1, padx=10, pady=5)

    # Available Time Dropdown
    tk.Label(frame, text="Available Time").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    time_dropdown = ttk.Combobox(frame, textvariable=selected_time, width=40)
    time_dropdown.grid(row=4, column=1, padx=10, pady=5)

    def fetch_availability():
        # Fetch Doctor Availability based on selected doctor
        doctor_id = selected_doctor.get().split(" - ")[0]

        conn = get_connection()
        cursor = conn.cursor()

        # Fetch Available Days and Times for the selected doctor
        cursor.execute("""
            SELECT Availability_Day, Start_Time, End_Time 
            FROM Doctor_Availability 
            WHERE Doctor_ID = ?
        """, (doctor_id,))
        availability = cursor.fetchall()

        # Update the Available Days dropdown
        days = sorted(set(avail[0] for avail in availability))
        day_dropdown['values'] = days

        # Update the Available Times dropdown based on selected day
        def update_times(*args):  # Accept all three arguments
            selected_avail_day = selected_day.get()

            # Get the start and end times for the selected day
            times = sorted(set(
                f"{avail[1]} - {avail[2]}" for avail in availability if avail[0] == selected_avail_day
            ))

            time_dropdown['values'] = times

        selected_day.trace_add("write", update_times)

        conn.close()

    # Update availability when doctor is selected
    doctor_dropdown.bind("<<ComboboxSelected>>", lambda event: fetch_availability())

    def register_appointment():
        try:
            patient_id = selected_patient.get().split(" - ")[0]
            doctor_id = selected_doctor.get().split(" - ")[0]
            app_date = app_date_var.get().strip()
            app_time = selected_time.get().strip()

             # Check if appointment date is entered
            if not app_date:
                messagebox.showerror("Invalid Input", "Appointment date must be entered.")
                app_date_entry.focus_set()  # Focus back on the appointment date entry
                return
            
            # Validate date/time format
            app_datetime_str = f"{app_date} {app_time.split(' - ')[0]}"
            app_datetime = datetime.strptime(app_datetime_str, "%Y-%m-%d %I:%M %p")

            if app_datetime <= datetime.now():
                messagebox.showwarning("Invalid Date/Time", "The appointment must be scheduled for a future time.")
                return

            conn = get_connection()
            cursor = conn.cursor()

            # Check patient and doctor existence
            cursor.execute("SELECT COUNT(*) FROM Patients WHERE Patient_ID = ?", (patient_id,))
            if cursor.fetchone()[0] == 0:
                messagebox.showerror("Invalid Patient", "Patient ID does not exist.")
                conn.close()
                return

            cursor.execute("SELECT COUNT(*) FROM Doctors WHERE Doctor_ID = ?", (doctor_id,))
            if cursor.fetchone()[0] == 0:
                messagebox.showerror("Invalid Doctor", "Doctor ID does not exist.")
                conn.close()
                return

            cursor.execute(""" 
                INSERT INTO Appointments (Patient_ID, Doctor_ID, App_Date, App_Time, Status)
                VALUES (?, ?, ?, ?, ?)
            """, (patient_id, doctor_id, app_date, app_time, "Scheduled"))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Appointment successfully registered.")
            app_date_var.set("")
            selected_time.set("")
            load_appointments()

        except Exception as e:
            messagebox.showerror("Error", f"Error registering appointment: {e}")

    tk.Button(window, text="Register Appointment ✅", command=register_appointment, bg="lightgreen", width=30).pack(pady=10)

    # Appointment Listbox
    listbox = tk.Listbox(window, width=100, height=12)
    listbox.pack(pady=20)

    def load_appointments():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.Appointment_ID, p.First_Name || ' ' || p.Last_Name, 
                       d.First_Name || ' ' || d.Last_Name, 
                       a.App_Date, a.App_Time, a.Status
                FROM Appointments a
                JOIN Patients p ON a.Patient_ID = p.Patient_ID
                JOIN Doctors d ON a.Doctor_ID = d.Doctor_ID
                ORDER BY a.App_Date, a.App_Time
            """)
            appointments = cursor.fetchall()
            listbox.delete(0, tk.END)
            for appt in appointments:
                listbox.insert(tk.END, f"ID: {appt[0]} | Patient: {appt[1]} | Doctor: {appt[2]} | Date: {appt[3]} | Time: {appt[4]} | Status: {appt[5]}")
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load appointments: {e}")

    def cancel_appointment():
        try:
            selected = listbox.curselection()
            if not selected:
                messagebox.showwarning("No selection", "Please select an appointment to cancel.")
                return

            item_text = listbox.get(selected[0])
            appt_id = item_text.split("|")[0].split(":")[1].strip()

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE Appointments SET Status = ? WHERE Appointment_ID = ?", ("Cancelled", appt_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Cancelled", "Appointment has been cancelled.")
            load_appointments()

        except Exception as e:
            messagebox.showerror("Error", f"Error cancelling appointment: {e}")

    def go_back_to_main_menu():
        window.destroy()
        root.deiconify()

    tk.Button(window, text="Cancel Appointment ❌", command=cancel_appointment, bg="orange", width=30).pack(pady=5)
    tk.Button(window, text="Go Back to Main Menu ⬅️", command=go_back_to_main_menu, bg="lightblue", width=30).pack(pady=5)

    load_appointments()
