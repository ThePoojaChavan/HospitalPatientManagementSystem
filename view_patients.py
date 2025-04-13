import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import get_connection

def delete_patient(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a patient to delete.")
        return

    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this patient?")
    if not confirm:
        return

    patient_id = tree.item(selected_item[0])['values'][0]

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Patients WHERE Patient_ID = ?", (patient_id,))
        conn.commit()
        conn.close()

        tree.delete(selected_item[0])
        messagebox.showinfo("Deleted", "Patient record deleted successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete patient: {e}")
        print(f"Error: {e}")

def edit_patient(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a patient to edit.")
        return

    values = tree.item(selected_item[0])['values']
    patient_id = values[0]

    edit_win = tk.Toplevel()
    edit_win.grab_set()  # Allow editing even when the main window is active
    edit_win.title("✏️ Edit Patient")
    edit_win.geometry("500x500")

    fields = ["First_Name", "Last_Name", "DOB", "Gender", "Phone_Number", "Email"]
    entries = {}

    for idx, field in enumerate(fields):
        tk.Label(edit_win, text=field).pack()
        entry = tk.Entry(edit_win, width=40)
        entry.insert(0, values[idx+1])  # Skip Patient ID
        entry.pack(pady=5)
        entries[field] = entry

    def save_changes():
        updated_values = [entry.get() for entry in entries.values()]
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Patients 
                SET First_Name=?, Last_Name=?, DOB=?, Gender=?, Phone_Number=?, Email=?
                WHERE Patient_ID = ?
            """, (*updated_values, patient_id))
            conn.commit()
            conn.close()

            for i, val in enumerate(updated_values):
                tree.set(selected_item[0], column=tree["columns"][i+1], value=val)

            messagebox.showinfo("Success", "Patient record updated successfully.")
            edit_win.destroy()
            tree.selection_set(selected_item[0])  # Reselect the edited item
            #tree.selection_clear()  # Deselect the edited item
            
            

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update patient: {e}")
            print(f"Error: {e}")

    tk.Button(edit_win, text="Save Changes", command=save_changes, bg="lightgreen", fg="white", height=2, width=20).pack(pady=5)
    tk.Button(edit_win, text="Cancel", command=edit_win.destroy, bg="red", fg="white", height=2, width=20).pack(pady=5)

def view_patients_window():
    window = tk.Toplevel()
    window.title("👀 View Patients")
    window.geometry("800x400")
    window.state('zoomed')  # Maximize the window
    #window.grab_set()  # Focus on this window until it's closed

    tree = ttk.Treeview(window, columns=("Patient ID", "First Name", "Last Name", "DOB", "Gender", "Street", "City","State", "ZIP", "Phone", "Email","Emergency Phone"), show="headings")

    # Define column headings
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    # Set individual column widths
    tree.column("Patient ID", width=50)
    tree.column("First Name", width=150)
    tree.column("Last Name", width=150)
    tree.column("DOB", width=100)
    tree.column("Gender", width=100)
    tree.column("Street", width=150)
    tree.column("City", width=100)
    tree.column("State", width=100)
    tree.column("ZIP", width=100)
    tree.column("Phone", width=100)
    tree.column("Email", width=150)
    tree.column("Emergency Phone", width=100)

    tree.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Patients")
        rows = cursor.fetchall()

        for row in rows:
            tree.insert("", "end", values=row)

        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve patient records: {e}")
        print(f"Error: {e}")

    # Buttons
    btn_frame = tk.Frame(window)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="✏️ Edit Selected", command=lambda: edit_patient(tree), bg="orange", fg="white", width=20, height=2).pack(side="left", padx=10)
    tk.Button(btn_frame, text="🗑️ Delete Selected", command=lambda: delete_patient(tree), bg="light blue", fg="white", width=20, height=2).pack(side="left", padx=10)
    tk.Button(btn_frame, text="❌ Close", command=window.destroy, bg="red", fg="white", width=20, height=2).pack(side="left", padx=10)


