import tkinter as tk
from tkinter import ttk

class HomeUI(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.panel = ttk.Label(text='Welcome')
        self.sinhvien_btn = ttk.Button(text='Sinh Viên')
        self.giangvien_btn = ttk.Button(text='Giảng Viên')
        self.admin_btn = ttk.Button(text='Admin')
        self.info_btn = ttk.Button(text='?')
        
        self.panel.pack()
        self.sinhvien_btn.pack()
        self.giangvien_btn.pack()
        self.admin_btn.pack()
        self.info_btn.pack()