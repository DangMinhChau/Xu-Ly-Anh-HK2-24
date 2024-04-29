import sqlite3
import numpy as np
import cv2 as cv
from tkinter import messagebox
# Function to create database connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as err:
        print(err)
    return conn

# Function to create tables if not exists
def create_tables(conn):
    try:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS SINHVIEN(
                    MSSV TEXT PRIMARY KEY NOT NULL,
                    HOTEN TEXT NOT NULL,
                    FEATURES BLOB
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS GIANGVIEN(
                   MSGV TEXT PRIMARY KEY NOT NULL,
                   TEN TEXT NOT NULL
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS LOPHOC(
                   MSLOP TEXT PRIMARY KEY NOT NULL,
                   TENLOP TEXT NOT NULL,
                   MSGV TEXT NOT NULL,
                   FOREIGN KEY (MSGV) REFERENCES GIANGVIEN(MSGV)
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS SINHVIEN_LOPHOC(
                   MSSV TEXT,
                   MSLOP TEXT,
                   PRIMARY KEY (MSSV, MSLOP),
                   FOREIGN KEY (MSSV) REFERENCES SINHVIEN(MSSV),
                   FOREIGN KEY (MSLOP) REFERENCES LOPHOC(MSLOP)
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTs DIEMDANH(
                    MSSV TEXT,
                    MSLOP TEXT,
                    THOIGIAN TIMESTAMP,
                    PRIMARY KEY(MSSV, MSLOP, THOIGIAN),
                    FOREIGN KEY(MSSV) REFERENCES SINHVIEN(MSSV),
                    FOREIGN KEY(MSLOP) REFERENCES LOPHOC(MSLOP)
        )''')
    except sqlite3.Error as err:
        print(err)

# Function to insert a student
def insert_student(conn, MSSV, HOTEN):
    try:
        cur = conn.cursor()
        cur.execute('''INSERT INTO SINHVIEN(MSSV, HOTEN) VALUES (?, ?)''', 
                   (MSSV, HOTEN))
        conn.commit()
        print('Student inserted successfully')
    except sqlite3.Error as err: 
        print(err)

# Function to retrieve all students
def get_all_students(conn):
    try:
        cur = conn.cursor()
        cur.execute('''SELECT * FROM SINHVIEN''')
        rows = cur.fetchall()
        return rows
    except sqlite3.Error as err:
        print(err)

# Function to get student name
def get_student_name(conn, mssv):
    try:
        cur = conn.cursor()
        cur.execute('''SELECT HOTEN FROM SINHVIEN WHERE MSSV=?''', (mssv,))
        return cur.fetchone()[0]
    except sqlite3.Error as err:
        print(err)
        
# Function to update a student's features
def update_features(conn, MSSV, features):
    try: 
        cur = conn.cursor()
        # Serialize the Numpy array to bytes
        cur.execute('''UPDATE SINHVIEN SET FEATURES=? WHERE MSSV=?''', (features.tobytes(), MSSV))
        if cur.rowcount == 0:
            messagebox.showerror("ID không tồn tại.")
        else:
            messagebox.showinfo("Update face", f'Update thành công - ID: {MSSV}')
    finally:
        conn.close()

# Function to get all student's features:
    
def get_features(conn):
    try:
        cur = conn.cursor()
        cur.execute('''SELECT MSSV, FEATURES FROM SINHVIEN''')
        rows = cur.fetchall()
        features_list = []
        for row in rows:
            MSSV, features_bytes = row
            if features_bytes is not None:
                features_array = np.frombuffer(features_bytes, dtype=np.float32).reshape(1, -1)
                features_list.append((MSSV, features_array))
        return features_list
    finally:
        conn.close()

# Function to delete a student
def delete_student(conn, MSSV):
    try:
        cur = conn.cursor()
        cur.execute('''DELETE FROM SINHVIEN WHERE MSSV=?''', (MSSV,))
        conn.commit()
        print('Student deleted successfully')
    except sqlite3.Error as err:
        print(err)

# Function to insert a teacher
def insert_teacher(conn, MSGV, TEN):
    try:
        cur = conn.cursor()
        cur.execute('''INSERT INTO GIANGVIEN(MSGV, TEN) VALUES (?, ?)''', 
                   (MSGV, TEN))
        conn.commit()
        print('Teacher inserted successfully')
    except sqlite3.Error as err: 
        print(err)

# Function to retrieve all teachers
def get_all_teachers(conn):
    try:
        cur = conn.cursor()
        cur.execute('''SELECT * FROM GIANGVIEN''')
        rows = cur.fetchall()
        return rows
    except sqlite3.Error as err:
        print(err)

# Function to update a teacher's information
def update_teacher(conn, MSGV, TEN):
    try:
        cur = conn.cursor()
        cur.execute('''UPDATE GIANGVIEN SET TEN=? WHERE MSGV=?''', (TEN, MSGV))
        conn.commit()
        print('Teacher updated successfully')
    except sqlite3.Error as err:
        print(err)

# Function to delete a teacher
def delete_teacher(conn, MSGV):
    try:
        cur = conn.cursor()
        cur.execute('''DELETE FROM GIANGVIEN WHERE MSGV=?''', (MSGV,))
        conn.commit()
        print('Teacher deleted successfully')
    except sqlite3.Error as err:
        print(err)

# Function to insert a class
def insert_class(conn, MSLOP, TENLOP, MSGV):
    try:
        cur = conn.cursor()
        cur.execute('''INSERT INTO LOPHOC(MSLOP, TENLOP, MSGV) VALUES (?, ?, ?)''', 
                   (MSLOP, TENLOP, MSGV))
        conn.commit()
        print('Class inserted successfully')
    except sqlite3.Error as err: 
        print(err)

# Function to retrieve all classes
def get_all_classes(conn):
    try:
        cur = conn.cursor()
        cur.execute('''SELECT * FROM LOPHOC''')
        rows = cur.fetchall()
        return rows
    except sqlite3.Error as err:
        print(err)

# Function to update a class's information
def update_class(conn, MSLOP, TENLOP, MSGV):
    try:
        cur = conn.cursor()
        cur.execute('''UPDATE LOPHOC SET TENLOP=?, MSGV=? WHERE MSLOP=?''', (TENLOP, MSGV, MSLOP))
        conn.commit()
        print('Class updated successfully')
    except sqlite3.Error as err:
        print(err)

# Function to delete a class
def delete_class(conn, MSLOP):
    try:
        cur = conn.cursor()
        cur.execute('''DELETE FROM LOPHOC WHERE MSLOP=?''', (MSLOP,))
        conn.commit()
        print('Class deleted successfully')
    except sqlite3.Error as err:
        print(err)

# Function to enroll a student in a class
def enroll_student_in_class(conn, MSSV, MSLOP):
    try:
        cur = conn.cursor()
        cur.execute('''INSERT INTO SINHVIEN_LOPHOC(MSSV, MSLOP) VALUES (?, ?)''', 
                   (MSSV, MSLOP))
        conn.commit()
        print('Student enrolled in class successfully')
    except sqlite3.Error as err: 
        print(err)

# Function to withdraw a student from a class
def withdraw_student_from_class(conn, MSSV, MSLOP):
    try:
        cur = conn.cursor()
        cur.execute('''DELETE FROM SINHVIEN_LOPHOC WHERE MSSV=? AND MSLOP=?''', (MSSV, MSLOP))
        conn.commit()
        print('Student withdrawn from class successfully')
    except sqlite3.Error as err:
        print(err)

# Function to get all classes of a student
def get_student_classes(conn, MSSV):
    try:
        cur = conn.cursor()
        cur.execute('''SELECT LOPHOC.* FROM LOPHOC INNER JOIN SINHVIEN_LOPHOC ON LOPHOC.MSLOP = SINHVIEN_LOPHOC.MSLOP WHERE SINHVIEN_LOPHOC.MSSV=?''', (MSSV,))
        rows = cur.fetchall()
        return rows
    except sqlite3.Error as err:
        print(err)

# Function to get all students in a class
def get_class_students(conn, MSLOP):
    try:
        cur = conn.cursor()
        cur.execute('''SELECT SINHVIEN.* FROM SINHVIEN INNER JOIN SINHVIEN_LOPHOC ON SINHVIEN.MSSV = SINHVIEN_LOPHOC.MSSV WHERE SINHVIEN_LOPHOC.MSLOP=?''', (MSLOP,))
        rows = cur.fetchall()
        return rows
    except sqlite3.Error as err:
        print(err)


def insert_attendance_record(conn, MSSV, MSLOP, THOIGIAN):
    try:
        cur = conn.cursor()
        cur.execute('''INSERT INTO DIEMDANH(MSSV, MSLOP, THOIGIAN) VALUES (?, ?, ?)''', 
                   (MSSV, MSLOP, THOIGIAN))
        conn.commit()
        print('Attendance record inserted successfully')
    except sqlite3.Error as err: 
        print(err)

def get_attendance_records(conn, MSSV=None, MSLOP=None):
    try:
        cur = conn.cursor()
        if MSSV is not None and MSLOP is not None:
            cur.execute('''SELECT * FROM DIEMDANH WHERE MSSV=? AND MSLOP=?''', (MSSV, MSLOP))
        elif MSSV is not None:
            cur.execute('''SELECT * FROM DIEMDANH WHERE MSSV=?''', (MSSV,))
        elif MSLOP is not None:
            cur.execute('''SELECT * FROM DIEMDANH WHERE MSLOP=?''', (MSLOP,))
        else:
            cur.execute('''SELECT * FROM DIEMDANH''')
        rows = cur.fetchall()
        return rows
    except sqlite3.Error as err:
        print(err)

def delete_attendance_record(conn, MSSV, MSLOP, THOIGIAN):
    try:
        cur = conn.cursor()
        cur.execute('''DELETE FROM DIEMDANH WHERE MSSV=? AND MSLOP=? AND THOIGIAN=?''', (MSSV, MSLOP, THOIGIAN))
        conn.commit()
        print('Attendance record deleted successfully')
    except sqlite3.Error as err:
        print(err)



#############################################3

if __name__ == '__main__':
    # Create a connection to the database
    conn = create_connection('mydatabase.db')
    # Create tables if not exist
    #create_tables(conn)
    #print('Database and tables created successfully')
    #insert_student(conn, MSSV='20110445', HOTEN='Đặng Minh Châu')
    # Close the database connection
    f = get_features(conn)
    print(type(f))
    print(f)
    if conn is not None:
        conn.close()
