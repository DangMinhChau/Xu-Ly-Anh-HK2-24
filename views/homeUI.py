import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

import config


class HomeUI(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.panel = ttk.Label(self, text='Welcome')
        self.sinhvien_btn = ttk.Button(self, text='Sinh Viên', command=lambda: self.button_click(1))
        self.admin_btn = ttk.Button(self, text='Admin', command=self.admin_btn_click)
        self.info_btn = ttk.Button(self, text='Thông tin', command=lambda: self.button_click(3))
        self.exit_btn = ttk.Button(self, text="Thoát", command=self.exit)
    
    def display(self):
        self.pack(expand=True, fill=tk.BOTH, side=tk.TOP, anchor=tk.CENTER)
        self.panel.pack()
        self.sinhvien_btn.pack()
        self.admin_btn.pack()
        self.info_btn.pack()
        self.exit_btn.pack()
    
    def hide(self):
        for w in (self, self.panel, self.sinhvien_btn, self.admin_btn, self.info_btn, self.exit_btn):
            w.pack_forget()
        
    def button_click(self, frameName):
        self.master.show_frame(frameName)

    def admin_btn_click(self):
        password = simpledialog.askstring("Admin Password", "Enter your password", show="*")
        if password == config.admin_password:
            self.master.show_frame(2)

    def exit(self):
        ans = messagebox.askyesno("Thoát", "Bạn có muốn đóng ứng dụng không?")
        if ans is True:
            self.master.destroy()