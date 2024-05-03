import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

import config

class HomeUI(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.style = ttk.Style(self)
        self.panel = tk.Label(self, text='HCMUTE', background="#DFF5FF", foreground="#FF204E", font=("Arial", 40, "bold"))
        self.buttons_frame = ttk.Frame(self)
        self.sinhvien_btn = ttk.Button(self.buttons_frame, text='Sinh viên', style="HomeButton.TButton", takefocus=False, command=lambda: self.button_click(1))
        self.admin_btn = ttk.Button(self.buttons_frame, text='Giảng viên', style="HomeButton.TButton", takefocus=False, command=self.admin_btn_click)
        self.info_btn = ttk.Button(self.buttons_frame, text='Thông tin', style="HomeButton.TButton", takefocus=False, command=lambda: self.button_click(3))
        self.exit_btn = ttk.Button(self.buttons_frame, text="Thoát", style="Back.TButton", takefocus=False, command=self.exit)

        # config grid
        self.grid(row=0, column=0, sticky=tk.NSEW)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=9)
        self.buttons_frame.grid_columnconfigure(0, weight=1)
        for i in range(0, 7):
            self.buttons_frame.grid_rowconfigure(i, weight=1)

    
    def display(self):
        self.grid(row=0, column=0, sticky=tk.NSEW)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=9)
        self.panel.grid(row=0, column=0)

        self.buttons_frame.grid(row=1, column=0, sticky=tk.NSEW)
        self.sinhvien_btn.grid(row=1, sticky=tk.NSEW)
        self.admin_btn.grid(row=2, sticky=tk.NSEW)
        self.info_btn.grid(row=3, sticky=tk.NSEW)
        self.exit_btn.grid(row=6)

    def hide(self):
        for w in (self,  self.panel, self.buttons_frame, self.sinhvien_btn, self.admin_btn, self.info_btn, self.exit_btn):
            w.grid_forget()
        
    def button_click(self, frameName):
        self.master.show_frame(frameName)

    def admin_btn_click(self):
        password = simpledialog.askstring("Password", "Enter your password", show="*")
        if password == config.admin_password:
            self.master.show_frame(2)
        else:
            messagebox.showwarning("Warning", "Password is incorrect")

    def exit(self):
        ans = messagebox.askyesno("Thoát", "Bạn có muốn đóng ứng dụng không?")
        if ans is True:
            self.master.destroy()