import tkinter as tk
from patients import open_patient_window
from view_patients import view_patients_window
from doctors import open_doctor_window
from appointments import open_appointments_window
from billing import open_billing_window

def main():
    root = tk.Tk()
    root.title("🏥 Hospital Patient Management System")
    root.geometry("800x650")
    root.resizable(False, False)

    tk.Label(root, text="🏥 Hospital Patient Management System Main Menu", font=("Arial", 18, "bold")).pack(pady=20)

    # Buttons
    tk.Button(root, text="🧍 Register Patient", command=open_patient_window, width=25, height=2, bg="#f0f0f0").pack(pady=10)
    tk.Button(root, text="🔍 View Patients", command=view_patients_window, width=25, height=2, bg="#f0f0f0").pack(pady=10)
    tk.Button(root, text="🩺 Doctor Management", command=lambda: open_doctor_window(root), width=25, height=2).pack(pady=10)
    tk.Button(root, text="📅 Appointments", command=lambda: open_appointments_window(root), width=25, height=2).pack(pady=10)
    tk.Button(root, text="💵 Billing", command=lambda: open_billing_window(root), width=25, height=2).pack(pady=10)
    tk.Button(root, text="Exit", command=root.quit, width=25, height=2, bg="red", fg="white").pack(pady=30)
    root.mainloop()

if __name__ == "__main__":
    main()