from tkinter import *
from tkinter import ttk
import tkinter
from PIL import Image, ImageTk
from Student import Student
from train import FaceTrainer as Train
import os

from face_recognition import Face_recognition
from attendance import Attendance
from developper import Developer
from chatbot import ChatBot
from time import strftime
from datetime import datetime


class Face_Recognition_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("ATTENDIFY")
        self.root.configure(bg="#f0f0f0")  # Light gray background

        # Create a style for buttons
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12, "bold"), borderwidth=1)
        style.map("TButton", background=[("active", "#3366ff"), ("!active", "#0052cc")])
        style.configure("TFrame", background="#f0f0f0")

        # Top header frame
        header_frame = Frame(self.root, bg="#0052cc")  # Dark blue header
        header_frame.place(x=0, y=0, width=1530, height=130)

        # Title in center of header
        title_lbl = Label(header_frame, text="Smart Face Recognition Attendance System",
                          font=("Montserrat", 32, "bold"), bg="#0052cc", fg="white")
        title_lbl.pack(pady=40)  # Using pack to center horizontally

        # Logo on left
        img = Image.open(r"icones\ENSAH.png")
        img = img.resize((100, 100), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)
        logo_lbl = Label(header_frame, image=self.photoimg, bg="#0052cc", bd=0)
        logo_lbl.place(x=20, y=15)

        # Digital clock on right
        def time():
            string = strftime("%H:%M:%S %p")
            clock_lbl.config(text=string)
            clock_lbl.after(1000, time)

        clock_frame = Frame(header_frame, bg="#003d99", bd=2, relief=RAISED)  # Slightly darker blue
        clock_frame.place(x=1350, y=40, width=150, height=50)

        clock_lbl = Label(clock_frame, font=('Arial', 14, 'bold'), bg="#003d99", fg="white")
        clock_lbl.place(x=5, y=5, width=140, height=40)
        time()

        # Main content area with modern card layout
        main_frame = Frame(self.root, bg="#f0f0f0")
        main_frame.place(x=0, y=130, width=1530, height=660)

        # Create a canvas for subtle gradient background
        canvas = Canvas(main_frame, bg="#f0f0f0", bd=0, highlightthickness=0)
        canvas.place(x=0, y=0, width=1530, height=660)

        # Create gradient
        canvas.create_rectangle(0, 0, 1530, 660, fill="#f0f0f0", outline="")
        for i in range(660):
            color = f"#{int(240 - i / 10):02x}{int(240 - i / 10):02x}{int(240 - i / 10):02x}"
            canvas.create_line(0, i, 1530, i, fill=color)

        # Calculate center positioning for cards
        # Total width of 4 cards with spacing
        card_width = 220
        card_spacing = 30
        total_row_width = (4 * card_width) + (3 * card_spacing)
        start_x = (1530 - total_row_width) // 2

        # Store image objects
        self.card_images = {}

        # Function to create modern card buttons
        def create_card(index, image_path, title, command):
            row = index // 4
            col = index % 4

            x = start_x + (col * (card_width + card_spacing))
            y = 50 + (row * 290)  # Increased vertical spacing between rows

            # Main card frame
            card_frame = Frame(main_frame, bg="white", bd=0, cursor="hand2")
            card_frame.place(x=x, y=y, width=card_width, height=260)

            # Card shadow effect
            shadow_frame = Frame(main_frame, bg="#cccccc")
            shadow_frame.place(x=x + 5, y=y + 5, width=card_width, height=260)
            card_frame.lift()

            # Border frame to add blue border
            border_frame = Frame(card_frame, bg="#0052cc", bd=1)
            border_frame.place(x=0, y=0, width=card_width, height=260)

            # Inner frame for content with white background
            inner_frame = Frame(border_frame, bg="white")
            inner_frame.place(x=1, y=1, width=card_width - 2, height=258)

            # Load image with PIL and convert to Tkinter PhotoImage
            try:
                img = Image.open(image_path)
                img = img.resize((180, 180), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                # Store reference to prevent garbage collection
                self.card_images[title] = photo
            except Exception as e:
                # Fallback if image can't be loaded
                print(f"Error loading image {image_path}: {e}")
                # Create blank image as fallback
                self.card_images[title] = None

            # Create image label
            img_lbl = Label(inner_frame, bg="white", cursor="hand2")
            if self.card_images[title]:
                img_lbl.config(image=self.card_images[title])
            img_lbl.place(x=20, y=10, width=180, height=180)

            # Title
            title_lbl = Label(inner_frame, text=title, font=("Arial", 14, "bold"),
                              bg="white", fg="#0052cc", cursor="hand2")
            title_lbl.place(x=0, y=200, width=220, height=30)

            # Make entire card clickable
            card_frame.bind("<Button-1>", lambda e: command())
            img_lbl.bind("<Button-1>", lambda e: command())
            title_lbl.bind("<Button-1>", lambda e: command())

            # Enhanced hover effect with blue tint
            def on_enter(e):
                inner_frame.config(bg="#e6f0ff")  # Light blue background
                title_lbl.config(bg="#e6f0ff", fg="#0066ff")  # Brighter blue text
                img_lbl.config(bg="#e6f0ff")
                shadow_frame.config(bg="#3399ff")  # Blue shadow on hover
                border_frame.config(bg="#3399ff", bd=2)  # Thicker blue border

            def on_leave(e):
                inner_frame.config(bg="white")
                title_lbl.config(bg="white", fg="#0052cc")
                img_lbl.config(bg="white")
                shadow_frame.config(bg="#cccccc")
                border_frame.config(bg="#0052cc", bd=1)

            # Bind hover events to all elements
            for widget in [card_frame, inner_frame, img_lbl, title_lbl]:
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)

        # Create cards in centered layout
        cards_config = [
            (r"icones\students.png", "Student Details", self.student_details),
            (r"icones\facedetector.png", "Face Detector", self.face_data),
            (r"icones\Attendance.png", "Attendance", self.attendance_data),
            (r"chatbot_images\chatbot.png", "ChatBot", self.chatbot_data),
            (r"icones\train.png", "Train Data", self.train_data),
            (r"icones\photos.png", "Photos", self.open_img),
            (r"icones\developer.png", "Developer", self.developer_data),
            (r"icones\exit.png", "Exit", self.iExit)
        ]

        for i, (img_path, title, command) in enumerate(cards_config):
            create_card(i, img_path, title, command)

        # Footer
        footer_frame = Frame(self.root, bg="#0052cc", height=30)
        footer_frame.place(x=0, y=760, width=1530, height=30)

        footer_text = Label(footer_frame, text="© 2025 Smart Face Recognition System. All Rights Reserved.",
                            font=("Arial", 10), bg="#0052cc", fg="white")
        footer_text.place(x=0, y=0, width=1530, height=30)

    def open_img(self):
        os.startfile("data")

    def iExit(self):
        if tkinter.messagebox.askyesno("Smart Face Recognition", "Are you sure you want to exit?",
                                       icon='question'):
            self.root.destroy()
        else:
            return

    # Functions buttons
    def student_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)

    def train_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Train(self.new_window)

    def face_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Face_recognition(self.new_window)

    def attendance_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Attendance(self.new_window)

    def developer_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Developer(self.new_window)

    def chatbot_data(self):
        self.new_window = Toplevel(self.root)
        self.app = ChatBot(self.new_window)


if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()