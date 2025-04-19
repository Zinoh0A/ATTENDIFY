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

# Interface de reconnaissance faciale améliorée
class Face_recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1510x770+0+0")
        self.root.title("Système de Présence par Reconnaissance Faciale")
        
        # Variables globales
        self.marked_students = set()
        self.load_marked_students()
        self.last_recognition_time = {}
        self.recognition_enabled = False
        self.is_running = False
        self.video_thread = None
        self.cap = None
        
        # Variables pour l'interface utilisateur
        self.video_frame = None
        self.status_label = None
        self.result_frame = None
        self.recognition_btn = None
        self.stop_btn = None
        
        # Configuration de la base de données
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "face_recognition_system"
        }
        
        # Créer l'interface utilisateur
        self.setup_ui()
        
    def setup_ui(self):
        """Créer une interface utilisateur moderne et conviviale"""
        # Cadre principal
        main_frame = Frame(self.root, bg="#f0f0f0")
        main_frame.place(x=0, y=0, width=1510, height=770)
        
        # Titre avec style moderne
        title_frame = Frame(main_frame, bg="#3498db")
        title_frame.place(x=0, y=0, width=1510, height=70)
        
        title_lbl = Label(
            title_frame,
            text="Système de Présence par Reconnaissance Faciale",
            font=("Helvetica", 28, "bold"),
            bg="#3498db",
            fg="white",
        )
        title_lbl.pack(pady=10)
        
        # Panneau gauche pour la vidéo
        left_frame = Frame(main_frame, bg="#ffffff", highlightbackground="#dddddd", highlightthickness=1)
        left_frame.place(x=20, y=90, width=720, height=650)
        
        video_label = Label(
            left_frame,
            text="Flux Vidéo en Direct",
            font=("Helvetica", 16, "bold"),
            bg="#ffffff",
            fg="#333333",
        )
        video_label.pack(pady=10)
        
        # Cadre pour le flux vidéo
        self.video_frame = Label(left_frame, bg="black")
        self.video_frame.place(x=10, y=50, width=700, height=500)
        
        # Statut de la reconnaissance
        status_frame = Frame(left_frame, bg="#ffffff")
        status_frame.place(x=10, y=560, width=700, height=80)
        
        self.status_label = Label(
            status_frame,
            text="Reconnaissance Faciale : Désactivée",
            font=("Helvetica", 12),
            bg="#ffffff",
            fg="#e74c3c",
        )
        self.status_label.pack(pady=5)
        
        # Boutons de contrôle
        button_frame = Frame(status_frame, bg="#ffffff")
        button_frame.pack(pady=5)
        
        self.recognition_btn = Button(
            button_frame,
            text="Démarrer la Reconnaissance",
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
            text="Arrêter",
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
        
        # Panneau droit pour les résultats
        right_frame = Frame(main_frame, bg="#ffffff", highlightbackground="#dddddd", highlightthickness=1)
        right_frame.place(x=760, y=90, width=730, height=650)
        
        result_label = Label(
            right_frame,
            text="Résultats de la Reconnaissance",
            font=("Helvetica", 16, "bold"),
            bg="#ffffff",
            fg="#333333",
        )
        result_label.pack(pady=10)
        
        # Cadre pour afficher les résultats de reconnaissance
        self.result_frame = Frame(right_frame, bg="#f9f9f9")
        self.result_frame.place(x=10, y=50, width=710, height=580)
        
        # Information initiale
        info_label = Label(
            self.result_frame,
            text="En attente de la reconnaissance faciale...",
            font=("Helvetica", 14),
            bg="#f9f9f9",
            fg="#7f8c8d",
        )
        info_label.pack(pady=250)
        
    def load_marked_students(self):
        """Charger les étudiants déjà marqués présents depuis le fichier CSV"""
        self.marked_students = set()
        today_date = datetime.now().strftime("%d/%m/%Y")
        
        try:
            if os.path.exists("attendance.csv"):
                with open("attendance.csv", "r") as f:
                    for line in f.readlines():
                        if line.strip():
                            parts = line.strip().split(",")
                            if len(parts) >= 6 and parts[5] == today_date:  # Vérifier la date
                                key = f"{parts[0]}_{today_date}"
                                self.marked_students.add(key)  # Format: "ID_date"
        except Exception as e:
            print(f"Erreur lors du chargement des étudiants marqués: {str(e)}")
            
    def mark_attendance(self, student_id, gender, name, dep, course=None, year=None, semester=None, division=None):
        """Marquer la présence d'un étudiant"""
        # Vérifier si déjà marqué aujourd'hui
        today_date = datetime.now().strftime("%d/%m/%Y")
        key = f"{student_id}_{today_date}"
        
        if key not in self.marked_students:
            try:
                # Créer le fichier s'il n'existe pas
                if not os.path.exists("attendance.csv"):
                    with open("attendance.csv", "w", newline="\n") as f:
                        f.write("ID,Gender,Name,Department,Course,Year,Time,Date,Status\n")
                
                # Ouvrir le fichier en mode ajout
                with open("attendance.csv", "a+", newline="\n") as f:
                    now = datetime.now()
                    date_str = now.strftime("%d/%m/%Y")
                    time_str = now.strftime("%H:%M:%S")
                    
                    # Inclure les informations supplémentaires si disponibles
                    if course and year and semester and division:
                        f.write(f"{student_id},{gender},{name},{dep},{course},{year},{time_str},{date_str},Present\n")
                    else:
                        f.write(f"{student_id},{gender},{name},{dep},N/A,N/A,{time_str},{date_str},Present\n")
                
                # Ajouter à l'ensemble des étudiants marqués
                self.marked_students.add(key)
                return True
            except Exception as e:
                print(f"Erreur lors du marquage de présence: {str(e)}")
                return False
        return False
        
    def toggle_recognition(self):
        """Activer/désactiver la reconnaissance faciale"""
        if not self.is_running:
            self.start_recognition()
        else:
            self.recognition_enabled = not self.recognition_enabled
            status_text = "Activée" if self.recognition_enabled else "Désactivée"
            status_color = "#2ecc71" if self.recognition_enabled else "#e74c3c"
            self.status_label.config(text=f"Reconnaissance Faciale : {status_text}", fg=status_color)
            
    def start_recognition(self):
        """Démarrer le processus de reconnaissance faciale dans un thread séparé"""
        if not self.is_running:
            self.is_running = True
            self.recognition_enabled = True
            self.status_label.config(text="Reconnaissance Faciale : Activée", fg="#2ecc71")
            self.recognition_btn.config(text="Pause/Reprendre", bg="#3498db")
            self.stop_btn.config(state=NORMAL)
            
            # Démarrer la reconnaissance dans un thread séparé
            self.video_thread = threading.Thread(target=self.face_recog)
            self.video_thread.daemon = True
            self.video_thread.start()
            
    def stop_recognition(self):
        """Arrêter le processus de reconnaissance faciale"""
        self.is_running = False
        self.recognition_enabled = False
        self.status_label.config(text="Reconnaissance Faciale : Désactivée", fg="#e74c3c")
        self.recognition_btn.config(text="Démarrer la Reconnaissance", bg="#2ecc71")
        self.stop_btn.config(state=DISABLED)
        
        # Fermer la caméra si elle est ouverte
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
            self.cap = None
        
        # Réinitialiser l'affichage vidéo
        blank_image = Image.new('RGB', (700, 500), color='black')
        blank_photo = ImageTk.PhotoImage(blank_image)
        self.video_frame.config(image=blank_photo)
        self.video_frame.image = blank_photo
        
        # Réinitialiser l'affichage des résultats
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        info_label = Label(
            self.result_frame,
            text="En attente de la reconnaissance faciale...",
            font=("Helvetica", 14),
            bg="#f9f9f9",
            fg="#7f8c8d",
        )
        info_label.pack(pady=250)
        
    def update_result_display(self, student_id, name, gender, dep, course=None, year=None, semester=None, is_marked=False):
        """Mettre à jour l'affichage des résultats de reconnaissance"""
        # Effacer les widgets existants
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        # Créer un cadre stylisé pour les informations de l'étudiant
        student_info = Frame(self.result_frame, bg="#f9f9f9")
        student_info.pack(pady=20, fill=BOTH, expand=True)
        
        # Icône de succès de reconnaissance
        success_frame = Frame(student_info, bg="#f9f9f9")
        success_frame.pack(pady=20)
        
        success_label = Label(
            success_frame,
            text="✓ RECONNAISSANCE RÉUSSIE",
            font=("Helvetica", 18, "bold"),
            bg="#f9f9f9",
            fg="#2ecc71",
        )
        success_label.pack()
        
        # Informations de l'étudiant
        info_frame = Frame(student_info, bg="#f9f9f9")
        info_frame.pack(pady=20, padx=50, fill=X)
        
        # Style pour les étiquettes et les valeurs
        label_font = ("Helvetica", 14)
        value_font = ("Helvetica", 14, "bold")
        
        # ID étudiant
        id_frame = Frame(info_frame, bg="#f9f9f9")
        id_frame.pack(fill=X, pady=10)
        
        id_label = Label(
            id_frame,
            text="ID Étudiant:",
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
        
        # Nom de l'étudiant
        name_frame = Frame(info_frame, bg="#f9f9f9")
        name_frame.pack(fill=X, pady=10)
        
        name_label = Label(
            name_frame,
            text="Nom:",
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
        
        # Genre (si disponible)
        if gender and gender != "N/A":
            gender_frame = Frame(info_frame, bg="#f9f9f9")
            gender_frame.pack(fill=X, pady=10)
            
            gender_label = Label(
                gender_frame,
                text="Genre:",
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
        
        # Département
        dep_frame = Frame(info_frame, bg="#f9f9f9")
        dep_frame.pack(fill=X, pady=10)
        
        dep_label = Label(
            dep_frame,
            text="Département:",
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
        
        # Cours (si disponible)
        if course and course != "N/A":
            course_frame = Frame(info_frame, bg="#f9f9f9")
            course_frame.pack(fill=X, pady=10)
            
            course_label = Label(
                course_frame,
                text="Cours:",
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
            
        # Année (si disponible)
        if year and year != "N/A":
            year_frame = Frame(info_frame, bg="#f9f9f9")
            year_frame.pack(fill=X, pady=10)
            
            year_label = Label(
                year_frame,
                text="Année:",
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
            
        # Statut de présence
        status_frame = Frame(info_frame, bg="#f9f9f9")
        status_frame.pack(fill=X, pady=10)
        
        status_label = Label(
            status_frame,
            text="Statut:",
            font=label_font,
            width=15,
            anchor=W,
            bg="#f9f9f9",
            fg="#333333",
        )
        status_label.pack(side=LEFT)
        
        status_text = "Présence Marquée" if is_marked else "Déjà Marqué"
        status_color = "#2ecc71" if is_marked else "#e67e22"
        
        status_value = Label(
            status_frame,
            text=status_text,
            font=value_font,
            bg="#f9f9f9",
            fg=status_color,
        )
        status_value.pack(side=LEFT)
        
        # Horodatage
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%d/%m/%Y")
        
        time_frame = Frame(info_frame, bg="#f9f9f9")
        time_frame.pack(fill=X, pady=10)
        
        time_label = Label(
            time_frame,
            text="Horodatage:",
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
        
    def get_student_info(self, student_id):
        """Récupérer les informations d'un étudiant depuis la base de données MySQL"""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Query modifiée pour correspondre à la structure de la base de données
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
            print(f"Erreur lors de la récupération des informations de l'étudiant: {str(e)}")
            messagebox.showerror("Erreur de base de données", f"Impossible de récupérer les informations: {str(e)}")
            return None
        
    def face_recog(self):
        """Fonction principale de reconnaissance faciale"""
        # Charger le classificateur pour la détection faciale
        try:
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            if face_cascade.empty():
                print("Erreur: Impossible de charger le classificateur Haar Cascade")
                # Essayer le chemin absolu avec cv2.data
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                if face_cascade.empty():
                    raise Exception("Le fichier haarcascade_frontalface_default.xml n'est pas valide")
        except Exception as e:
            messagebox.showerror("Erreur de classificateur", f"Impossible de charger le classificateur: {str(e)}")
            self.stop_recognition()
            return
        
        # Charger le modèle de reconnaissance faciale
        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            model_path = self.find_latest_model()
            if model_path:
                recognizer.read(model_path)
                print(f"Modèle chargé: {model_path}")
            else:
                raise Exception("Modèle de reconnaissance faciale introuvable")
        except Exception as e:
            messagebox.showerror("Erreur de modèle", f"Impossible de charger le modèle de reconnaissance: {str(e)}")
            self.stop_recognition()
            return
        
        # Initialiser la caméra
        self.cap = cv2.VideoCapture(0)
        
        # Vérifier si la caméra est ouverte
        if not self.cap.isOpened():
            # Essayer avec un autre index de caméra
            self.cap = cv2.VideoCapture(1)
            if not self.cap.isOpened():
                # Dernière tentative avec des options explicites
                self.cap = cv2.VideoCapture(0, cv2.CAP_ANY)
                if not self.cap.isOpened():
                    messagebox.showerror("Erreur de caméra", "Impossible d'accéder à la caméra. Veuillez vérifier que la caméra est bien connectée.")
                    self.stop_recognition()
                    return
        
        # Configurer la résolution de la caméra
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        print("Caméra initialisée avec succès")
        
        # Boucle principale de reconnaissance faciale
        while self.is_running:
            try:
                if not self.recognition_enabled:
                    # Si reconnaissance en pause, montrer juste le flux vidéo sans reconnaissance
                    ret, frame = self.cap.read()
                    if ret:
                        frame = cv2.flip(frame, 1)  # Miroir horizontal
                        # Convertir pour affichage Tkinter
                        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        img = Image.fromarray(rgb_frame)
                        img = img.resize((700, 500), Image.LANCZOS)
                        imgtk = ImageTk.PhotoImage(image=img)
                        
                        # Mettre à jour l'interface dans le thread principal
                        self.root.after(0, lambda: self.update_video_display(imgtk))
                    time.sleep(0.03)  # Réduire l'utilisation du CPU
                    continue
                
                ret, frame = self.cap.read()
                if not ret:
                    print("Erreur de lecture de la caméra")
                    time.sleep(0.1)
                    continue
                
                # Miroir horizontal pour une vision plus naturelle
                frame = cv2.flip(frame, 1)
                
                # Convertir en niveaux de gris pour la détection de visage
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.equalizeHist(gray)  # Améliorer le contraste
                
                # Détecter les visages dans l'image
                faces = face_cascade.detectMultiScale(
                    gray, 
                    scaleFactor=1.1, 
                    minNeighbors=5, 
                    minSize=(30, 30),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )
                
                # Dessiner un rectangle autour de chaque visage et effectuer la reconnaissance
                for (x, y, w, h) in faces:
                    # Dessiner un rectangle autour du visage
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    
                    # Extraire la région du visage
                    face_roi = gray[y:y+h, x:x+w]
                    
                    try:
                        # Redimensionner pour une meilleure reconnaissance
                        face_roi_resized = cv2.resize(face_roi, (92, 112), interpolation=cv2.INTER_AREA)
                        
                        # Reconnaissance faciale
                        id_pred, confidence = recognizer.predict(face_roi_resized)
                        
                        # Calculer le pourcentage de confiance (100% = match parfait)
                        confidence_value = 100 - int(confidence)
                        
                        # Afficher l'ID avec le niveau de confiance
                        text = f"ID: {id_pred} ({confidence_value}%)"
                        cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                        
                        # Si la confiance est suffisante, marquer la présence
                        if confidence < 70:  # Seuil de confiance
                            student_id = str(id_pred)
                            
                            # Limiter la fréquence de reconnaissance pour le même étudiant
                            current_time = time.time()
                            if student_id not in self.last_recognition_time or (current_time - self.last_recognition_time[student_id] > 5):
                                # Récupérer les informations de l'étudiant
                                student_info = self.get_student_info(student_id)
                                
                                if student_info:
                                    # Marquer la présence
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
                                    
                                    # Créer des variables locales pour la lambda
                                    student_id_copy = student_info["id"]
                                    name_copy = student_info["name"]
                                    gender_copy = student_info["gender"]
                                    dep_copy = student_info["dep"]
                                    course_copy = student_info["course"]
                                    year_copy = student_info["year"]
                                    semester_copy = student_info["semester"]
                                    is_marked_copy = is_marked
                                    
                                    # Mettre à jour l'affichage des résultats dans le thread principal
                                    self.root.after(0, lambda: self.update_result_display(
                                        student_id_copy, name_copy, gender_copy, dep_copy, 
                                        course_copy, year_copy, semester_copy, is_marked_copy))
                                    
                                    # Mettre à jour le temps de dernière reconnaissance
                                    self.last_recognition_time[student_id] = current_time
                    except Exception as e:
                        print(f"Erreur lors de la reconnaissance: {str(e)}")
                
                # Convertir l'image pour l'affichage Tkinter
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb_frame)
                img = img.resize((700, 500), Image.LANCZOS)
                imgtk = ImageTk.PhotoImage(image=img)
                
                # Mettre à jour l'interface dans le thread principal
                self.root.after(0, lambda: self.update_video_display(imgtk))
                
                # Petit délai pour éviter de surcharger le CPU
                time.sleep(0.03)
            
            except Exception as e:
                print(f"Erreur dans la boucle de reconnaissance: {str(e)}")
                time.sleep(0.1)
        
        # Libérer les ressources de la caméra
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
        print("Reconnaissance faciale arrêtée")

    def update_video_display(self, img_tk):
        """Mettre à jour l'affichage vidéo en toute sécurité"""
        self.video_frame.config(image=img_tk)
        self.video_frame.image = img_tk  # Garder une référence pour éviter le garbage collection

    def find_latest_model(self):
        """Trouver le modèle de reconnaissance le plus récent"""
        # Rechercher le modèle dans différents emplacements possibles
        possible_paths = [
            "classifier/classifier.xml",
            "classifier.xml",
            "TrainingImageLabel/Trainner.yml"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # Chercher dans le dossier classifier
        model_files = []
        if os.path.exists("classifier"):
            model_files = [os.path.join("classifier", f) for f in os.listdir("classifier") 
                          if f.endswith(".xml") or f.endswith(".yml")]
        
        # Chercher à la racine
        if not model_files:
            model_files = [f for f in os.listdir(".") if (f.endswith(".xml") or f.endswith(".yml")) 
                          and f != "haarcascade_frontalface_default.xml"]
        
        if model_files:
            # Trier par date de dernière modification (le plus récent en premier)
            model_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            return model_files[0]
        
        return None

if __name__ == "__main__":
    root = Tk()
    app = Face_recognition(root)
    root.mainloop()