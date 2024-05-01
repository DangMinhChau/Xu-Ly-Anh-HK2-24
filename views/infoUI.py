import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
class InfoUI(ttk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.info_lable = ttk.Label(self)
        self.image = ImageTk.PhotoImage(Image.open('info.png'))
        self.info_lable.config(image=self.image)
        self.back_btn = ttk.Button(self, text='back', command=lambda: self.master.show_frame(0))

    def display(self):
        self.pack(fill=tk.BOTH, expand=True)
        self.info_lable.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.back_btn.pack(side=tk.BOTTOM)

    def hide(self):
        self.pack_forget()
        self.place_forget()
        self.back_btn.pack_forget()



