import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from .loginUI import LoginUI
from utils import db
from utils.ui import center_window

class HomeUI(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.isLogin = False
        self.style = ttk.Style(self)
        self.panel = tk.Label(self, text='HCMUTE', background="#DFF5FF", foreground="#FF204E", font=("Arial", 40, "bold"))
        self.buttons_frame = ttk.Frame(self)
        self.sinhvien_btn = ttk.Button(self.buttons_frame, text='Sinh viên', style="HomeButton.TButton", takefocus=False, command=self.sinhvien_btn_click)
        self.giangvien_btn = ttk.Button(self.buttons_frame, text='Giảng viên', style="HomeButton.TButton", takefocus=False, command=self.giangvien_btn_click)
        self.admin_btn = ttk.Button(self.buttons_frame, text="Admin", style="HomeButton.TButton", takefocus=False, command=self.admin_btn_click)
        self.info_btn = ttk.Button(self.buttons_frame, text='Thông tin', style="HomeButton.TButton", takefocus=False, command=lambda: self.button_click(4))
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
        self.isLogin = False
        self.grid(row=0, column=0, sticky=tk.NSEW)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=9)
        self.panel.grid(row=0, column=0)

        self.buttons_frame.grid(row=1, column=0, sticky=tk.NSEW)
        self.sinhvien_btn.grid(row=1, sticky=tk.NSEW)
        self.giangvien_btn.grid(row=2, sticky=tk.NSEW)
        self.admin_btn.grid(row=3, sticky=tk.NSEW)
        self.info_btn.grid(row=4, sticky=tk.NSEW)
        self.exit_btn.grid(row=6)

    def hide(self):
        for w in (self,  self.panel, self.buttons_frame, self.sinhvien_btn, self.giangvien_btn, self.admin_btn, self.info_btn, self.exit_btn):
            w.grid_forget()
        
    def button_click(self, frameName):
        self.master.show_frame(frameName)

    def giangvien_btn_click(self):
        loginUI = LoginUI(self.master)
        loginUI.grab_set()

    def admin_btn_click(self):
        password = simpledialog.askstring('Đăng nhập admin', '''Vui lòng nhập mật khẩu        
Mật khẩu mặc định: admin''', show="*")
        if password:
            if(password == 'admin'):
                self.master.show_frame(3)
            else: 
                messagebox.showwarning("Đăng nhập admin", 'Sai mật khẩu!')
            
    
    def sinhvien_btn_click(self):
        def ok_click(self):
            selected_class = classes_cb.get()
            if selected_class:
                self.master.frames[1].current_class = selected_class
                top.destroy()
                self.master.show_frame(1)
            else:
                messagebox.showwarning("Warning", "Vui lòng chọn lớp học")
        top = tk.Toplevel(background="#DFF5FF")
        top.focus()
        top.title("Chọn lớp")
        top.geometry("300x160")
        center_window(top)
        top.grid_rowconfigure(0, weight=1)
        top.grid_rowconfigure(1, weight=1)
        top.grid_columnconfigure(0, weight=1)
        top.grid_columnconfigure(1, weight=1)
        ttk.Label(top, text="Lớp: ", style="Normal.TLabel").grid(row=0, column=0)
        classes_dict = {f"{class_name} - {class_id}": class_id for class_id, class_name in db.get_classes()}
        classes_cb = ttk.Combobox(top, values=list(classes_dict.keys()), state='readonly')
        classes_cb.set("Vui lòng chọn lớp...")
        classes_cb.grid(row=0, column=1)
        classes_cb.focus()
        ttk.Button(top, text="OK", command=lambda self=self: ok_click(self),style="Normal.TButton").grid(row=1, column=0)
        ttk.Button(top, text="Cancel", command= lambda: top.destroy(), style="Normal.TButton").grid(row=1, column=1)
                   
        
        
    def exit(self):
        ans = messagebox.askyesno("Thoát", "Bạn có muốn đóng ứng dụng không?")
        if ans is True:
            self.master.destroy()