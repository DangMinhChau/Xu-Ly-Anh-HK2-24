import tkinter as tk
from tkinter import ttk
from .sinhVienUI import SinhVienUI
from .homeUI import HomeUI
from .adminUI import AdminUI
from .infoUI import InfoUI
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("1041x614")
        self.minsize(width=1041, height=614)
        self.after(0, lambda: self.state('zoomed'))
        self.title("Ứng dụng điểm danh")
        self.frames = []
        self.create_frame()
        self.frames[0].display()
        self.currentFrame = self.frames[0]
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
    def show_frame(self, frame_index):
        self.currentFrame.hide()
        self.currentFrame = self.frames[frame_index]
        self.currentFrame.display()
    
    def create_frame(self):
        for F in (HomeUI, SinhVienUI, AdminUI, InfoUI):
            self.frames.append(F(self))
        