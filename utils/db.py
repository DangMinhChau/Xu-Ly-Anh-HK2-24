import sqlite3
import numpy as np
import datetime
import config
from tkinter import messagebox
# Function to create database connection
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(config.database_str)
        return conn
    except sqlite3.Error as err:
        print(err)
    return conn

# Function to create tables if not exists
def create_tables():
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS SINHVIEN(
                    MSSV TEXT PRIMARY KEY NOT NULL,
                    HOTEN TEXT NOT NULL,
                    FEATURES BLOB
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS DIEMDANH(
                    MSSV TEXT,
                    DATE TEXT,
                    TIME TEXT,
                    PRIMARY KEY(MSSV, DATE),
                    FOREIGN KEY(MSSV) REFERENCES SINHVIEN(MSSV)
        )''')
    except sqlite3.Error as err:
        messagebox.showerror("Warning", f"{err.sqlite_errorname}")
    finally:
        conn.close()

# Function to insert a student
def insert_student(MSSV, HOTEN):
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''INSERT INTO SINHVIEN(MSSV, HOTEN) VALUES (?, ?)''', 
                   (MSSV, HOTEN))
        conn.commit()
        print('Student inserted successfully')
    except sqlite3.Error as err:
        messagebox.showerror("Warning", f"{err.sqlite_errorname}")
    finally:
        conn.close()

# Function to retrieve all students
def get_all_students():
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''SELECT * FROM SINHVIEN''')
        rows = cur.fetchall()
        return rows
    except sqlite3.Error as err:
        messagebox.showerror("Warning", f"{err.sqlite_errorname}")
    finally:
        conn.close()

# Function to get student name
def get_student_name(mssv):
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''SELECT HOTEN FROM SINHVIEN WHERE MSSV=?''', (mssv,))
        return cur.fetchone()[0]
    except sqlite3.Error as err:
        messagebox.showerror("Warning", f"{err.sqlite_errorname}")
    finally:
        conn.close()
        
# Function to update a student's features
def update_features(MSSV, features):
    conn = create_connection()
    try: 
        cur = conn.cursor()
        # Serialize the Numpy array to bytes
        cur.execute('''UPDATE SINHVIEN SET FEATURES=? WHERE MSSV=?''', (features.tobytes(), MSSV))
        if cur.rowcount == 0:
            messagebox.showerror("Error", "ID không tồn tại.")
        else:
            messagebox.showinfo("Update face", f'Update thành công - ID: {MSSV}')
        conn.commit()
    except sqlite3.Error as err:
        messagebox.showerror("Warning", f"{err.sqlite_errorname}")
    finally:
        conn.close()

# Function to get all student's features:
    
def get_features():
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''SELECT * FROM SINHVIEN''')
        rows = cur.fetchall()
        features_list = []
        for row in rows:
            MSSV, HOTEN, features_bytes = row
            if features_bytes is not None:
                features_array = np.frombuffer(features_bytes, dtype=np.float32).reshape(1, -1)
                features_list.append((MSSV, HOTEN, features_array))
        return features_list
    except sqlite3.Error as err:
        messagebox.showerror("Warning", f"{err.sqlite_errorname}")
    finally:
        conn.close()

def update_student(MSSV, HOTEN):
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''UPDATE SINHVIEN SET HOTEN=? WHERE MSSV=?''', (HOTEN, MSSV))
        conn.commit()
    except sqlite3.Error as err:
        messagebox.showerror("Warning", f"{err.sqlite_errorname}")
    finally:
        conn.close()
# Function to delete a student
def delete_student(MSSV):
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''DELETE FROM SINHVIEN WHERE MSSV=?''', (MSSV,))
        conn.commit()
    except sqlite3.Error as err:
        messagebox.showerror("Warning", f"{err.sqlite_errorname}")
    finally:
        conn.close()

def insert_attendance_record(MSSV):
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''INSERT INTO DIEMDANH(MSSV, DATE, TIME) VALUES (?, ?, ?)''',
                   (MSSV, datetime.date.today().strftime('%d-%m-%Y'), datetime.datetime.now().time().strftime('%H:%M:%S')))
        conn.commit()
        messagebox.showinfo("Điểm danh", "Điểm danh thành công.")
    except sqlite3.Error as err:
        if err.sqlite_errorcode == 1555:
            messagebox.showwarning("Điểm danh", "Hôm nay bạn đã điểm danh")
    finally:
        conn.close()

def get_attendance_data():
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''SELECT SINHVIEN.MSSV, SINHVIEN.HOTEN, COUNT(DIEMDANH.MSSV) AS Number_of_Attendances
                           FROM SINHVIEN
                           LEFT JOIN DIEMDANH ON SINHVIEN.MSSV = DIEMDANH.MSSV
                           GROUP BY SINHVIEN.MSSV, SINHVIEN.HOTEN''')
        data = cur.fetchall()
        return data
    except sqlite3.Error as err:
        messagebox.showerror("Warning", f"{err.sqlite_errorname}")
    finally:
        conn.close()

def get_attendance(mssv):
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''SELECT COUNT(MSSV) AS Number_of_Attendances
                       FROM DIEMDANH
                       WHERE MSSV = ?''', (mssv,))
        data = cur.fetchone()
        return data[0] if data else 0
    except sqlite3.Error as err:
        messagebox.showerror("Warning", f"{err.sqlite_errorname}")
    finally:
        conn.close()

def get_diemdanh_log():
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''SELECT MSSV, DATE, TIME FROM DIEMDANH ORDER BY MSSV''')
        data = cur.fetchall()
        return data
    except sqlite3.Error as err:
        messagebox.showerror("Warning", f"{err.sqlite_errorname}")
    finally:
        conn.close()
