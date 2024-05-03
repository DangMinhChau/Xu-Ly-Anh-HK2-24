import tkinter as tk
from tkinter import ttk
from .sinhVienUI import SinhVienUI
from .homeUI import HomeUI
from .adminUI import AdminUI
from .infoUI import InfoUI
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.style = ttk.Style()
        self.create_style()
        self.geometry("1041x614")
        self.minsize(width=1041, height=614)
        self.after(0, lambda: self.state('zoomed'))
        self.title("Ứng dụng điểm danh")
        self.config(background="#DFF5FF")
        self.frames = []
        self.create_frame()
        self.frames[0].display()
        self.currentFrame = self.frames[0]

        # config grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
    def show_frame(self, frame_index):
        self.currentFrame.hide()
        self.currentFrame = self.frames[frame_index]
        self.currentFrame.display()
    
    def create_frame(self):
        for F in (HomeUI, SinhVienUI, AdminUI, InfoUI):
            self.frames.append(F(self))

    def create_style(self):
        main_color = "#DFF5FF"
        self.style.theme_use('default')
        self.style.configure("HomeButton.TButton", background=main_color, borderwidth=0, font=("Arial", 28, "bold"), foreground='#378CE7')
        self.style.map("HomeButton.TButton", background=[('active', main_color)], foreground=[('active', '#67C6E3')])

        self.style.configure("SinhVienButton.TButton", background=main_color, borderwidth=0, font=("Arial", 18, "bold"), foreground='#378CE7')
        self.style.map("SinhVienButton.TButton", background=[('active', main_color)], foreground=[('active', '#67C6E3')])

        self.style.configure("Admin.TButton", background = "#378CE7", foreground = "white")
        self.style.map("Admin.TButton", background=[('active', '#378CE7')], foreground=[('active', '#67C6E3')])

        self.style.configure("Back.TButton", background=main_color, borderwidth=0, font=("Arial", 20), foreground='#378CE7')
        self.style.map("Back.TButton", background=[('active', main_color)], foreground=[('active', '#FF204E')])

        self.style.configure("TreeView", background = main_color)
        self.style.configure("TFrame", background=main_color)