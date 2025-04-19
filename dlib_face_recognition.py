import cv2
import dlib
import numpy as np
import os
from datetime import datetime
import mysql.connector
from imutils import face_utils
from tkinter import messagebox
import pickle

class DlibFaceRecognition:
    def __init__(self):
        """Initialize the dlib face recognition system"""
        self.models_path = "pretrained_model"
        
        # Create directory for models if it doesn't exist
        os.makedirs(self.models_path, exist_ok=True)
        
        # Known faces will be stored here
        self.known_faces_dir = "known_faces"
        os.makedirs(self.known_faces_dir, exist_ok=True)
        
        # Path for encodings
        self.encodings_path = os.path.join(self.models_path, "encodings.pickle")
        
        # Load pretrained models
        try:
            print('[INFO] Loading pretrained dlib models...')
            self.pose_predictor = dlib.shape_predictor(os.path.join(self.models_path, "shape_predictor_68_face_landmarks.dat"))
            self.face_encoder = dlib.face_recognition_model_v1(os.path.join(self.models_path, "dlib_face_recognition_resnet_model_v1.dat"))
            self.face_detector = dlib.get_frontal_face_detector()
            print('[INFO] Models loaded successfully')
            
            # Load existing encodings if available
            self.known_face_encodings = []
            self.known_face_ids = []
            self.load_encodings()
            
        except Exception as e:
            print(f"[ERROR] Could not load dlib models: {str(e)}")
            raise Exception(f"Failed to load dlib models: {str(e)}")
    
    def load_encodings(self):
        """Load existing face encodings from pickle file"""
        if os.path.exists(self.encodings_path):
            try:
                with open(self.encodings_path, "rb") as f:
                    data = pickle.load(f)
                    self.known_face_encodings = data.get("encodings", [])
                    self.known_face_ids = data.get("ids", [])
                print(f"[INFO] Loaded {len(self.known_face_encodings)} face encodings")
            except Exception as e:
                print(f"[ERROR] Failed to load encodings: {str(e)}")
                # Initialize as empty if loading fails
                self.known_face_encodings = []
                self.known_face_ids = []
        else:
            # Initialize as empty if file doesn't exist
            self.known_face_encodings = []
            self.known_face_ids = []
    
    def save_encodings(self):
        """Save face encodings to pickle file"""
        try:
            data = {
                "encodings": self.known_face_encodings,
                "ids": self.known_face_ids
            }
            with open(self.encodings_path, "wb") as f:
                pickle.dump(data, f)
            print(f"[INFO] Saved {len(self.known_face_encodings)} face encodings")
        except Exception as e:
            print(f"[ERROR] Failed to save encodings: {str(e)}")
    
    def transform_rect(self, image, face_location):
        """Convert dlib rectangle to coordinates (top, right, bottom, left)"""
        rect = face_location.top(), face_location.right(), face_location.bottom(), face_location.left()
        # Ensure coordinates are within image bounds
        coord_face = max(rect[0], 0), min(rect[1], image.shape[1]), min(rect[2], image.shape[0]), max(rect[3], 0)
        return coord_face
    
    def encode_face(self, image):
        """Detect faces in an image and compute their encodings"""
        # Convert to RGB if needed (dlib expects RGB images)
        if len(image.shape) == 3 and image.shape[2] == 3:
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            rgb_image = image
        
        # Detect faces
        face_locations = self.face_detector(rgb_image, 1)
        
        face_encodings_list = []
        face_locations_list = []
        
        for face_location in face_locations:
            # Get facial landmarks
            shape = self.pose_predictor(rgb_image, face_location)
            
            # Compute face encoding
            face_encoding = self.face_encoder.compute_face_descriptor(rgb_image, shape)
            
            # Convert to numpy array for easier processing
            face_encoding_np = np.array(face_encoding)
            
            face_encodings_list.append(face_encoding_np)
            face_locations_list.append(self.transform_rect(rgb_image, face_location))
        
        return face_encodings_list, face_locations_list
    
    def add_face(self, image, student_id):
        """Add a face to the known faces database"""
        face_encodings, face_locations = self.encode_face(image)
        
        if not face_encodings:
            return False, "No face detected in the image"
        
        if len(face_encodings) > 1:
            return False, "Multiple faces detected in the image. Please use an image with only one face."
        
        # Check if this student_id already exists
        if student_id in self.known_face_ids:
            # Update existing encoding
            idx = self.known_face_ids.index(student_id)
            self.known_face_encodings[idx] = face_encodings[0]
            # Save to disk
            self.save_encodings()
            
            # Also save the image for reference
            os.makedirs(os.path.join(self.known_faces_dir, str(student_id)), exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_filename = os.path.join(self.known_faces_dir, str(student_id), f"{timestamp}.jpg")
            cv2.imwrite(image_filename, image)
            
            return True, f"Updated face encoding for student ID: {student_id}"
        else:
            # Add new encoding
            self.known_face_encodings.append(face_encodings[0])
            self.known_face_ids.append(student_id)
            # Save to disk
            self.save_encodings()
            
            # Also save the image for reference
            os.makedirs(os.path.join(self.known_faces_dir, str(student_id)), exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_filename = os.path.join(self.known_faces_dir, str(student_id), f"{timestamp}.jpg")
            cv2.imwrite(image_filename, image)
            
            return True, f"Added new face encoding for student ID: {student_id}"
    
    def recognize_faces(self, image, tolerance=0.6):
        """Recognize faces in an image and return their IDs"""
        face_encodings, face_locations = self.encode_face(image)
        face_ids = []
        confidence_values = []
        
        for face_encoding in face_encodings:
            if len(self.known_face_encodings) == 0:
                face_ids.append("Unknown")
                confidence_values.append(0)
                continue
                
            # Calculate distances to all known faces
            face_distances = np.linalg.norm(np.array(self.known_face_encodings) - face_encoding, axis=1)
            
            # Find the closest match
            best_match_index = np.argmin(face_distances)
            best_match_distance = face_distances[best_match_index]
            
            # Calculate confidence (inverse of distance)
            confidence = max(0, min(100, int((1 - best_match_distance) * 100)))
            
            if best_match_distance <= tolerance:
                face_ids.append(self.known_face_ids[best_match_index])
            else:
                face_ids.append("Unknown")
            
            confidence_values.append(confidence)
        
        return face_ids, face_locations, confidence_values
    
    def get_student_info_by_id(self, student_id, db_config):
        """Get student information from the database"""
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            
            # Modified query to match your database structure
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
            print(f"[ERROR] Database query failed: {str(e)}")
            return None
    
    def mark_attendance(self, student_info, attendance_file="attendance.csv"):
        """Mark attendance for a recognized student"""
        # Check if student is already marked present today
        today_date = datetime.now().strftime("%d/%m/%Y")
        key = f"{student_info['id']}_{today_date}"
        
        marked_students = set()
        
        # Load existing attendance records
        try:
            if os.path.exists(attendance_file):
                with open(attendance_file, "r") as f:
                    for line in f.readlines():
                        if line.strip():
                            parts = line.strip().split(",")
                            if len(parts) >= 6 and parts[7] == today_date:  # Check date column
                                attendance_key = f"{parts[0]}_{today_date}"
                                marked_students.add(attendance_key)
        except Exception as e:
            print(f"[ERROR] Failed to load attendance: {str(e)}")
        
        # If student is not already marked, mark attendance
        if key not in marked_students:
            try:
                # Create file if it doesn't exist
                if not os.path.exists(attendance_file):
                    with open(attendance_file, "w", newline="") as f:
                        f.write("ID,Gender,Name,Department,Course,Year,Time,Date,Status\n")
                
                # Append attendance record
                with open(attendance_file, "a+", newline="") as f:
                    now = datetime.now()
                    date_str = now.strftime("%d/%m/%Y")
                    time_str = now.strftime("%H:%M:%S")
                    
                    # Format based on available info
                    course = student_info.get("course", "N/A")
                    year = student_info.get("year", "N/A")
                    
                    f.write(f"{student_info['id']},{student_info['gender']},{student_info['name']},"
                            f"{student_info['dep']},{course},{year},{time_str},{date_str},Present\n")
                
                marked_students.add(key)
                return True, f"Marked attendance for {student_info['name']}"
            except Exception as e:
                print(f"[ERROR] Failed to mark attendance: {str(e)}")
                return False, f"Failed to mark attendance: {str(e)}"
        else:
            return False, f"{student_info['name']} already marked present today"

# Example usage:
# face_recognition = DlibFaceRecognition()
# 
# # To add a new face:
# # success, message = face_recognition.add_face(image, student_id)
# 
# # To recognize faces:
# # ids, locations, confidences = face_recognition.recognize_faces(image)