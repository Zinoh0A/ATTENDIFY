import os
import cv2
import numpy as np
from datetime import datetime
from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk

class FaceTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("Entraîneur Facial - Expert Version")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f5f5f5')
        
        # Configuration initiale
        self.data_dir = "data"
        self.output_dir = "classifier"
        self.min_images_required = 10  # Minimum d'images par personne
        self.current_id = 0
        self.id_to_name = {}
        
        # Paramètres du modèle (optimisés)
        self.recognizer_params = {
            'radius': 2,
            'neighbors': 16,
            'grid_x': 10,
            'grid_y': 10,
            'threshold': 70
        }
        
        # Setup UI
        self.setup_ui()
        self.verify_directories()
        
    def setup_ui(self):
        """Interface utilisateur avancée"""
        # Frame principal
        main_frame = Frame(self.root, bg='#f5f5f5')
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header = Label(main_frame, 
                     text="SYSTÈME EXPERT D'ENTRAÎNEMENT FACIAL",
                     font=('Arial', 20, 'bold'),
                     bg='#2c3e50',
                     fg='white',
                     pady=15)
        header.pack(fill=X)
        
        # Section image
        self.img_frame = Frame(main_frame, bg='white', bd=2, relief=GROOVE)
        self.img_frame.pack(fill=BOTH, expand=True, pady=15)
        
        self.canvas = Canvas(self.img_frame, bg='white', highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Contrôles
        control_frame = Frame(main_frame, bg='#f5f5f5')
        control_frame.pack(fill=X, pady=10)
        
        Button(control_frame, 
              text="SÉLECTIONNER DOSSIER DATA", 
              command=self.select_data_dir,
              font=('Arial', 12),
              bg='#3498db',
              fg='white').pack(side=LEFT, padx=5)
        
        Button(control_frame, 
              text="LANCER L'ENTRAÎNEMENT", 
              command=self.start_training,
              font=('Arial', 12, 'bold'),
              bg='#27ae60',
              fg='white').pack(side=LEFT, padx=5)
        
        # Barre de statut
        self.status_var = StringVar()
        self.status_var.set("Prêt - Sélectionnez le dossier contenant les images")
        
        status_bar = Label(main_frame, 
                         textvariable=self.status_var,
                         font=('Arial', 10),
                         bg='#2c3e50',
                         fg='white',
                         anchor=W)
        status_bar.pack(fill=X, side=BOTTOM)
        
        # Afficher un exemple
        self.show_naming_example()
    
    def show_naming_example(self):
        """Affiche un exemple de nommage"""
        example = """
        Format requis pour les noms de fichiers:
        
        user.ID.numéro.jpg
        
        Exemples valides:
        - user.1.1.jpg
        - user.23.5.jpg
        - user.101.10.jpg
        
        Les images doivent être dans le dossier 'data'.
        """
        
        self.canvas.create_text(10, 10, 
                              text=example,
                              font=('Arial', 12),
                              anchor=NW,
                              fill='#333')
    
    def verify_directories(self):
        """Vérifie/crée les dossiers nécessaires"""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
        if not os.listdir(self.data_dir):
            self.status_var.set(f"Attention: Le dossier '{self.data_dir}' est vide!")
    
    def select_data_dir(self):
        """Permet de sélectionner le dossier data"""
        dir_path = filedialog.askdirectory(initialdir=self.data_dir)
        if dir_path:
            self.data_dir = dir_path
            self.status_var.set(f"Dossier sélectionné: {dir_path}")
            
            # Comptage des images JPG uniquement
            image_count = len([f for f in os.listdir(dir_path) 
                             if f.lower().endswith('.jpg')])
            self.status_var.set(f"{image_count} images JPG trouvées dans {os.path.basename(dir_path)}")
    
    def start_training(self):
        """Lance le processus complet"""
        # Vérification initiale
        if not self.validate_data_dir():
            return
            
        # Phase 1: Préparation des données
        faces, ids, names_info = self.prepare_training_data()
        if not faces:
            return
            
        # Phase 2: Entraînement
        model_path = os.path.join(self.output_dir, f"model_{datetime.now().strftime('%Y%m%d_%H%M')}.xml")
        success = self.train_model(faces, ids, model_path)
        
        if success:
            # Sauvegarde des métadonnées
            self.save_metadata(names_info, model_path)
            
            # Sauvegarde aussi comme trainer.xml pour être facilement trouvé
            generic_model_path = os.path.join(self.output_dir, "trainer.xml")
            if os.path.exists(model_path):
                import shutil
                shutil.copy2(model_path, generic_model_path)
            
            # Message final
            messagebox.showinfo("Succès",
                              f"Entraînement terminé avec succès!\n\n"
                              f"• Personnes enregistrées: {len(set(ids))}\n"
                              f"• Images utilisées: {len(faces)}\n"
                              f"• Modèle sauvegardé sous:\n{model_path}")
    
    def validate_data_dir(self):
        """Valide le contenu du dossier data"""
        if not os.path.exists(self.data_dir):
            messagebox.showerror("Erreur", f"Dossier '{self.data_dir}' introuvable!")
            return False
            
        # Ne considérer que les fichiers JPG
        image_files = [f for f in os.listdir(self.data_dir) 
                      if f.lower().endswith('.jpg')]
        
        if not image_files:
            messagebox.showerror("Erreur", f"Aucune image JPG trouvée dans '{self.data_dir}'!")
            return False
            
        return True
    
    def prepare_training_data(self):
        """Prépare les données pour l'entraînement"""
        faces = []
        ids = []
        names_info = {}
        
        # Ne considérer que les fichiers JPG
        image_files = [f for f in os.listdir(self.data_dir) 
                      if f.lower().endswith('.jpg')]
        
        # Charge le classificateur Haar
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # Pour le suivi de la progression
        total_files = len(image_files)
        processed_files = 0
        
        for filename in image_files:
            try:
                processed_files += 1
                progress = (processed_files / total_files) * 100
                self.status_var.set(f"Traitement: {filename} ({progress:.1f}%)")
                self.root.update()
                
                # Extraction des informations depuis le nom du fichier
                base_name = os.path.splitext(filename)[0]
                
                # Vérifier le format user.ID.numéro.jpg
                parts = base_name.split('.')
                if len(parts) >= 2 and parts[0].lower() == 'user':
                    try:
                        student_id = int(parts[1])  # L'ID est le second élément
                        names_info[student_id] = f"user_{student_id}"
                    except ValueError:
                        self.log_error(f"ID invalide dans: {filename} - ignoré")
                        continue
                else:
                    self.log_error(f"Format invalide: {filename} - ignoré")
                    continue
                
                # Traitement de l'image
                img_path = os.path.join(self.data_dir, filename)
                face_img = self.process_image(img_path, face_cascade)
                
                if face_img is not None:
                    faces.append(face_img)
                    ids.append(student_id)
                    self.log_progress(filename, student_id, names_info.get(student_id, f"ID:{student_id}"))
                else:
                    self.log_error(f"Aucun visage détecté dans {filename}")
                    
            except Exception as e:
                self.log_error(f"Erreur avec {filename}: {str(e)}")
                continue
        
        # Vérification finale
        if not faces:
            messagebox.showerror("Erreur", "Aucun visage n'a été détecté dans les images!")
            return [], [], {}
        
        return faces, ids, names_info
    
    def process_image(self, img_path, face_cascade):
        """Traite une image pour en extraire le visage"""
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return None
            
        # Amélioration du contraste pour une meilleure détection
        img = cv2.equalizeHist(img)
        
        # Détection du visage
        faces = face_cascade.detectMultiScale(
            img, 
            scaleFactor=1.1, 
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        if len(faces) == 0:
            return None
            
        (x, y, w, h) = faces[0]
        face_roi = img[y:y+h, x:x+w]
        
        # Prétraitement
        face_roi = cv2.resize(face_roi, (300, 300))
        face_roi = cv2.equalizeHist(face_roi)  # Normalisation du contraste
        
        return face_roi
    
    def train_model(self, faces, ids, model_path):
        """Effectue l'entraînement du modèle"""
        try:
            self.status_var.set("Début de l'entraînement...")
            self.root.update()
            
            # Conversion des IDs
            ids = np.array(ids)
            
            # Création du modèle
            recognizer = cv2.face.LBPHFaceRecognizer_create(
                radius=self.recognizer_params['radius'],
                neighbors=self.recognizer_params['neighbors'],
                grid_x=self.recognizer_params['grid_x'],
                grid_y=self.recognizer_params['grid_y']
            )
            
            # Entraînement
            recognizer.train(faces, ids)
            
            # Sauvegarde
            recognizer.save(model_path)
            
            # Aussi sauvegarder une copie avec un nom générique pour faciliter la détection
            generic_model_path = os.path.join(self.output_dir, "trainer.xml")
            recognizer.save(generic_model_path)
            
            self.status_var.set("Entraînement terminé avec succès!")
            
            return True
            
        except Exception as e:
            self.log_error(f"Échec de l'entraînement: {str(e)}")
            return False
    
    def save_metadata(self, names_info, model_path):
        """Sauvegarde les informations complémentaires"""
        # Fichier de correspondance noms/IDs
        with open(os.path.join(self.output_dir, "names_ids.txt"), "w") as f:
            for id, name in names_info.items():
                f.write(f"{id}:{name}\n")
        
        # Fichier de configuration
        with open(os.path.join(self.output_dir, "training_config.cfg"), "w") as f:
            f.write(f"model_path={model_path}\n")
            f.write(f"training_date={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"threshold={self.recognizer_params['threshold']}\n")
    
    def log_progress(self, filename, student_id, full_name):
        """Affiche la progression"""
        msg = f"Traitée: {filename} → ID:{student_id} ({full_name})"
        self.status_var.set(msg)
        self.root.update()
        print(f"[INFO] {msg}")
    
    def log_error(self, message):
        """Log les erreurs"""
        self.status_var.set(f"Erreur: {message}")
        self.root.update()
        print(f"[ERROR] {message}")

if __name__ == "__main__":
    root = Tk()
    
    # Centrage de la fenêtre
    window_width = 1000
    window_height = 700
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    app = FaceTrainer(root)
    root.mainloop()