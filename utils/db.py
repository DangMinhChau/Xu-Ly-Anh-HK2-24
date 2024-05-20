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
        conn.execute('PRAGMA foreign_keys = ON')
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
                    MSSV TEXT NOT NULL,
                    DATE TEXT NOT NULL,
                    MALOP TEXT NOT NULL,
                    TIME_CHECKIN TEXT NOT NULL,
                    TIME_CHECKOUT TEXT,
                    PRIMARY KEY(MSSV, DATE, MALOP),
                    FOREIGN KEY(MSSV) REFERENCES SINHVIEN(MSSV),
                    FOREIGN KEY(MALOP) REFERENCES LOP(MALOP)
        )''')
        
        cur.execute('''CREATE TABLE IF NOT EXISTS GIANGVIEN(
                    MAGV TEXT PRIMARY KEY NOT NULL,
                    HOTEN TEXT NOT NULL,
                    MATKHAU TEXT NOT NULL DEFAULT 'giangvien'
            )''')
        
        cur.execute('''CREATE TABLE IF NOT EXISTS LOP(
                    MALOP TEXT PRIMARY KEY NOT NULL,
                    TENLOP TEXT NOT NULL,
                    MAGV TEXT,
                    FOREIGN KEY(MAGV) REFERENCES GIANGVIEN(MAGV)
            )''')
        
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS SINHVIEN_LOP(
                    MSSV TEXT NOT NULL,
                    MALOP TEXT, 
                    PRIMARY KEY(MSSV, MALOP),
                    FOREIGN KEY(MSSV) REFERENCES SINHVIEN(MSSV),
                    FOREIGN KEY(MALOP) REFERENCES LOP(MALOP)
                    )
                    ''')
    except sqlite3.Error as err:
        print("SQLite Error: ", err)
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
    except sqlite3.Error as err:
        messagebox.showerror("Warning", f"{err.sqlite_errorname}")
    finally:
        conn.close()

# Function to retrieve all students
def get_all_students():
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''SELECT MSSV, HOTEN,
            CASE
                WHEN FEATURES IS NULL THEN 'No'
                ELSE 'Yes'
            END AS Feature_Status
        FROM SINHVIEN''')
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
    MSSV = str(MSSV)
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
    
def get_features(MALOP):
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''SELECT SINHVIEN.MSSV, SINHVIEN.HOTEN, SINHVIEN.FEATURES
                       FROM SINHVIEN
                       INNER JOIN SINHVIEN_LOP ON SINHVIEN.MSSV = SINHVIEN_LOP.MSSV
                       WHERE SINHVIEN_LOP.MALOP = ?''', (MALOP,))
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

def checkin(MALOP, MSSV):
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''INSERT INTO DIEMDANH(MALOP, MSSV, DATE, TIME_CHECKIN) VALUES (?, ?, ?, ?)''',
                   (MALOP, MSSV, datetime.date.today().strftime('%d-%m-%Y'), datetime.datetime.now().time().strftime('%H:%M:%S')))
        conn.commit()
        print(f'{MSSV} checkin')
    except sqlite3.Error as err:
        messagebox.showwarning("Error", err)
    finally:
        conn.close()

def isCheckin(MALOP, MSSV, date):
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''SELECT COUNT(*) FROM DIEMDANH WHERE MALOP=? AND MSSV = ? AND DATE = ?''', (MALOP, MSSV, date))
        count = cur.fetchone()[0]
        return count > 0  # Returns True if there is at least one record, False otherwise
    except sqlite3.Error as err:
        messagebox.showerror("Warning", f"{err.sqlite_errorname}")
        return False
    finally:
        conn.close()

def checkout(MALOP, MSSV, DATE): 
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''UPDATE DIEMDANH SET TIME_CHECKOUT = ? WHERE MALOP=? AND MSSV=? AND DATE =?''', (datetime.datetime.now().time().strftime('%H:%M:%S'),MALOP, MSSV, DATE))
        conn.commit()
        print(f'{MSSV} checkout')
    except sqlite3.Error as err:
        messagebox.showwarning('err', err)
    finally:
        conn.close()

def get_attendance_data(MALOP):
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''SELECT SV.MSSV, SV.HOTEN, COUNT(DD.MSSV) AS ATTENDANCE_COUNT
            FROM SINHVIEN SV
            JOIN SINHVIEN_LOP SVL ON SV.MSSV = SVL.MSSV
            LEFT JOIN DIEMDANH DD ON SV.MSSV = DD.MSSV AND SVL.MALOP = DD.MALOP
            WHERE SVL.MALOP = ?
            GROUP BY SV.MSSV, SV.HOTEN
            ORDER BY ATTENDANCE_COUNT DESC, SV.MSSV;
        ''', (MALOP,))
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

def get_student_log(MSSV, MALOP):
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''SELECT DD.DATE, DD.TIME_CHECKIN, DD.TIME_CHECKOUT
            FROM SINHVIEN SV
            JOIN DIEMDANH DD ON SV.MSSV = DD.MSSV
            JOIN SINHVIEN_LOP SVL ON SV.MSSV = SVL.MSSV
            WHERE SVL.MALOP = ? AND SV.MSSV = ?
            ORDER BY DD.DATE;
            ''', (MALOP, MSSV))
        data = cur.fetchall()
        return data
    except sqlite3.Error as err:
        messagebox.showerror("Warning", err)
    finally:
        conn.close()

def get_diemdanh_log(MALOP):
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''SELECT SINHVIEN.MSSV, SINHVIEN.HOTEN, DIEMDANH.DATE, DIEMDANH.TIME_CHECKIN, DIEMDANH.TIME_CHECKOUT
        FROM SINHVIEN
        JOIN DIEMDANH ON SINHVIEN.MSSV = DIEMDANH.MSSV
        JOIN LOP ON DIEMDANH.MALOP = LOP.MALOP
        WHERE LOP.MALOP = ?''', (MALOP,))
        data = cur.fetchall()
        return data
    except sqlite3.Error as err:
        messagebox.showerror("Warning", err)
    finally:
        conn.close()

