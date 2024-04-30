import tkinter as tk
from tkinter import ttk
from .sinhVienUI import SinhVienUI
from .homeUI import HomeUI
from .adminUI import AdminUI

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry(f"{self.winfo_width()}x{self.winfo_height()}")
        self.after(0, lambda: self.state('zoomed'))
        self.frames = []
        self.create_frame()
        self.frames[0].display()
        self.currentFrame = self.frames[0]
        
    def show_frame(self, frame_index):
        self.currentFrame.hide()
        self.currentFrame = self.frames[frame_index]
        self.currentFrame.display()
    
    def create_frame(self):
        for F in (HomeUI, SinhVienUI, AdminUI):
            self.frames.append(F(self))
        