import sqlite3
import numpy as np
import datetime
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

        cur.execute('''CREATE TABLE IF NOT EXISTS DIEMDANH(
                    MSSV TEXT,
                    THOIGIAN TIMESTAMP,
                    PRIMARY KEY(MSSV, THOIGIAN),
                    FOREIGN KEY(MSSV) REFERENCES SINHVIEN(MSSV)
        )''')
    finally:
        conn.close()

# Function to insert a student
def insert_student(conn, MSSV, HOTEN):
    try:
        cur = conn.cursor()
        cur.execute('''INSERT INTO SINHVIEN(MSSV, HOTEN) VALUES (?, ?)''', 
                   (MSSV, HOTEN))
        conn.commit()
        print('Student inserted successfully')
    finally:
        conn.close()

# Function to retrieve all students
def get_all_students(conn):
    try:
        cur = conn.cursor()
        cur.execute('''SELECT * FROM SINHVIEN''')
        rows = cur.fetchall()
        return rows
    finally:
        conn.close()

# Function to get student name
def get_student_name(conn, mssv):
    try:
        cur = conn.cursor()
        cur.execute('''SELECT HOTEN FROM SINHVIEN WHERE MSSV=?''', (mssv,))
        return cur.fetchone()[0]
    finally:
        conn.close()
        
# Function to update a student's features
def update_features(conn, MSSV, features):
    try: 
        cur = conn.cursor()
        # Serialize the Numpy array to bytes
        cur.execute('''UPDATE SINHVIEN SET FEATURES=? WHERE MSSV=?''', (features.tobytes(), MSSV))
        if cur.rowcount == 0:
            messagebox.showerror("Error", "ID không tồn tại.")
        else:
            messagebox.showinfo("Update face", f'Update thành công - ID: {MSSV}')
        conn.commit()
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

def update_student(conn, MSSV, HOTEN):
    try:
        cur = conn.cursor()
        cur.execute('''UPDATE SINHVIEN SET HOTEN=? WHERE MSSV=?''', (HOTEN, MSSV))
        conn.commit()
    finally:
        conn.close()
# Function to delete a student
def delete_student(conn, MSSV):
    try:
        cur = conn.cursor()
        cur.execute('''DELETE FROM SINHVIEN WHERE MSSV=?''', (MSSV,))
        conn.commit()
        print('Student deleted successfully')
    finally:
        conn.close()

def insert_attendance_record(conn, MSSV):
    try:
        cur = conn.cursor()
        cur.execute('''INSERT INTO DIEMDANH(MSSV, THOIGIAN) VALUES (?, ?)''',
                   (MSSV, datetime.date.today()))
        conn.commit()
        print('Attendance record inserted successfully')
    finally:
        conn.close()

def get_attendance_data(conn):
    try:
        cur = conn.cursor()
        cur.execute('''SELECT SINHVIEN.HOTEN, SINHVIEN.MSSV, COUNT(DIEMDANH.MSSV) AS Number_of_Attendances
                           FROM SINHVIEN
                           LEFT JOIN DIEMDANH ON SINHVIEN.MSSV = DIEMDANH.MSSV
                           GROUP BY SINHVIEN.MSSV, SINHVIEN.HOTEN''')
        data = cur.fetchall()
        return data
    except Exception as ex:
        print(ex)
    finally:
        conn.close()

def get_attendance(conn, mssv):
    try:
        cur = conn.cursor()
        cur.execute('''SELECT COUNT(MSSV) AS Number_of_Attendances
                       FROM DIEMDANH
                       WHERE MSSV = ?''', (mssv,))
        data = cur.fetchone()
        return data[0] if data else 0
    finally:
        conn.close()
