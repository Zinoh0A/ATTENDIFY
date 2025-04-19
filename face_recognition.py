from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
from datetime import datetime
import cv2
import os
import time
import threading
import numpy as np
from dlib_face_recognition import DlibFaceRecognition

# Face recognition interface using dlib
class Face_recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1510x770+0+0")
        self.root.title("Face Recognition Attendance System")
        
        # Global variables
        self.marked_students = set()
        self.load_marked_students()
        self.last_recognition_time = {}
        self.recognition_enabled = False
        self.is_running = False
        self.video_thread = None
        self.cap = None
        
        # UI variables
        self.video_frame = None
        self.status_label = None
        self.result_frame = None
        self.recognition_btn = None
        self.stop_btn = None
        
        # Database configuration
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "face_recognition_system"
        }
        
        # Initialize dlib face recognition
        try:
            self.face_recognition = DlibFaceRecognition()
            self.dlib_available = True
        except Exception as e:
            messagebox.showerror("Error", f"Could not initialize facial recognition: {str(e)}")
            self.dlib_available = False
        
        # Create the UI
        self.setup_ui()
        
    def setup_ui(self):
        """Create a modern and user-friendly interface"""
        # Main frame
        main_frame = Frame(self.root, bg="#f0f0f0")
        main_frame.place(x=0, y=0, width=1510, height=770)
        
        # Title with modern style
        title_frame = Frame(main_frame, bg="#3498db")
        title_frame.place(x=0, y=0, width=1510, height=70)
        
        title_lbl = Label(
            title_frame,
            text="Face Recognition Attendance System",
            font=("Helvetica", 28, "bold"),
            bg="#3498db",
            fg="white",
        )
        title_lbl.pack(pady=10)
        
        # Left panel for video
        left_frame = Frame(main_frame, bg="#ffffff", highlightbackground="#dddddd", highlightthickness=1)
        left_frame.place(x=20, y=90, width=720, height=650)
        
        video_label = Label(
            left_frame,
            text="Live Video Feed",
            font=("Helvetica", 16, "bold"),
            bg="#ffffff",
            fg="#333333",
        )
        video_label.pack(pady=10)
        
        # Video frame
        self.video_frame = Label(left_frame, bg="black")
        self.video_frame.place(x=10, y=50, width=700, height=500)
        
        # Recognition status
        status_frame = Frame(left_frame, bg="#ffffff")
        status_frame.place(x=10, y=560, width=700, height=80)
        
        self.status_label = Label(
            status_frame,
            text="Facial Recognition: Disabled",
            font=("Helvetica", 12),
            bg="#ffffff",
            fg="#e74c3c",
        )
        self.status_label.pack(pady=5)
        
        # Control buttons
        button_frame = Frame(status_frame, bg="#ffffff")
        button_frame.pack(pady=5)
        
        self.recognition_btn = Button(
            button_frame,
            text="Start Recognition",
            cursor="hand2",
            command=self.toggle_recognition,
            font=("Helvetica", 12, "bold"),
            bg="#2ecc71",
            fg="white",
            width=25,
            height=1,
            relief=FLAT,
        )
        self.recognition_btn.grid(row=0, column=0, padx=10)
        
        self.stop_btn = Button(
            button_frame,
            text="Stop",
            cursor="hand2",
            command=self.stop_recognition,
            font=("Helvetica", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            width=15,
            height=1,
            relief=FLAT,
            state=DISABLED,
        )
        self.stop_btn.grid(row=0, column=1, padx=10)
        
        # Right panel for results
        right_frame = Frame(main_frame, bg="#ffffff", highlightbackground="#dddddd", highlightthickness=1)
        right_frame.place(x=760, y=90, width=730, height=650)
        
        result_label = Label(
            right_frame,
            text="Recognition Results",
            font=("Helvetica", 16, "bold"),
            bg="#ffffff",
            fg="#333333",
        )
        result_label.pack(pady=10)
        
        # Results display frame
        self.result_frame = Frame(right_frame, bg="#f9f9f9")
        self.result_frame.place(x=10, y=50, width=710, height=580)
        
        # Initial info
        info_label = Label(
            self.result_frame,
            text="Waiting for facial recognition...",
            font=("Helvetica", 14),
            bg="#f9f9f9",
            fg="#7f8c8d",
        )
        info_label.pack(pady=250)
        
    def load_marked_students(self):
        """Load students already marked present from CSV file"""
        self.marked_students = set()
        today_date = datetime.now().strftime("%d/%m/%Y")
        
        try:
            if os.path.exists("attendance.csv"):
                with open("attendance.csv", "r") as f:
                    for line in f.readlines():
                        if line.strip():
                            parts = line.strip().split(",")
                            if len(parts) >= 6 and parts[7] == today_date:  # Check date column
                                key = f"{parts[0]}_{today_date}"
                                self.marked_students.add(key)  # Format: "ID_date"
        except Exception as e:
            print(f"Error loading marked students: {str(e)}")
            
    def mark_attendance(self, student_id, gender, name, dep, course=None, year=None, semester=None, division=None):
        """Mark a student's attendance"""
        # Check if already marked today
        today_date = datetime.now().strftime("%d/%m/%Y")
        key = f"{student_id}_{today_date}"
        
        if key not in self.marked_students:
            try:
                # Create file if it doesn't exist
                if not os.path.exists("attendance.csv"):
                    with open("attendance.csv", "w", newline="\n") as f:
                        f.write("ID,Gender,Name,Department,Course,Year,Time,Date,Status\n")
                
                # Open file in append mode
                with open("attendance.csv", "a+", newline="\n") as f:
                    now = datetime.now()
                    date_str = now.strftime("%d/%m/%Y")
                    time_str = now.strftime("%H:%M:%S")
                    
                    # Include additional information if available
                    if course and year and semester and division:
                        f.write(f"{student_id},{gender},{name},{dep},{course},{year},{time_str},{date_str},Present\n")
                    else:
                        f.write(f"{student_id},{gender},{name},{dep},N/A,N/A,{time_str},{date_str},Present\n")
                
                # Add to set of marked students
                self.marked_students.add(key)
                return True
            except Exception as e:
                print(f"Error marking attendance: {str(e)}")
                return False
        return False
        
    def toggle_recognition(self):
        """Enable/disable facial recognition"""
        if not self.is_running:
            self.start_recognition()
        else:
            self.recognition_enabled = not self.recognition_enabled
            status_text = "Enabled" if self.recognition_enabled else "Disabled"
            status_color = "#2ecc71" if self.recognition_enabled else "#e74c3c"
            self.status_label.config(text=f"Facial Recognition: {status_text}", fg=status_color)
            
    def start_recognition(self):
        """Start facial recognition process in a separate thread"""
        if not self.is_running:
            # Check if dlib is available
            if not self.dlib_available:
                messagebox.showerror("Error", "The dlib facial recognition system is not available")
                return
                
            self.is_running = True
            self.recognition_enabled = True
            self.status_label.config(text="Facial Recognition: Enabled", fg="#2ecc71")
            self.recognition_btn.config(text="Pause/Resume", bg="#3498db")
            self.stop_btn.config(state=NORMAL)
            
            # Start recognition in a separate thread
            self.video_thread = threading.Thread(target=self.face_recog_dlib)
            self.video_thread.daemon = True
            self.video_thread.start()
            
    def stop_recognition(self):
        """Stop facial recognition process"""
        self.is_running = False
        self.recognition_enabled = False
        self.status_label.config(text="Facial Recognition: Disabled", fg="#e74c3c")
        self.recognition_btn.config(text="Start Recognition", bg="#2ecc71")
        self.stop_btn.config(state=DISABLED)
        
        # Close camera if open
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
            self.cap = None
        
        # Reset video display
        blank_image = Image.new('RGB', (700, 500), color='black')
        blank_photo = ImageTk.PhotoImage(blank_image)
        self.video_frame.config(image=blank_photo)
        self.video_frame.image = blank_photo
        
        # Reset results display
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        info_label = Label(
            self.result_frame,
            text="Waiting for facial recognition...",
            font=("Helvetica", 14),
            bg="#f9f9f9",
            fg="#7f8c8d",
        )
        info_label.pack(pady=250)
        
    def update_result_display(self, student_id, name, gender, dep, course=None, year=None, semester=None, is_marked=False, confidence=None):
        """Update recognition results display"""
        # Clear existing widgets
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        # Create a styled frame for student info
        student_info = Frame(self.result_frame, bg="#f9f9f9")
        student_info.pack(pady=20, fill=BOTH, expand=True)
        
        # Recognition success icon
        success_frame = Frame(student_info, bg="#f9f9f9")
        success_frame.pack(pady=20)
        
        success_label = Label(
            success_frame,
            text="✓ RECOGNITION SUCCESSFUL",
            font=("Helvetica", 18, "bold"),
            bg="#f9f9f9",
            fg="#2ecc71",
        )
        success_label.pack()
        
        # Confidence display if available
        if confidence is not None:
            conf_label = Label(
                success_frame,
                text=f"Confidence: {confidence}%",
                font=("Helvetica", 14),
                bg="#f9f9f9",
                fg="#333333",
            )
            conf_label.pack(pady=5)
        
        # Student information
        info_frame = Frame(student_info, bg="#f9f9f9")
        info_frame.pack(pady=20, padx=50, fill=X)
        
        # Style for labels and values
        label_font = ("Helvetica", 14)
        value_font = ("Helvetica", 14, "bold")
        
        # Student ID
        id_frame = Frame(info_frame, bg="#f9f9f9")
        id_frame.pack(fill=X, pady=10)
        
        id_label = Label(
            id_frame,
            text="Student ID:",
            font=label_font,
            width=15,
            anchor=W,
            bg="#f9f9f9",
            fg="#333333",
        )
        id_label.pack(side=LEFT)
        
        id_value = Label(
            id_frame,
            text=student_id,
            font=value_font,
            bg="#f9f9f9",
            fg="#333333",
        )
        id_value.pack(side=LEFT)
        
        # Student name
        name_frame = Frame(info_frame, bg="#f9f9f9")
        name_frame.pack(fill=X, pady=10)
        
        name_label = Label(
            name_frame,
            text="Name:",
            font=label_font,
            width=15,
            anchor=W,
            bg="#f9f9f9",
            fg="#333333",
        )
        name_label.pack(side=LEFT)
        
        name_value = Label(
            name_frame,
            text=name,
            font=value_font,
            bg="#f9f9f9",
            fg="#333333",
        )
        name_value.pack(side=LEFT)
        
        # Gender (if available)
        if gender and gender != "N/A":
            gender_frame = Frame(info_frame, bg="#f9f9f9")
            gender_frame.pack(fill=X, pady=10)
            
            gender_label = Label(
                gender_frame,
                text="Gender:",
                font=label_font,
                width=15,
                anchor=W,
                bg="#f9f9f9",
                fg="#333333",
            )
            gender_label.pack(side=LEFT)
            
            gender_value = Label(
                gender_frame,
                text=gender,
                font=value_font,
                bg="#f9f9f9",
                fg="#333333",
            )
            gender_value.pack(side=LEFT)
        
        # Department
        dep_frame = Frame(info_frame, bg="#f9f9f9")
        dep_frame.pack(fill=X, pady=10)
        
        dep_label = Label(
            dep_frame,
            text="Department:",
            font=label_font,
            width=15,
            anchor=W,
            bg="#f9f9f9",
            fg="#333333",
        )
        dep_label.pack(side=LEFT)
        
        dep_value = Label(
            dep_frame,
            text=dep,
            font=value_font,
            bg="#f9f9f9",
            fg="#333333",
        )
        dep_value.pack(side=LEFT)
        
        # Course (if available)
        if course and course != "N/A":
            course_frame = Frame(info_frame, bg="#f9f9f9")
            course_frame.pack(fill=X, pady=10)
            
            course_label = Label(
                course_frame,
                text="Course:",
                font=label_font,
                width=15,
                anchor=W,
                bg="#f9f9f9",
                fg="#333333",
            )
            course_label.pack(side=LEFT)
            
            course_value = Label(
                course_frame,
                text=course,
                font=value_font,
                bg="#f9f9f9",
                fg="#333333",
            )
            course_value.pack(side=LEFT)
            
        # Year (if available)
        if year and year != "N/A":
            year_frame = Frame(info_frame, bg="#f9f9f9")
            year_frame.pack(fill=X, pady=10)
            
            year_label = Label(
                year_frame,
                text="Year:",
                font=label_font,
                width=15,
                anchor=W,
                bg="#f9f9f9",
                fg="#333333",
            )
            year_label.pack(side=LEFT)
            
            year_value = Label(
                year_frame,
                text=year,
                font=value_font,
                bg="#f9f9f9",
                fg="#333333",
            )
            year_value.pack(side=LEFT)
            
        # Attendance status
        status_frame = Frame(info_frame, bg="#f9f9f9")
        status_frame.pack(fill=X, pady=10)
        
        status_label = Label(
            status_frame,
            text="Status:",
            font=label_font,
            width=15,
            anchor=W,
            bg="#f9f9f9",
            fg="#333333",
        )
        status_label.pack(side=LEFT)
        
        status_text = "Attendance Marked" if is_marked else "Already Marked"
        status_color = "#2ecc71" if is_marked else "#e67e22"
        
        status_value = Label(
            status_frame,
            text=status_text,
            font=value_font,
            bg="#f9f9f9",
            fg=status_color,
        )
        status_value.pack(side=LEFT)
        
        # Timestamp
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%d/%m/%Y")
        
        time_frame = Frame(info_frame, bg="#f9f9f9")
        time_frame.pack(fill=X, pady=10)
        
        time_label = Label(
            time_frame,
            text="Timestamp:",
            font=label_font,
            width=15,
            anchor=W,
            bg="#f9f9f9",
            fg="#333333",
        )
        time_label.pack(side=LEFT)
        
        time_value = Label(
            time_frame,
            text=f"{time_str} - {date_str}",
            font=value_font,
            bg="#f9f9f9",
            fg="#333333",
        )
        time_value.pack(side=LEFT)
    
    def update_unknown_display(self):
        """Display when an unknown person is detected"""
        # Clear existing widgets
        for widget in self.result_frame.winfo_children():
            widget.destroy()
            
        # Create a styled frame for unknown info
        unknown_info = Frame(self.result_frame, bg="#f9f9f9")
        unknown_info.pack(pady=20, fill=BOTH, expand=True)
        
        # Unknown icon
        unknown_frame = Frame(unknown_info, bg="#f9f9f9")
        unknown_frame.pack(pady=20)
        
        unknown_label = Label(
            unknown_frame,
            text="❓ UNKNOWN PERSON",
            font=("Helvetica", 18, "bold"),
            bg="#f9f9f9",
            fg="#e74c3c",
        )
        unknown_label.pack()
        
        # Message
        message_label = Label(
            unknown_info,
            text="This person is not registered in the system.",
            font=("Helvetica", 14),
            bg="#f9f9f9",
            fg="#333333",
        )
        message_label.pack(pady=20)
        
        # Timestamp
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%d/%m/%Y")
        
        time_label = Label(
            unknown_info,
            text=f"Detected at: {time_str} - {date_str}",
            font=("Helvetica", 12),
            bg="#f9f9f9",
            fg="#666666",
        )
        time_label.pack(pady=10)
        
    def get_student_info(self, student_id):
        """Get student information from MySQL database"""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Modified query to match database structure
            query = "SELECT Name, Gender, Dep, Course, Year, Semester, Division FROM student WHERE Student_id = %s"
            cursor.execute(query, (student_id,))
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if result:
                return {
                    "id": student_id,
                    "name": result[0],
                    "gender": result[1],
                    "dep": result[2],
                    "course": result[3],
                    "year": result[4],
                    "semester": result[5],
                    "division": result[6]
                }
            return None
        except Exception as e:
            print(f"Error retrieving student information: {str(e)}")
            messagebox.showerror("Database Error", f"Unable to retrieve information: {str(e)}")
            return None
        
    def face_recog_dlib(self):
        """Main facial recognition function using dlib"""
        # Check if dlib is available
        if not self.dlib_available:
            messagebox.showerror("Error", "The dlib facial recognition system is not available")
            self.stop_recognition()
            return
        
        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        
        # Check if camera is open
        if not self.cap.isOpened():
            # Try another camera index
            self.cap = cv2.VideoCapture(1)
            if not self.cap.isOpened():
                # Last attempt with explicit options
                self.cap = cv2.VideoCapture(0, cv2.CAP_ANY)
                if not self.cap.isOpened():
                    messagebox.showerror("Camera Error", "Cannot access camera. Please check that the camera is connected.")
                    self.stop_recognition()
                    return
        
        # Set camera resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        print("Camera initialized successfully")
        
        # Main recognition loop
        while self.is_running:
            try:
                if not self.recognition_enabled:
                    # If recognition is paused, just show video feed without recognition
                    ret, frame = self.cap.read()
                    if ret:
                        frame = cv2.flip(frame, 1)  # Horizontal mirror
                        # Convert for Tkinter display
                        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        img = Image.fromarray(rgb_frame)
                        img = img.resize((700, 500), Image.LANCZOS)
                        imgtk = ImageTk.PhotoImage(image=img)
                        
                        # Update UI in the main thread
                        self.root.after(0, lambda: self.update_video_display(imgtk))
                    time.sleep(0.03)  # Reduce CPU usage
                    continue
                
                ret, frame = self.cap.read()
                if not ret:
                    print("Error reading from camera")
                    time.sleep(0.1)
                    continue
                
                # Horizontal mirror for more natural view
                frame = cv2.flip(frame, 1)
                
                # Make a copy for display
                display_frame = frame.copy()
                
                # Recognize faces using dlib
                face_ids, face_locations, confidences = self.face_recognition.recognize_faces(frame)
                
                # Process each detected face
                for i, (face_id, face_loc, confidence) in enumerate(zip(face_ids, face_locations, confidences)):
                    # Draw rectangle around face
                    top, right, bottom, left = face_loc
                    cv2.rectangle(display_frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    
                    # Display ID and confidence
                    text = f"ID: {face_id} ({confidence}%)"
                    cv2.putText(display_frame, text, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    
                    # If not unknown, mark attendance
                    if face_id != "Unknown":
                        # Limit recognition frequency for the same student
                        current_time = time.time()
                        if face_id not in self.last_recognition_time or (current_time - self.last_recognition_time[face_id] > 5):
                            # Get student info
                            student_info = self.get_student_info(face_id)
                            
                            if student_info:
                                # Mark attendance
                                is_marked = self.mark_attendance(
                                    student_info["id"],
                                    student_info["gender"],
                                    student_info["name"],
                                    student_info["dep"],
                                    student_info["course"],
                                    student_info["year"],
                                    student_info["semester"],
                                    student_info["division"]
                                )
                                
                                # Create local copies for lambda
                                student_id_copy = student_info["id"]
                                name_copy = student_info["name"]
                                gender_copy = student_info["gender"]
                                dep_copy = student_info["dep"]
                                course_copy = student_info["course"]
                                year_copy = student_info["year"]
                                semester_copy = student_info["semester"]
                                is_marked_copy = is_marked
                                confidence_copy = confidence
                                
                                # Update results display in main thread
                                self.root.after(0, lambda: self.update_result_display(
                                    student_id_copy, name_copy, gender_copy, dep_copy, 
                                    course_copy, year_copy, semester_copy, is_marked_copy, confidence_copy))
                                
                                # Update last recognition time
                                self.last_recognition_time[face_id] = current_time
                    else:
                        # Display unknown person
                        self.root.after(0, self.update_unknown_display)
                
                # Convert image for Tkinter display
                rgb_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb_frame)
                img = img.resize((700, 500), Image.LANCZOS)
                imgtk = ImageTk.PhotoImage(image=img)
                
                # Update UI in main thread
                self.root.after(0, lambda: self.update_video_display(imgtk))
                
                # Small delay to avoid CPU overload
                time.sleep(0.03)
            
            except Exception as e:
                print(f"Error in recognition loop: {str(e)}")
                time.sleep(0.1)
        
        # Release camera resources
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
        print("Facial recognition stopped")

    def update_video_display(self, img_tk):
        """Update video display safely"""
        self.video_frame.config(image=img_tk)
        self.video_frame.image = img_tk  # Keep a reference to avoid garbage collection

if __name__ == "__main__":
    root = Tk()
    app = Face_recognition(root)
    root.mainloop()