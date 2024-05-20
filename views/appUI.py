import tkinter as tk
from tkinter import ttk
import cv2 as cv
import config
from .diemDanhUI import DiemDanhUI
from .homeUI import HomeUI
from .giangVienUI import GiangVienUI
from .infoUI import InfoUI
from .adminUI import AdminUI
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
        self.detector = cv.FaceDetectorYN.create(model=f'{config.root_dir}/models/face_detection_yunet_2023mar.onnx',
                                                 input_size=[640, 480], config="", score_threshold=0.9)
        self.sface = cv.FaceRecognizerSF.create(model=f'{config.root_dir}/models/face_recognition_sface_2021dec.onnx',
                                                config="")

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
        for F in (HomeUI, DiemDanhUI, GiangVienUI, AdminUI, InfoUI):
            self.frames.append(F(self))

    def create_style(self):
        main_color = "#DFF5FF"
        self.style.theme_use('default')
        self.style.configure("HomeButton.TButton", background=main_color, borderwidth=0, font=("Arial", 28, "bold"), foreground='#378CE7')
        self.style.map("HomeButton.TButton", background=[('active', main_color)], foreground=[('active', '#67C6E3')])

        self.style.configure("SinhVienButton.TButton", background=main_color, borderwidth=0, font=("Arial", 18, "bold"), foreground='#378CE7')
        self.style.map("SinhVienButton.TButton", background=[('active', main_color)], foreground=[('active', '#67C6E3')])

        self.style.configure("Normal.TButton", background = "#378CE7", foreground = "white", font=("Arial", 12))
        self.style.map("Normal.TButton", background=[('active', '#378CE7')], foreground=[('active', '#67C6E3')])

        self.style.configure("Special.TButton", background = "green", foreground = "white", font=("Arial", 12, "bold"))
        self.style.map("Special.TButton", background=[('active', 'green')], foreground=[('active', '#67C6E3')])

        self.style.configure("Back.TButton", background=main_color, borderwidth=0, font=("Arial", 20), foreground='#378CE7')
        self.style.map("Back.TButton", background=[('active', main_color)], foreground=[('active', '#67C6E3')])

        self.style.configure("Treeview", font=('Arial', 12))
        self.style.configure("Treeview.Heading", font=('Arial', 14), background='#ACE1AF')
        self.style.map('Treeview', background=[('selected', '#40A2E3')])

        self.style.configure("TFrame", background=main_color)
        
        self.style.map('TCombobox', fieldbackground=[('readonly', 'white')], selectbackground=[('readonly', 'white')], selectforeground=[('readonly', 'blue')])

        self.style.configure('TNotebook.Tab', font=('Arial', 11), background='white', foreground='blue')
        self.style.map('TNotebook.Tab', font=[('selected',('Arial', 14, 'bold'))], background=[('selected', main_color)])
        
        self.style.configure('MainLabel.TLabel', background=main_color, foreground="#074173", font=("Arial", 16, "bold"), anchor="center", justify="center")
        self.style.configure('Normal.TLabel', background=main_color, foreground="#074173", font=("Arial", 14, "bold"), anchor="center", justify="center")

