from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk
import cv2 as cv
from utils.face import detect_face, match_face, visualize
from database import db
import os
import config

def create_videoCap(deviceId):
    cap = cv.VideoCapture(deviceId)
    w = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    return (cap, w, h)

cap, w, h = create_videoCap(0)
cap.release()

conn_string = config.database_str
detector = cv.FaceDetectorYN.create(model= f'{config.root_dir}/models/face_detection_yunet_2023mar.onnx', input_size=[w, h], config="", score_threshold=0.92)
sface = cv.FaceRecognizerSF.create(model=f'{config.root_dir}/models/face_recognition_sface_2021dec.onnx', config="")
root_project = os.path.dirname(os.path.abspath(__file__))

class SinhVienUI(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.cameraPanel = ttk.Label(background='red')
        self.menuFrame = ttk.Frame()
        self.diemDanh_btn = ttk.Button(self.menuFrame, text='Điểm danh', command=self.attend)
        self.dangKy_btn = ttk.Button(self.menuFrame, text='Đăng ký', command=self.register)
        self.xem_btn = ttk.Button(self.menuFrame, text= 'Xem')
        
        self.cameraPanel.pack(side= tk.LEFT, expand=True, fill=tk.BOTH)
        self.menuFrame.pack(side=tk.RIGHT, expand=True, fill= tk.BOTH)
        self.diemDanh_btn.pack()
        self.dangKy_btn.pack()
        self.xem_btn.pack()

        self.mssv = None
        self.features = None
        self.cap = None
        self.isCapOpen = False
        self.startScan()
        
    def resize_image(self, image):
        # Lấy kích thước hiện tại của cameraPanel
        panel_width = self.cameraPanel.winfo_width()
        panel_height = self.cameraPanel.winfo_height()

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

    
    def startScan(self):
        features_db = db.get_features(db.create_connection(conn_string))
        self.isCapOpen = True
        def scan():
            ret = False
            if self.isCapOpen is True:
                ret, img = self.cap.read()
            text = "None"
            if ret:
                detections = detect_face(detector, sface, img)
                image_with_boxes = cv.cvtColor(img, cv.COLOR_BGR2RGB)
                if detections is not None:
                    detected_face, self.features, _ = detections
                    self.mssv = None
                    for id, db_features in features_db:
                        is_matched = match_face(sface, self.features, db_features)
                        if is_matched:
                            self.mssv = id
                            text = id
                    image_with_boxes = visualize(image_with_boxes, detected_face, text)
                else:
                    self.features = None
                    self.mssv = None
                image_with_boxes = Image.fromarray(image_with_boxes)
                image_with_boxes = self.resize_image(image_with_boxes)
                imgTk = ImageTk.PhotoImage(image=image_with_boxes)
                self.cameraPanel.img = imgTk
                self.cameraPanel.config(image=imgTk)
            self.cameraPanel.after(25, scan)
                
        if self.cap is None:
            self.cap = cv.VideoCapture(0)
        scan()
        
    def attend(self):
        self.isCapOpen = False
        if self.mssv is not None:
            studentName = db.get_student_name(db.create_connection(conn_string), self.mssv)
            ans = messagebox.askyesno('Xác nhận', f'Bạn là {studentName} - {self.mssv} ?')
            if ans is True:
                ### Code here
                messagebox.showinfo('Điểm danh', 'Điểm danh thành công')
        self.isCapOpen = True
        
        
    def register(self):
        if self.features is not None:
            self.isCapOpen = False
            mssv = simpledialog.askstring('Xác nhận đăng ký', 'Vui lòng nhập Mã số sinh viên')
            if mssv is not None:
                db.update_features(db.create_connection(conn_string), mssv, self.features)
            self.isCapOpen = True

        



         
