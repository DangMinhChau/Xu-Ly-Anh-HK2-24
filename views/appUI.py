import tkinter as tk
from tkinter import ttk
from .sinhVienUI import SinhVienUI
from .homeUI import HomeUI

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.after(0, lambda: self.state('zoomed'))
        self.sinhVienUI = SinhVienUI(self)
        #self.homeUI = HomeUI(self)
        #self.homeUI.pack()
