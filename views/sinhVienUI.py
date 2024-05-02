from tkinter import ttk
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import cv2 as cv
from utils.face import detect_face, match_face, visualize
from utils import db
import config
import threading
import time


class SinhVienUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.cameraCanvas = tk.Canvas(self)
        self.menuFrame = ttk.Frame(self)
        self.diemDanh_btn = ttk.Button(self.menuFrame, text='Điểm danh', command=self.attend)
        self.dangKy_btn = ttk.Button(self.menuFrame, text='Đăng ký', command=self.register)
        self.xem_btn = ttk.Button(self.menuFrame, text= 'Số ngày điểm danh', command=self.xem_btn_click)
        self.back_btn = ttk.Button(self.menuFrame, text="Quay lại", command=lambda: self.master.show_frame(0))

        self.mssv = None
        self.features = None
        self.db_features = db.get_features()
        self.cap = None
        self.isScanning = False
        self.detector = cv.FaceDetectorYN.create(model=f'{config.root_dir}/models/face_detection_yunet_2023mar.onnx',
                                                 input_size=[640, 480], config="", score_threshold=0.7)
        self.sface = cv.FaceRecognizerSF.create(model=f'{config.root_dir}/models/face_recognition_sface_2021dec.onnx',
                                                config="")

        # grid config
        self.grid_columnconfigure(0, weight=8)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)
        for i in range(0, 6):
            self.menuFrame.rowconfigure(i, weight=1)
        self.menuFrame.grid_columnconfigure(0, weight=1)

        # create thread for scanning
        self.start_scan_thread()

    def display(self):
        self.grid(sticky=tk.NSEW)
        self.cameraCanvas.grid(row=0, column=0, sticky=tk.NSEW)
        self.menuFrame.grid(row=0, column=1, sticky=tk.NSEW)
        self.diemDanh_btn.grid(row=0, sticky=tk.NSEW)
        self.dangKy_btn.grid(row=1, sticky=tk.NSEW)
        self.xem_btn.grid(row=2, sticky=tk.NSEW)
        self.back_btn.grid(row=5, sticky=tk.NSEW)
        self.cap = cv.VideoCapture(0)
        self.isScanning = True

    def hide(self):
        for w in (self, self.cameraCanvas, self.menuFrame, self.diemDanh_btn, self.dangKy_btn, self.xem_btn, self.back_btn):
            w.grid_forget()
        self.isScanning = False
        self.cap.release()

    def resize_image(self, image):
        # Lấy kích thước hiện tại của cameraPanel
        panel_width = self.cameraCanvas.winfo_width()
        panel_height = self.cameraCanvas.winfo_height()

        # Tính toán kích thước mới của hình ảnh dựa trên kích thước của cameraPanel
        aspect_ratio = image.width / image.height
        new_width = int(panel_height * aspect_ratio)
        new_height = int(panel_width / aspect_ratio)

        # Chọn kích thước mới phù hợp
        if new_width <= panel_width:
            image = image.resize((new_width, panel_height), Image.LANCZOS)
        else:
            image = image.resize((panel_width, new_height), Image.LANCZOS)
        return image

    def start_scan_thread(self):
        scan_thread = threading.Thread(target=self.scan)
        scan_thread.daemon = True
        scan_thread.start()
            
    def scan(self):
        while True:
            while self.isScanning:
                ret, img = self.cap.read()
                text = "None"
                if ret:
                    detections = detect_face(self.detector, self.sface, img)
                    image_with_boxes = cv.cvtColor(img, cv.COLOR_BGR2RGB)
                    if detections is not None:
                        detected_face, self.features, _ = detections
                        self.mssv = None
                        for id, name, db_features in self.db_features:
                            is_matched = match_face(self.sface, self.features, db_features)
                            if is_matched:
                                self.mssv = id
                                text = f"{self.mssv} - {name}"
                        image_with_boxes = visualize(image_with_boxes, detected_face, text)
                    else:
                        self.features = None
                        self.mssv = None
                    image_with_boxes = Image.fromarray(image_with_boxes)
                    image_with_boxes = self.resize_image(image_with_boxes)
                    imgTk = ImageTk.PhotoImage(image=image_with_boxes)
                    self.cameraCanvas.create_image(0, 0, image=imgTk, anchor=tk.NW)
                    self.cameraCanvas.image = imgTk
                time.sleep(0.01)
            time.sleep(1)
        
    def attend(self):
        self.isScanning = False
        if self.mssv is not None:
            studentName = db.get_student_name(self.mssv)
            ans = messagebox.askyesno('Xác nhận', f'Bạn là {studentName} - {self.mssv} ?')
            if ans is True:
                db.insert_attendance_record(self.mssv)
        self.isScanning = True

    def register(self):
        if self.features is not None:
            self.isScanning = False
            mssv = simpledialog.askstring('Xác nhận đăng ký', 'Vui lòng nhập Mã số sinh viên')
            if mssv is not None:
                db.update_features(mssv, self.features)
                self.db_features = db.get_features()
            self.isScanning = True

    def xem_btn_click(self):
        if self.mssv is not None:
            date = db.get_attendance(self.mssv)
            messagebox.showinfo("Điểm danh", f"Số ngày bạn đã điểm danh: {date} ngày.")
        



         
