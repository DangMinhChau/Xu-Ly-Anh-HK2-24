import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
class InfoUI(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.info_lable = ttk.Label(self, background="#DFF5FF")
        self.image = ImageTk.PhotoImage(Image.open('info.jpg'))
        self.info_lable.config(image=self.image)
        self.back_btn = ttk.Button(self, text='Trở về', style="Back.TButton", takefocus=False, command=lambda: self.master.show_frame(0))

        # config grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=8)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
    def display(self):
        self.grid(sticky=tk.NSEW)
        self.info_lable.grid(row=0, column=0)
        self.back_btn.grid(row=2, column=0)

    def hide(self):
        self.grid_forget()
        self.grid_forget()
        self.back_btn.grid_forget()



