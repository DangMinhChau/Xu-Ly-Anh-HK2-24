import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from utils import db
from tkinter import filedialog
import pandas as pd
class AdminUI(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Create Notebook (Tab control)
        self.notebook = ttk.Notebook(self)
        # Add tabs
        self.student_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.student_tab, text="Students")
        self.student_tree = ttk.Treeview(self.student_tab, columns=("MSSV", "HOTEN", "ATTENDANCES"))
        self.student_tree.heading("#0", text="STT", anchor='center')
        self.student_tree.heading("MSSV", text="Mã số sinh viên", anchor='center')
        self.student_tree.heading("HOTEN", text="Họ tên", anchor='center')
        self.student_tree.heading("ATTENDANCES", text="Số ngày điểm danh", anchor='center')
        self.student_tree.column("#0", anchor="center")
        self.student_tree.column("MSSV", anchor="center")
        self.student_tree.column("HOTEN", anchor="center")
        self.student_tree.column("ATTENDANCES", anchor="center")
        self.btn_frame = ttk.Frame(self)
        self.add_btn = ttk.Button(self.btn_frame, text="Add Student", command=self.add_student_btn_click)
        self.edit_btn = ttk.Button(self.btn_frame, text="Edit Student", command=self.edit_student_btn_click)
        self.delete_btn = ttk.Button(self.btn_frame, text="Delete Student", command=self.delete_student)
        self.export_danhsach_btn = ttk.Button(self.btn_frame, text="Export List", command=self.export_list_student_to_excel)
        self.export_log_btn = ttk.Button(self.btn_frame, text="Export Log", command=self.export_log_to_excel)
        self.back_btn = tk.Button(self.btn_frame, text="Back", command=lambda : self.master.show_frame(0))

        # config grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=9)
        self.grid_rowconfigure(1, weight=1)
        self.notebook.grid_columnconfigure(0, weight=1)
        self.notebook.grid_rowconfigure(0, weight=1)
        self.student_tab.grid_columnconfigure(0, weight=1)
        self.student_tab.rowconfigure(0, weight=1)
        for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            self.btn_frame.grid_columnconfigure(i, weight=1)
        self.btn_frame.grid_rowconfigure(0, weight=1)


        # load student
        self.load_students()

    def display(self):
        self.grid(sticky=tk.NSEW)
        self.notebook.grid(row=0, column=0, sticky=tk.NSEW)
        self.student_tab.grid(row=0, column=0, sticky=tk.NSEW)
        # Student table
        self.student_tree.grid(row=0, column=0, sticky=tk.NSEW)
        # Buttons
        self.btn_frame.grid(row=1, column=0, sticky=tk.NSEW)
        self.add_btn.grid(row=0, column=3)
        self.edit_btn.grid(row=0, column=4)
        self.delete_btn.grid(row=0, column=5)
        self.export_danhsach_btn.grid(row=0, column=6)
        self.export_log_btn.grid(row=0, column=7)
        self.back_btn.grid(row=0, column=10)
        self.load_students()

    def hide(self):
        for w in (self, self.notebook, self.student_tab, self.student_tree, self.student_tree, self.btn_frame, self.add_btn, self.edit_btn, self.delete_btn, self.export_danhsach_btn, self.export_log_btn, self.back_btn):
            w.grid_forget()

    def load_students(self):
        self.student_tree.delete(*self.student_tree.get_children())  # Clear existing data
        students = db.get_attendance_data()
        for index, student in enumerate(students, start=1):
            self.student_tree.insert("", "end", text=index, values=student)

    def add_student_btn_click(self):
        add_window = tk.Toplevel(self.master)
        add_window.title("Add Student")
        window_width = 200  # Set the width of the window
        window_height = 110  # Set the height of the window
        screen_width = add_window.winfo_screenwidth()
        screen_height = add_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        add_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Labels and Entries
        tk.Label(add_window, text="MSSV:").grid(row=0, column=0, padx=5, pady=5)
        self.mssv_entry = tk.Entry(add_window)
        self.mssv_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)
        self.mssv_entry.focus_set()

        tk.Label(add_window, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(add_window)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)

        # Add Button
        add_btn = tk.Button(add_window, text="Add", command=self.save_added_student)
        add_btn.grid(row=2, column=0, pady=10, columnspan=2)
        self.mssv_entry.bind("<Return>", lambda event : self.name_entry.focus())
        self.name_entry.bind("<Return>", lambda event : add_btn.invoke())

    def save_added_student(self):
        mssv = self.mssv_entry.get()
        name = self.name_entry.get()

        if mssv and name:
            db.insert_student(mssv, name)
            self.load_students()  # Reload student list
            self.mssv_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.mssv_entry.focus()
        else:
            tk.messagebox.showerror("Error", "Please enter both MSSV and Name.")
    def edit_student_btn_click(self):
        selected_item = self.student_tree.focus()
        if selected_item:
            data = self.student_tree.item(selected_item)['values']
            edit_window = tk.Toplevel(self.master)
            edit_window.title("Edit Student")
            window_width = 200  # Set the width of the window
            window_height = 110  # Set the height of the window
            screen_width = edit_window.winfo_screenwidth()
            screen_height = edit_window.winfo_screenheight()
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            edit_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

            # Labels and Entries
            tk.Label(edit_window, text="MSSV:").grid(row=0, column=0, padx=5, pady=5)
            self.edit_mssv_label = ttk.Label(edit_window)
            self.edit_mssv_label.grid(row=0, column=1, padx=5, pady=5)

            tk.Label(edit_window, text="Name:").grid(row=1, column=0, padx=5, pady=5)
            self.edit_name_entry = tk.Entry(edit_window)
            self.edit_name_entry.grid(row=1, column=1, padx=5, pady=5)
            self.edit_name_entry.focus()

            # Populate current data
            mssv = data[0]
            self.edit_mssv_label.config(text=mssv)
            self.edit_name_entry.insert(0, data[1])

            # Update Button
            update_btn = tk.Button(edit_window, text="Update", command=lambda: self.update_student(mssv))
            update_btn.grid(row=2, column=0, pady=10, columnspan=2)
            self.edit_name_entry.bind("<Return>", lambda event : (update_btn.invoke(), edit_window.destroy()))
        else:
            tk.messagebox.showerror("Error", "Please select a student to edit.")

    def update_student(self, mssv):
        name = self.edit_name_entry.get()
        if mssv != '' and name != '':
            db.update_student(mssv, name)
            self.load_students()  # Reload student list
        else:
            tk.messagebox.showerror("Error", "Please enter both MSSV and Name.")

    def delete_student(self):
        selected_item = self.student_tree.focus()
        if selected_item:
            if tk.messagebox.askyesno("Delete Student", "Are you sure you want to delete this student?"):
                data = self.student_tree.item(selected_item)['values']
                mssv = data[0]
                db.delete_student(mssv)
                self.load_students()  # Reload student list
        else:
            tk.messagebox.showerror("Error", "Please select a student to delete.")

    def export_list_student_to_excel(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        print(file_path)
        if file_path !="":
            data = db.get_attendance_data()
            df = pd.DataFrame(data, columns=["MSSV", "HOTEN", "ATTENDANCES"])
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Export", "Exported Successfully.")

    def export_log_to_excel(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path != "":
            data = db.get_diemdanh_log()
            df = pd.DataFrame(data, columns=["MSSV", "DATE", "TIME"])
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Export", "Exported Successfully.")

