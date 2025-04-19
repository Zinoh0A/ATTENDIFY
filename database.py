import mysql.connector
from mysql.connector import Error

# Database connection function
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Replace with your MySQL password
            database="face_recognition_system"
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Function to add a student to the database
def add_student(student_data):
    conn = connect_to_database()
    if conn is not None:
        try:
            cursor = conn.cursor()
            sql = """
            INSERT INTO student (Student_id, Dep, Course, Year, Semester, Name, Division, Roll, Gender, Dob, Email, Phone, Address, Teacher, PhotoSample)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, student_data)
            conn.commit()
            print("Student added successfully")
        except Error as e:
            print(f"Error adding student: {e}")
        finally:
            cursor.close()
            conn.close()

# Function to fetch all students from the database
def fetch_students():
    conn = connect_to_database()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM student")
            students = cursor.fetchall()
            return students
        except Error as e:
            print(f"Error fetching students: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

# Function to update a student in the database
def update_student(student_data):
    conn = connect_to_database()
    if conn is not None:
        try:
            cursor = conn.cursor()
            sql = """
            UPDATE student SET Dep=%s, Course=%s, Year=%s, Semester=%s, Name=%s, Division=%s, Roll=%s, Gender=%s, Dob=%s, Email=%s, Phone=%s, Address=%s, Teacher=%s, PhotoSample=%s
            WHERE Student_id=%s
            """
            cursor.execute(sql, student_data)
            conn.commit()
            print("Student updated successfully")
        except Error as e:
            print(f"Error updating student: {e}")
        finally:
            cursor.close()
            conn.close()

# Function to delete a student from the database
def delete_student(student_id):
    conn = connect_to_database()
    if conn is not None:
        try:
            cursor = conn.cursor()
            sql = "DELETE FROM student WHERE Student_id=%s"
            cursor.execute(sql, (student_id,))
            conn.commit()
            print("Student deleted successfully")
        except Error as e:
            print(f"Error deleting student: {e}")
        finally:
            cursor.close()
            conn.close()

# Function to add attendance to the database
def add_attendance(attendance_data):
    conn = connect_to_database()
    if conn is not None:
        try:
            cursor = conn.cursor()
            sql = """
            INSERT INTO attendance (Student_id, Roll, Name, Departement, Time, Date, AttendanceStatus)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, attendance_data)
            conn.commit()
            print("Attendance added successfully")
        except Error as e:
            print(f"Error adding attendance: {e}")
        finally:
            cursor.close()
            conn.close()

# Function to fetch all attendance records from the database
def fetch_attendance():
    conn = connect_to_database()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM attendance")
            attendance_records = cursor.fetchall()
            return attendance_records
        except Error as e:
            print(f"Error fetching attendance: {e}")
            return []
        finally:
            cursor.close()
            conn.close()