def get_all_teachers():
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''SELECT MAGV, HOTEN FROM GIANGVIEN''')
        data = cur.fetchall()
        return data
    except sqlite3.Error as err:
        messagebox.showerror('Warning', err)
    finally:
        conn.close()
        
def insert_teacher(MAGV, HOTEN):
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''INSERT INTO GIANGVIEN(MAGV, HOTEN) VALUES (?, ?)''', 
                   (MAGV, HOTEN))
        conn.commit()
    except sqlite3.Error as err:
        messagebox.showerror("Warning", f"{err.sqlite_errorname}")
    finally:
        conn.close()

def delete_teacher(MAGV):
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''DELETE FROM GIANGVIEN WHERE MAGV=?''', (MAGV,))
        conn.commit()
    except sqlite3.Error as err:
        messagebox.showerror("Warning", f"{err.sqlite_errorname}")
    finally:
        conn.close()

def update_teacher(MAGV, HOTEN):
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''UPDATE GIANGVIEN SET HOTEN=? WHERE MAGV=?''', (HOTEN, MAGV))
        conn.commit()
    except sqlite3.Error as err:
        messagebox.showerror("Warning", f"{err.sqlite_errorname}")
    finally:
        conn.close()
        
def change_password_teacher(MAGV, NEWPASSWORD):
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''UPDATE GIANGVIEN SET MATKHAU=? WHERE MAGV=?''', (NEWPASSWORD, MAGV))
        conn.commit()
    except sqlite3.Error as err:
        messagebox.showerror("Warning", f"{err.sqlite_errorname}")
    finally:
        conn.close()
        
def get_password(MAGV): 
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''SELECT MATKHAU FROM GIANGVIEN WHERE MAGV=?''', (MAGV,))
        pw = cur.fetchone()
        if pw is not None:
            return pw[0]
        else:
            return None
    except sqlite3.Error as err:
        messagebox.showerror("Warning", f"{err.sqlite_errorname}")
    finally:
        conn.close()
        
def get_all_classes():
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''SELECT LOP.MALOP, LOP.TENLOP, GIANGVIEN.MAGV, GIANGVIEN.HOTEN
                       FROM LOP 
                       LEFT JOIN GIANGVIEN ON LOP.MAGV = GIANGVIEN.MAGV
                       ORDER BY LOP.TENLOP''')
        data = cur.fetchall()
        return data
    except sqlite3.Error as err:
        messagebox.showerror('Warning', err)
    finally:
        conn.close()
        
def get_classes():
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''SELECT MALOP, TENLOP FROM LOP ORDER BY TENLOP''')
        data = cur.fetchall()
        return data
    except sqlite3.Error as err:
        messagebox.showerror('Warning', err)
    finally:
        conn.close()
    
def insert_class(MALOP, TENLOP, MAGV):
    if MAGV== '':
        MAGV=None
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''INSERT INTO LOP(MALOP, TENLOP, MAGV) VALUES (?, ?, ?)''', 
                   (MALOP, TENLOP, MAGV))
        conn.commit()
    except sqlite3.Error as err:
        messagebox.showerror("Warning", f"{err.sqlite_errorname}")
    finally:
        conn.close()

def delete_class(MALOP):
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''DELETE FROM LOP WHERE MALOP=?''', (MALOP,))
        conn.commit()
    except sqlite3.Error as err:
        messagebox.showerror("Warning", f"{err.sqlite_errorname}")
    finally:
        conn.close()
        
def update_class(MALOP, TENLOP, MAGV):
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''UPDATE LOP SET TENLOP=?, MAGV=? WHERE MALOP=?''', (TENLOP, MAGV, MALOP))
        conn.commit()
    except sqlite3.Error as err:
        messagebox.showerror("Warning", f"{err.sqlite_errorname}")
    finally:
        conn.close()

def get_students_of_class(MALOP):
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''SELECT SINHVIEN.MSSV, SINHVIEN.HOTEN
                    FROM SINHVIEN
                    JOIN SINHVIEN_LOP ON SINHVIEN.MSSV = SINHVIEN_LOP.MSSV
                    JOIN LOP ON SINHVIEN_LOP.MALOP = LOP.MALOP
                    WHERE LOP.MALOP =?''', (MALOP,))
        students = cur.fetchall()
        return students
    except sqlite3.Error as err:
        messagebox.showerror('Warning', f'{err.sqlite_errorname}')
    finally:
        conn.close()
        
def get_classes_for_teacher(MAGV):
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''SELECT MALOP, TENLOP FROM LOP WHERE MAGV=?''', (MAGV,))
        classes = cur.fetchall()
        return classes
    except sqlite3.Error as err:
        messagebox.showerror('Warning', f'{err.sqlite_errorname}')
    finally:
        conn.close()
        
def insert_student_class(MALOP, MSSV):
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''INSERT INTO SINHVIEN_LOP(MALOP, MSSV) VALUES (?, ?)''', 
                   (MALOP, MSSV))
        conn.commit()
    except sqlite3.Error as err:
        messagebox.showerror("Warning", f"{err.sqlite_errorname}")
    finally:
        conn.close()

def delete_student_in_class(MALOP, MSSV):
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('''DELETE FROM SINHVIEN_LOP WHERE MALOP=? AND MSSV=?''', (MALOP, MSSV))
        conn.commit()
    except sqlite3.Error as err:
        messagebox.showerror("Warning", f"{err.sqlite_errorname}")
    finally:
        conn.close()
        
