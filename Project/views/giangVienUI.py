import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
from utils import db
from tkinter import filedialog
import pandas as pd
import os 

class GiangVienUI(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # Create Notebook (Tab control)
        self.notebook = ttk.Notebook(self)
        self.id_giangvien = None
        self.current_class = None
        self.log_text = None
        # Add tabs
        self.student_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.student_tab, text='Sinh viên')
        
        self.log_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.log_tab, text='Log')
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.notebook.grid_rowconfigure(0, weight=1)
        self.notebook.grid_columnconfigure(0, weight=1)
        
        # class tab config
        for tab in (self.student_tab, self.log_tab):
            tab.grid_rowconfigure(0, weight=1)
            tab.grid_rowconfigure(1, weight=8)
            tab.grid_rowconfigure(2, weight=1)
            tab.grid_columnconfigure(0, weight=1)

    def display(self):
        self.current_class = None
        self.grid(row=0, column=0, sticky=tk.NSEW)
        self.notebook.grid(row=0, column=0, sticky=tk.NSEW)
        self.notebook.hide(self.log_tab)
        self.createTabSinhVien()
        self.createTabLog()
        self.classes_cb.set("Vui lòng chọn lớp...")
        self.classes_cb.focus()

    def hide(self):
        self.grid_forget()

    def load_students(self):
        self.student_treeview.delete(*self.student_treeview.get_children())  # Clear existing data
        students = db.get_attendance_data(self.current_class)
        for student in students:
            self.student_treeview.insert('', 'end', values=student)
            
    def load_log_of_student(self, mssv):
        self.log_treeview.delete(*self.log_treeview.get_children())  # Clear existing data
        logs = db.get_student_log(mssv, self.current_class)
        for log in logs:
            self.log_treeview.insert('', 'end', values=log)


    def export_list_student_to_excel(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        print(file_path)
        if file_path !="" and self.current_class is not None:
            data = db.get_attendance_data(MALOP=self.current_class)
            df = pd.DataFrame(data, columns=["MSSV", "HOTEN", "ATTENDANCES"])
            df.to_excel(file_path, index=False)
            open_file= messagebox.askyesno("Thành công", "Xuất file thành công, bạn có muốn mở file không?")
            if open_file:
                os.startfile(file_path)

    def export_log_to_excel(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path != "":
            data = db.get_diemdanh_log(self.current_class)
            df = pd.DataFrame(data, columns=["MSSV", "HOTEN", "DATE", "TIME_CHECKIN", "TIME_CHECKOUT"])
            df.to_excel(file_path, index=False)
            open_file= messagebox.askyesno("Thành công", "Xuất file thành công, bạn có muốn mở file không?")
            if open_file:
                os.startfile(file_path)


    def on_class_select(self, event):
        selected_class = self.classes_cb.get()
        self.current_class = self.classes_dict[selected_class]
        self.load_students()
    
    def show_log_btn_click(self):
        selected_item = self.student_treeview.focus()
        if selected_item and self.current_class is not None:
            data = self.student_treeview.item(selected_item)['values']
            self.notebook.add(self.log_tab, text='Log', state='normal')
            self.notebook.select(1)
            self.load_log_of_student(data[0])
            self.log_text_class.config(text=f"Lớp: {self.classes_cb.get()}")
            self.log_text_student.config(text= f'Sinh viên: {data[1]} - {data[0]}')
        else:
            messagebox.showwarning("Warning", "Vui lòng chọn sinh viên")

    def createTabSinhVien(self):
        self.header_student_frame = ttk.Frame(self.student_tab)
        self.header_student_frame.grid_rowconfigure(0, weight=1)
        for i in range(0, 10):
            self.header_student_frame.grid_columnconfigure(i, weight=1)
            
        ttk.Label(self.header_student_frame, text='Chọn lớp: ', style="Normal.TLabel").grid(row=0, column=0)
        self.classes_dict = {f"{class_name} - {class_id}": class_id for class_id, class_name in db.get_classes_for_teacher(self.id_giangvien)}
        self.classes_cb = ttk.Combobox(self.header_student_frame, values=list(self.classes_dict.keys()), state="readonly")
        self.classes_cb.bind('<<ComboboxSelected>>', self.on_class_select)
        self.classes_cb.grid(row=0, column=1)
        
        text = ttk.Label(self.header_student_frame, text=f"ID giảng viên: {self.id_giangvien}", style="Normal.TLabel")
        text.grid(row=0, column=8)
        ttk.Button(self.header_student_frame, text="Đổi mật khẩu", command=self.change_password_btn_click, style="Normal.TButton", takefocus=False).grid(row=0, column=9)
        
        self.student_treeview = ttk.Treeview(self.student_tab, columns=('#1', '#2', '#3'))
        self.student_treeview.heading('#1', text='Mã số sinh viên')
        self.student_treeview.heading('#2', text='Họ tên sinh viên')
        self.student_treeview.heading('#3', text='Số ngày điểm danh')
        
        self.student_treeview.column('#1', anchor='center')
        self.student_treeview.column('#2', anchor='center')
        self.student_treeview.column('#3', anchor='center')
        self.student_treeview.column("#0", width=0, stretch="no")
        
        self.student_btn_frame = ttk.Frame(self.student_tab)
        for i in range(0, 11):
            self.student_btn_frame.grid_columnconfigure(i, weight=1)
        self.student_btn_frame.grid_rowconfigure(0, weight=1)
        
        self.show_log_btn = ttk.Button(self.student_btn_frame, text='Xem log điểm danh của sinh viên đã chọn', style='Normal.TButton', takefocus=False, command=self.show_log_btn_click)
        self.export_danhsach_btn = ttk.Button(self.student_btn_frame, text="Xuất danh sách sinh viên của lớp", style="Normal.TButton", takefocus=False, command=self.export_list_student_to_excel)
        self.export_log_btn = ttk.Button(self.student_btn_frame, text="Xuất log điểm danh của lớp", style="Normal.TButton", takefocus=False, command=self.export_log_to_excel)
        self.back_btn = ttk.Button(self.student_btn_frame, text="Back", style="Normal.TButton", takefocus=False, command=lambda : self.master.show_frame(0))
                
        self.show_log_btn.grid(row=0, column=0)
        self.export_danhsach_btn.grid(row=0, column=1)
        self.export_log_btn.grid(row=0, column=2)
        self.back_btn.grid(row=0, column=10)
        
        self.header_student_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.student_treeview.grid(row=1, column=0, sticky=tk.NSEW)
        self.student_btn_frame.grid(row=2, column=0, sticky=tk.NSEW)
       
    def createTabLog(self):
        self.header_log_frame = ttk.Frame(self.log_tab)
        self.header_log_frame.grid_rowconfigure(0, weight=1)
        for i in range(0, 10):
            self.header_log_frame.grid_columnconfigure(i, weight=1)
        self.header_log_frame.grid_rowconfigure(0, weight=1)
        self.header_log_frame.grid_rowconfigure(1, weight=1)
        self.log_text_class = ttk.Label(self.header_log_frame, text="", style="Normal.TLabel")
        self.log_text_student = ttk.Label(self.header_log_frame, text="", style="Normal.TLabel")
        self.log_text_class.grid(row=0, column=0, sticky=tk.W)
        self.log_text_student.grid(row=1, column=0, sticky=tk.W)
        
        self.log_treeview = ttk.Treeview(self.log_tab, columns=('#1', '#2', '#3'))
        self.log_treeview.heading('#1', text='Ngày')
        self.log_treeview.heading('#2', text='Thời gian checkin')
        self.log_treeview.heading('#3', text='Thời gian checkout')
        
        self.log_treeview.column('#1', anchor='center')
        self.log_treeview.column('#2', anchor='center')
        self.log_treeview.column('#3', anchor='center')
        self.log_treeview.column("#0", width=0, stretch="no")
        
        self.log_btn_frame = ttk.Frame(self.log_tab)
        for i in range(0, 11):
            self.log_btn_frame.grid_columnconfigure(i, weight=1)
        self.log_btn_frame.grid_rowconfigure(0, weight=1)
        
        self.complete_btn = ttk.Button(self.log_btn_frame, text="Xong", style="Normal.TButton", takefocus=False, command=lambda : self.notebook.hide(self.log_tab))
        self.complete_btn.grid(row=0, column=10)
        
        self.header_log_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.log_treeview.grid(row=1, column=0, sticky=tk.NSEW)
        self.log_btn_frame.grid(row=2, column=0, sticky=tk.NSEW)
        
    def change_password_btn_click(self):
        newPassword = simpledialog.askstring("Đổi mật khẩu", "Vui lòng nhập mật khẩu mới: ")
        if newPassword: 
            if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn đổi mật khẩu không?"):
                db.change_password_teacher(self.id_giangvien, newPassword)
                messagebox.showinfo("Thành công", "Đổi mật khẩu thành công")
        elif newPassword=="":
            messagebox.showwarning("Warning", "Vui lòng nhập mật khẩu mới")