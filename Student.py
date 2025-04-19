from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import threading
import time
from dlib_face_recognition import DlibFaceRecognition  # Import our new module

# Student class with dlib integration
class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1510x770+0+0")
        self.root.title("Face Recognition Attendance System")
        ##########variables##############
        self.var_dep = StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_std_id = StringVar()
        self.var_std_name = StringVar()
        self.var_div = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_address = StringVar()
        self.var_teacher = StringVar()
        
        # Initialize dlib face recognition system
        try:
            self.face_recognition = DlibFaceRecognition()
            self.dlib_available = True
        except Exception as e:
            messagebox.showerror("Error", f"Could not initialize facial recognition: {str(e)}")
            self.dlib_available = False
        
        # Rest of your initialization code...
        # image1------------------------
        img = Image.open(r"student images\image-85.webp")
        img = img.resize((500, 130), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)
        f_lbl = Label(self.root, image=self.photoimg)
        f_lbl.place(x=0, y=0, width=500, height=130)
        # image2-----------------------
        img1 = Image.open(r"student images\face-recognition-806x440.webp")
        img1 = img1.resize((500, 130), Image.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        f_lbl = Label(self.root, image=self.photoimg1)
        f_lbl.place(x=500, y=0, width=500, height=130)
        
        # image 3----------------------
        img2 = Image.open(r"student images\happy-female-student.webp")
        img2 = img2.resize((500, 130), Image.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)
        f_lbl = Label(self.root, image=self.photoimg2)
        f_lbl.place(x=950, y=0, width=500, height=130)
        
        # background image ---------------
        img3 = Image.open(r"student images\student-management.png")
        img3 = img3.resize((1400, 1000), Image.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)
        bg_img = Label(self.root, image=self.photoimg3)
        bg_img.place(x=0, y=130, width=1400, height=600)
        
        title_lbl = Label(
            bg_img,
            text="Student management system",
            font=("times new roman", 35, "bold"),
            bg="white",
            fg="darkgreen",
        )
        title_lbl.place(x=0, y=0, relwidth=1530, height=45)
        
        main_frame = Frame(bg_img, bd=2, bg="white")
        main_frame.place(x=20, y=0, width=1500, height=600)
        
        # left label frame
        Left_frame = LabelFrame(
            main_frame,
            bd=2,
            relief=RIDGE,
            text="Student Detail",
            font=("times new roman", 12, "bold"),
        )
        Left_frame.place(x=10, y=2, width=730, height=680)
        
        img_left = Image.open(r"student images\studentdetail.png")
        img_left = img2.resize((720, 130), Image.LANCZOS)
        self.photoimg_left = ImageTk.PhotoImage(img_left)
        f_lbl = Label(Left_frame, image=self.photoimg_left)
        f_lbl.place(x=5, y=0, width=720, height=130)
        
        # current course information
        current_course_frame = LabelFrame(
            Left_frame,
            bd=2,
            bg="white",
            text="Current course information",
            relief=RIDGE,
            font=("times new roman", 12, "bold"),
        )
        current_course_frame.place(x=5, y=70, width=720, height=150)
        
        # Departement
        dep_label = Label(
            current_course_frame,
            text="Departement",
            font=("times new roman", 12, "bold"),
            bg="white",
        )
        dep_label.grid(row=0, column=0, padx=10, sticky=W)
        
        dep_combo = ttk.Combobox(
            current_course_frame,
            font=("times new roman", 12, "bold"),
            textvariable=self.var_dep,
            width=17,
            state="readonly",
        )
        dep_combo["values"] = (
            "Select Departement",
            "IDSCC",
            "Civil",
            "Industriel",
            "Electrique",
            "software",
            "Itirc",
        )
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)
        
        # course
        course_label = Label(
            current_course_frame,
            text="Course",
            font=("times new roman", 13, "bold"),
            bg="white",
        )
        course_label.grid(row=0, column=2, padx=10, sticky=W)
        
        course_combo = ttk.Combobox(
            current_course_frame,
            font=("times new roman", 13, "bold"),
            textvariable=self.var_course,
            width=17,
            state="readonly",
        )
        course_combo["values"] = (
            "Select Course",
            "Java",
            "Mecanique",
            "Python",
            "STR",
            "Database",
        )
        course_combo.current(0)
        course_combo.grid(row=0, column=3, padx=2, pady=10, sticky=W)
        
        # year
        year_label = Label(
            current_course_frame,
            text="Year",
            font=("times new roman", 13, "bold"),
            bg="white",
        )
        year_label.grid(row=1, column=0, padx=10, sticky=W)
        
        year_combo = ttk.Combobox(
            current_course_frame,
            font=("times new roman", 13, "bold"),
            textvariable=self.var_year,
            width=17,
            state="readonly",
        )
        year_combo["values"] = (
            "Select Year",
            "2022-23",
            "2023-24",
            "2024-25",
            "2025-26",
        )
        year_combo.current(0)
        year_combo.grid(row=1, column=1, padx=2, pady=10, sticky=W)
        
        # Semestre
        Semester_label = Label(
            current_course_frame,
            text="Semester",
            font=("times new roman", 13, "bold"),
            bg="white",
        )
        Semester_label.grid(row=1, column=2, padx=10, sticky=W)
        Semester_combo = ttk.Combobox(
            current_course_frame,
            textvariable=self.var_semester,
            font=("times new roman", 13, "bold"),
            width=17,
            state="readonly",
        )
        Semester_combo["values"] = ("Select Semestre", "Semestre-1", "Semestre-2")
        Semester_combo.current(0)
        Semester_combo.grid(row=1, column=3, padx=2, pady=10, sticky=W)
        
        # Class Student information
        class_Student_frame = LabelFrame(
            Left_frame,
            bd=2,
            bg="white",
            relief=RIDGE,
            text="Class Student information",
            font=("times new roman", 13, "bold"),
        )
        class_Student_frame.place(x=5, y=220, width=750, height=350)
        
        # student Id
        StudentId_label = Label(
            class_Student_frame,
            text="StudentID:",
            font=("times new roman", 13, "bold"),
            bg="white",
        )
        StudentId_label.grid(row=0, column=0, padx=10, sticky=W)
        
        StudentId_entry = Entry(
            class_Student_frame,
            width=20,
            textvariable=self.var_std_id,
            font=("times new roman", 13, "bold"),
        )
        StudentId_entry.grid(row=0, column=1, padx=10, sticky=W)
        
        # student name
        studenName_label = Label(
            class_Student_frame,
            text="Student Name:",
            font=("times new roman", 13, "bold"),
            bg="white",
        )
        studenName_label.grid(row=0, column=2, padx=10, pady=5, sticky=W)
        
        studenName_entry = ttk.Entry(
            class_Student_frame,
            textvariable=self.var_std_name,
            width=20,
            font=("times new roman", 13, "bold"),
        )
        studenName_entry.grid(row=0, column=3, padx=10, pady=5, sticky=W)
        
        # class division
        class_div_label = Label(
            class_Student_frame,
            text="Class Division:",
            font=("times new roman", 13, "bold"),
            bg="white",
        )
        class_div_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)
        
        div_combo = ttk.Combobox(
            class_Student_frame,
            font=("times new roman", 13, "bold"),
            textvariable=self.var_div,
            width=17,
            state="readonly",
        )
        div_combo["values"] = ("DR1", "DR2", "DR3")
        div_combo.current(0)
        div_combo.grid(row=1, column=1, padx=2, pady=10, sticky=W)
        
        # Gender (à la place de Roll No)
        gender_label = Label(
            class_Student_frame,
            text="Gender:",
            font=("times new roman", 13, "bold"),
            bg="white",
        )
        gender_label.grid(row=1, column=2, padx=10, pady=5, sticky=W)
        
        gender_combo = ttk.Combobox(
            class_Student_frame,
            font=("times new roman", 13, "bold"),
            textvariable=self.var_gender,
            width=17,
            state="readonly",
        )
        gender_combo["values"] = ("Select Gender", "Male", "Female", "Other")
        gender_combo.current(0)
        gender_combo.grid(row=1, column=3, padx=2, pady=10, sticky=W)
        
        # DOB
        dob_label = Label(
            class_Student_frame,
            text="DOB:",
            font=("times new roman", 13, "bold"),
            bg="white",
        )
        dob_label.grid(row=2, column=0, padx=10, pady=5, sticky=W)
        
        dob_entry = ttk.Entry(
            class_Student_frame,
            textvariable=self.var_dob,
            width=20,
            font=("times new roman", 13, "bold"),
        )
        dob_entry.grid(row=2, column=1, padx=10, pady=5, sticky=W)
        
        # Email
        email_label = Label(
            class_Student_frame,
            text="Email:",
            font=("times new roman", 13, "bold"),
            bg="white",
        )
        email_label.grid(row=2, column=2, padx=10, pady=5, sticky=W)
        email_entry = ttk.Entry(
            class_Student_frame,
            textvariable=self.var_email,
            width=20,
            font=("times new roman", 13, "bold"),
        )
        email_entry.grid(row=2, column=3, padx=10, pady=5, sticky=W)
        
        # phone no
        phone_label = Label(
            class_Student_frame,
            text="Phone No:",
            font=("times new roman", 13, "bold"),
            bg="white",
        )
        phone_label.grid(row=3, column=0, padx=10, pady=5, sticky=W)
        phone_entry = ttk.Entry(
            class_Student_frame,
            textvariable=self.var_phone,
            width=20,
            font=("times new roman", 13, "bold"),
        )
        phone_entry.grid(row=3, column=1, padx=10, pady=5, sticky=W)
        
        # Adresse
        adresse_label = Label(
            class_Student_frame,
            text="Address:",
            font=("times new roman", 13, "bold"),
            bg="white",
        )
        adresse_label.grid(row=3, column=2, padx=10, pady=5, sticky=W)
        adresse_entry = ttk.Entry(
            class_Student_frame,
            textvariable=self.var_address,
            width=20,
            font=("times new roman", 13, "bold"),
        )
        adresse_entry.grid(row=3, column=3, padx=10, pady=5, sticky=W)
        
        # Teacher name
        teacher_label = Label(
            class_Student_frame,
            text="Teacher Name:",
            font=("times new roman", 13, "bold"),
            bg="white",
        )
        teacher_label.grid(row=4, column=0, padx=10, pady=5, sticky=W)
        teacher_entry = ttk.Entry(
            class_Student_frame,
            textvariable=self.var_teacher,
            width=20,
            font=("times new roman", 13, "bold"),
        )
        teacher_entry.grid(row=4, column=1, padx=10, pady=5, sticky=W)
        
        # Radio Buttons pour la photo
        self.var_radio1 = StringVar()
        radiobtn1 = ttk.Radiobutton(
            class_Student_frame,
            variable=self.var_radio1,
            text="Take Photo Sample",
            value="Yes",
        )
        radiobtn1.grid(row=4, column=2, padx=10, pady=5, sticky=W)
        radiobtn2 = ttk.Radiobutton(
            class_Student_frame,
            variable=self.var_radio1,
            text="No Photo Sample",
            value="No",
        )
        radiobtn2.grid(row=4, column=3, padx=10, pady=5, sticky=W)
        
        # Buttons frame
        btn_frame = Frame(class_Student_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame.place(x=0, y=250, width=720, height=35)
        save_btn = Button(
            btn_frame,
            text="Save",
            command=self.add_data,
            width=17,
            font=("times new roman", 13, "bold"),
            bg="blue",
            fg="white",
        )
        save_btn.grid(row=0, column=0)
        update_btn = Button(
            btn_frame,
            text="Update",
            command=self.update_data,
            width=17,
            font=("times new roman", 13, "bold"),
            bg="blue",
            fg="white",
        )
        update_btn.grid(row=0, column=1)
        delete_btn = Button(
            btn_frame,
            text="Delete",
            command=self.delete_data,
            width=17,
            font=("times new roman", 13, "bold"),
            bg="blue",
            fg="white",
        )
        delete_btn.grid(row=0, column=2)
        reset_btn = Button(
            btn_frame,
            text="Reset",
            command=self.reset_data,
            width=17,
            font=("times new roman", 13, "bold"),
            bg="blue",
            fg="white",
        )
        reset_btn.grid(row=0, column=3)
        btn_frame1 = Frame(class_Student_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame1.place(x=0, y=290, width=720, height=35)
        take_photo_btn = Button(
            btn_frame1,
            text="Take Photo Sample (dlib)",
            command=self.generate_dataset_dlib,
            width=35,
            font=("times new roman", 13, "bold"),
            bg="blue",
            fg="white",
        )
        take_photo_btn.grid(row=0, column=0)
        update_photo_btn = Button(
            btn_frame1,
            text="Update Photo Sample",
            width=35,
            font=("times new roman", 13, "bold"),
            bg="blue",
            fg="white",
        )
        update_photo_btn.grid(row=0, column=1)
        
        # Right label frame
        Right_frame = LabelFrame(
            main_frame,
            bd=2,
            relief=RIDGE,
            text="Student Details",
            font=("times new roman", 12, "bold"),
        )
        Right_frame.place(x=750, y=2, width=730, height=680)
        
        # Search frame
        search_frame = LabelFrame(
            Right_frame,
            bd=2,
            bg="white",
            relief=RIDGE,
            text="Search System",
            font=("times new roman", 12, "bold"),
        )
        search_frame.place(x=5, y=10, width=710, height=70)
        
        search_label = Label(
            search_frame,
            text="Search By:",
            font=("times new roman", 13, "bold"),
            bg="red",
            fg="white",
        )
        search_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)
        
        # Variable pour la recherche
        self.var_search_combo = StringVar()
        search_combo = ttk.Combobox(
            search_frame,
            textvariable=self.var_search_combo,
            font=("times new roman", 13, "bold"),
            width=15,
            state="readonly",
        )
        search_combo["values"] = ("Select", "Student_id", "Name", "Phone")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)
        
        # Variable pour le texte de recherche
        self.var_search_entry = StringVar()
        search_entry = ttk.Entry(
            search_frame,
            textvariable=self.var_search_entry,
            width=15,
            font=("times new roman", 13, "bold"),
        )
        search_entry.grid(row=0, column=2, padx=10, pady=5, sticky=W)
        
        search_btn = Button(
            search_frame,
            command=self.search_data,
            text="Search",
            width=14,
            font=("times new roman", 13, "bold"),
            bg="blue",
            fg="white",
        )
        search_btn.grid(row=0, column=3, padx=4)
        showall_btn = Button(
            search_frame,
            command=self.fetch_data,
            text="Show All",
            width=14,
            font=("times new roman", 13, "bold"),
            bg="blue",
            fg="white",
        )
        showall_btn.grid(row=0, column=4, padx=4)
        
        # Table frame
        table_frame = Frame(Right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=5, y=90, width=710, height=360)
        
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)
        
        # Configuration de la table (suppression de "roll" de la liste des colonnes)
        self.student_table = ttk.Treeview(
            table_frame,
            column=(
                "dep", "course", "year", "sem", "id", "name", "div", "gender",
                "dob", "email", "phone", "address", "teacher", "photo"
            ),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set,
        )
        
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("dep", text="Department")
        self.student_table.heading("course", text="Course")
        self.student_table.heading("year", text="Year")
        self.student_table.heading("sem", text="Semester")
        self.student_table.heading("id", text="StudentId")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("div", text="Division")
        self.student_table.heading("gender", text="Gender")
        self.student_table.heading("dob", text="DOB")
        self.student_table.heading("email", text="Email")
        self.student_table.heading("phone", text="Phone")
        self.student_table.heading("address", text="Address")
        self.student_table.heading("teacher", text="Teacher")
        self.student_table.heading("photo", text="PhotoSampleStatus")
        
        self.student_table["show"] = "headings"

        # Increase these values to fit your data
        self.student_table.column("dep", width=120)
        self.student_table.column("course", width=120)
        self.student_table.column("year", width=120)
        self.student_table.column("sem", width=120)
        self.student_table.column("id", width=120)
        self.student_table.column("name", width=140)
        self.student_table.column("div", width=120)
        self.student_table.column("gender", width=120)
        self.student_table.column("dob", width=140)
        self.student_table.column("email", width=180)
        self.student_table.column("phone", width=140)
        self.student_table.column("address", width=180)
        self.student_table.column("teacher", width=140)
        self.student_table.column("photo", width=150)
        
        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<ButtonRelease>", self.get_cursor)
        self.fetch_data()
    
    # fonction pour ajouter des données au tableau
    def add_data(self):
        if (
            self.var_dep.get() == "Select Department"
            or self.var_std_name.get() == ""
            or self.var_std_id.get() == ""
        ):
            messagebox.showerror("Error", "Tous les champs sont requis", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",  # Votre nom d'utilisateur MySQL
                    password="",  # Votre mot de passe MySQL
                    database="face_recognition_system"  # Nom correct de la base de données
                )
                cursor = conn.cursor()
                
                # Vérifier si l'étudiant existe déjà
                cursor.execute("SELECT * FROM student WHERE Student_id=%s", (self.var_std_id.get(),))
                existing_student = cursor.fetchone()
                
                if existing_student:
                    messagebox.showerror("Error", "Cet ID étudiant existe déjà", parent=self.root)
                else:
                    # Ajouter un nouvel étudiant (sans le champ "roll")
                    sql = """INSERT INTO student (Dep, Course, Year, Semester, Student_id, 
                             Name, Division, Gender, DOB, Email, Phone, Address, 
                             Teacher, PhotoSample) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    
                    values = (
                        self.var_dep.get(),
                        self.var_course.get(),
                        self.var_year.get(),
                        self.var_semester.get(),
                        self.var_std_id.get(),
                        self.var_std_name.get(),
                        self.var_div.get(),
                        self.var_gender.get(),
                        self.var_dob.get(),
                        self.var_email.get(),
                        self.var_phone.get(),
                        self.var_address.get(),
                        self.var_teacher.get(),
                        self.var_radio1.get()
                    )
                    
                    cursor.execute(sql, values)
                    conn.commit()
                    conn.close()
                    
                    self.fetch_data()
                    messagebox.showinfo("Success", "Étudiant ajouté avec succès", parent=self.root)
                
            except Exception as es:
                messagebox.showerror("Error", f"En raison de: {str(es)}", parent=self.root)
                
    # Afficher les données
    def fetch_data(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="face_recognition_system"
            )
            cursor = conn.cursor()

            # Make sure to select columns in the same order as your treeview
            cursor.execute(
                "SELECT Dep, Course, Year, Semester, Student_id, Name, Division, Gender, DOB, Email, Phone, Address, Teacher, PhotoSample FROM student")
            data = cursor.fetchall()

            if len(data) != 0:
                self.student_table.delete(*self.student_table.get_children())
                for i in data:
                    self.student_table.insert("", END, values=i)
                conn.commit()
            conn.close()
        except Exception as es:
            messagebox.showerror("Error", f"En raison de: {str(es)}", parent=self.root)
    
    # Fonction pour récupérer les données lorsqu'on clique sur un élément du tableau
    def get_cursor(self, event=""):
        cursor_row = self.student_table.focus()
        content = self.student_table.item(cursor_row)
        data = content["values"]

        if data:
            # Print for debugging
            print("Selected row data:", data)
            self.var_dep.set(data[0])
            self.var_course.set(data[1])
            self.var_year.set(data[2])
            self.var_semester.set(data[3])
            self.var_std_id.set(data[4])
            self.var_std_name.set(data[5])
            self.var_div.set(data[6])
            self.var_gender.set(data[7])
            self.var_dob.set(data[8])
            self.var_email.set(data[9])
            self.var_phone.set(data[10])
            self.var_address.set(data[11])
            self.var_teacher.set(data[12])
            self.var_radio1.set(data[13])
    
    # Fonction de recherche
    def search_data(self):
        if self.var_search_combo.get() == "Select" or self.var_search_entry.get() == "":
            messagebox.showerror("Error", "Veuillez sélectionner un critère de recherche et saisir une valeur",
                                 parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="face_recognition_system"
                )
                cursor = conn.cursor()

                # Build search query
                search_field = self.var_search_combo.get()
                search_value = self.var_search_entry.get()

                query = f"SELECT Dep, Course, Year, Semester, Student_id, Name, Division, Gender, DOB, Email, Phone, Address, Teacher, PhotoSample FROM student WHERE {search_field} LIKE %s"
                cursor.execute(query, (f"%{search_value}%",))

                rows = cursor.fetchall()
                if len(rows) != 0:
                    self.student_table.delete(*self.student_table.get_children())
                    for row in rows:
                        self.student_table.insert("", END, values=row)
                else:
                    messagebox.showinfo("Info", "Aucun résultat trouvé", parent=self.root)

                conn.commit()
                conn.close()
            except Exception as es:
                messagebox.showerror("Error", f"En raison de: {str(es)}", parent=self.root)
    
    # Fonction pour mettre à jour les données
    def update_data(self):
        if (
            self.var_dep.get() == "Select Department"
            or self.var_std_name.get() == ""
            or self.var_std_id.get() == ""
        ):
            messagebox.showerror("Error", "Tous les champs sont requis", parent=self.root)
        else:
            try:
                update = messagebox.askyesno(
                    "Update",
                    "Voulez-vous mettre à jour cet étudiant?",
                    parent=self.root
                )
                
                if update:
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="root",  # Votre nom d'utilisateur MySQL
                        password="",  # Votre mot de passe MySQL
                        database="face_recognition_system"  # Nom correct de la base de données
                    )
                    cursor = conn.cursor()
                    
                    # Requête de mise à jour sans le champ "roll"
                    sql = """UPDATE student SET Dep=%s, Course=%s, Year=%s, Semester=%s, 
                             Name=%s, Division=%s, Gender=%s, DOB=%s, Email=%s, 
                             Phone=%s, Address=%s, Teacher=%s, PhotoSample=%s 
                           WHERE Student_id=%s"""
                    
                    values = (
                        self.var_dep.get(),
                        self.var_course.get(),
                        self.var_year.get(),
                        self.var_semester.get(),
                        self.var_std_name.get(),
                        self.var_div.get(),
                        self.var_gender.get(),
                        self.var_dob.get(),
                        self.var_email.get(),
                        self.var_phone.get(),
                        self.var_address.get(),
                        self.var_teacher.get(),
                        self.var_radio1.get(),
                        self.var_std_id.get()
                    )
                    
                    cursor.execute(sql, values)
                    conn.commit()
                    conn.close()
                    
                    self.fetch_data()
                    messagebox.showinfo(
                        "Success", "Étudiant mis à jour avec succès", parent=self.root
                    )
            except Exception as es:
                messagebox.showerror("Error", f"En raison de: {str(es)}", parent=self.root)
                
    # Fonction pour supprimer des données
    def delete_data(self):
        if self.var_std_id.get() == "":
            messagebox.showerror("Error", "L'ID étudiant est requis", parent=self.root)
        else:
            try:
                delete = messagebox.askyesno(
                    "Delete",
                    "Voulez-vous supprimer cet étudiant?",
                    parent=self.root
                )
                
                if delete:
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="root",  # Votre nom d'utilisateur MySQL
                        password="",  # Votre mot de passe MySQL
                        database="face_recognition_system"  # Nom correct de la base de données
                    )
                    cursor = conn.cursor()
                    sql = "DELETE FROM student WHERE Student_id=%s"
                    values = (self.var_std_id.get(),)
                    cursor.execute(sql, values)
                    conn.commit()
                    conn.close()
                    
                    self.fetch_data()
                    self.reset_data()
                    messagebox.showinfo(
                        "Delete", "Étudiant supprimé avec succès", parent=self.root
                    )
            except Exception as es:
                messagebox.showerror("Error", f"En raison de: {str(es)}", parent=self.root)
    
    # Fonction pour réinitialiser les champs
    def reset_data(self):
        self.var_dep.set("Select Department")
        self.var_course.set("Select Course")
        self.var_year.set("Select Year")
        self.var_semester.set("Select Semester")
        self.var_std_id.set("")
        self.var_std_name.set("")
        self.var_div.set("Select Division")
        self.var_gender.set("Select Gender")
        self.var_dob.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_teacher.set("")
        self.var_radio1.set("")
    
    # New function to generate dataset using dlib (replaces the old function)
    def generate_dataset_dlib(self):
        """Generate a facial recognition dataset using dlib for a student"""
        if (
            self.var_dep.get() == "Select Department"
            or self.var_std_name.get() == ""
            or self.var_std_id.get() == ""
        ):
            messagebox.showerror("Error", "Tous les champs sont requis", parent=self.root)
        else:
            try:
                # Check if dlib is available
                if not self.dlib_available:
                    messagebox.showerror("Error", "Le système de reconnaissance faciale dlib n'est pas disponible",
                                        parent=self.root)
                    return
                
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="face_recognition_system"
                )
                cursor = conn.cursor()

                # Check if student ID is a valid number
                try:
                    student_id = int(self.var_std_id.get())
                except ValueError:
                    messagebox.showerror("Error", "L'ID étudiant doit être un nombre entier", parent=self.root)
                    return

                # Create photo capture window
                capture_window = Toplevel(self.root)
                capture_window.title("Capture Photo")
                capture_window.geometry("640x640")
                capture_window.resizable(False, False)
                
                # Instructions
                instruction_label = Label(capture_window, 
                                         text="Positionnez votre visage au centre et regardez la caméra",
                                         font=("Arial", 12, "bold"))
                instruction_label.pack(pady=10)
                
                # Frame for video
                video_frame = Label(capture_window)
                video_frame.pack(padx=10, pady=10)
                
                # Status label
                status_label = Label(capture_window, text="Préparation de la caméra...", font=("Arial", 10))
                status_label.pack(pady=5)
                
                # Buttons
                button_frame = Frame(capture_window)
                button_frame.pack(pady=10)
                
                capture_btn = Button(button_frame, text="Capturer", width=15, 
                                    font=("Arial", 10, "bold"), state=DISABLED)
                capture_btn.grid(row=0, column=0, padx=10)
                
                retry_btn = Button(button_frame, text="Réessayer", width=15, 
                                  font=("Arial", 10, "bold"), state=DISABLED)
                retry_btn.grid(row=0, column=1, padx=10)
                
                save_btn = Button(button_frame, text="Enregistrer", width=15, 
                                 font=("Arial", 10, "bold"), state=DISABLED)
                save_btn.grid(row=0, column=2, padx=10)
                
                cancel_btn = Button(button_frame, text="Annuler", width=15, 
                                   font=("Arial", 10, "bold"), command=capture_window.destroy)
                cancel_btn.grid(row=0, column=3, padx=10)
                
                # Variables
                self.cap = None
                self.is_capturing = True
                self.current_frame = None
                self.face_detected = False
                self.captured_image = None
                
                # Function to update the video feed
                def update_video():
                    if self.is_capturing and self.cap is not None and self.cap.isOpened():
                        ret, frame = self.cap.read()
                        if ret:
                            # Flip horizontally for a mirror effect
                            frame = cv2.flip(frame, 1)
                            self.current_frame = frame.copy()
                            
                            # Detect faces
                            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            face_locations = self.face_recognition.face_detector(rgb_frame, 1)
                            
                            self.face_detected = len(face_locations) > 0
                            
                            # Draw rectangle around faces
                            for face_location in face_locations:
                                x, y, w, h = (face_location.left(), face_location.top(), 
                                             face_location.width(), face_location.height())
                                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            
                            # Update status
                            if self.face_detected:
                                status_label.config(text="Visage détecté! Cliquez sur 'Capturer'")
                                capture_btn.config(state=NORMAL)
                            else:
                                status_label.config(text="Aucun visage détecté. Veuillez vous positionner correctement.")
                                capture_btn.config(state=DISABLED)
                            
                            # Convert to ImageTk
                            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            img = Image.fromarray(img)
                            img = img.resize((600, 450))
                            imgtk = ImageTk.PhotoImage(image=img)
                            video_frame.imgtk = imgtk  # Keep a reference
                            video_frame.config(image=imgtk)
                            
                            # Schedule the next update
                            video_frame.after(10, update_video)
                        else:
                            status_label.config(text="Erreur de lecture de la caméra. Veuillez réessayer.")
                    
                # Function to capture the current frame
                def capture_image():
                    if self.current_frame is not None and self.face_detected:
                        self.captured_image = self.current_frame.copy()
                        
                        # Display the captured image
                        img = cv2.cvtColor(self.captured_image, cv2.COLOR_BGR2RGB)
                        img = Image.fromarray(img)
                        img = img.resize((600, 450))
                        imgtk = ImageTk.PhotoImage(image=img)
                        video_frame.imgtk = imgtk
                        video_frame.config(image=imgtk)
                        
                        # Stop the video capture
                        self.is_capturing = False
                        
                        # Update status and buttons
                        status_label.config(text="Image capturée! Cliquez sur 'Enregistrer' ou 'Réessayer'")
                        capture_btn.config(state=DISABLED)
                        retry_btn.config(state=NORMAL)
                        save_btn.config(state=NORMAL)
                
                # Function to retry capturing
                def retry_capture():
                    self.captured_image = None
                    self.is_capturing = True
                    
                    # Reset buttons
                    retry_btn.config(state=DISABLED)
                    save_btn.config(state=DISABLED)
                    
                    # Restart video
                    update_video()
                
                # Function to save the captured image
                def save_image():
                    if self.captured_image is not None:
                        try:
                            # Use dlib to add face to the database
                            success, message = self.face_recognition.add_face(self.captured_image, student_id)
                            
                            if success:
                                # Update database to mark photo as taken
                                cursor.execute("UPDATE student SET PhotoSample=%s WHERE Student_id=%s", 
                                              ("Yes", student_id))
                                conn.commit()
                                
                                messagebox.showinfo("Success", message, parent=capture_window)
                                
                                # Close capture window
                                capture_window.destroy()
                                
                                # Refresh student table
                                self.fetch_data()
                            else:
                                messagebox.showerror("Error", message, parent=capture_window)
                                retry_capture()
                                
                        except Exception as e:
                            messagebox.showerror("Error", f"Erreur lors de l'enregistrement: {str(e)}", 
                                                parent=capture_window)
                            retry_capture()
                
                # Set button commands
                capture_btn.config(command=capture_image)
                retry_btn.config(command=retry_capture)
                save_btn.config(command=save_image)
                
                # Initialize camera
                def initialize_camera():
                    try:
                        self.cap = cv2.VideoCapture(0)
                        
                        # Set resolution
                        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                        
                        if not self.cap.isOpened():
                            messagebox.showerror("Error", "Impossible d'accéder à la caméra", 
                                                parent=capture_window)
                            capture_window.destroy()
                            return
                        
                        status_label.config(text="Caméra initialisée. Positionnez votre visage dans le cadre.")
                        update_video()
                    except Exception as e:
                        messagebox.showerror("Error", f"Erreur d'initialisation de la caméra: {str(e)}", 
                                            parent=capture_window)
                        capture_window.destroy()
                
                # Clean up resources when window is closed
                def on_closing():
                    self.is_capturing = False
                    if self.cap is not None and self.cap.isOpened():
                        self.cap.release()
                    capture_window.destroy()
                
                capture_window.protocol("WM_DELETE_WINDOW", on_closing)
                
                # Start camera in a separate thread
                threading.Thread(target=initialize_camera).start()
                
            except Exception as e:
                messagebox.showerror("Error", f"En raison de: {str(e)}", parent=self.root)
                print(f"Exception détaillée: {str(e)}")