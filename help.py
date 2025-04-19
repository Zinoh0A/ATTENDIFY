from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2


# page student interface
class Help:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1510x770+0+0")
        self.root.title("face Recognition  attendance System")
        # title ------------
        title_lbl = Label(
            self.root,
            text="HELP DESK",
            font=("times new roman", 35, "bold"),
            bg="white",
            fg="blue",
        )
        title_lbl.place(x=-60, y=0, width=1530, height=45)
        # top images
        img_top = Image.open(r"help_images\help.jpg"
        )
        img_top = img_top.resize((1530, 680), Image.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)
        f_lbl = Label(self.root, image=self.photoimg_top)
        f_lbl.place(x=0, y=45, width=1530, height=680)
        dev_label = Label(
            f_lbl,
            text="Email:  wiamterrab3@gmail.com   or tchorbodouae@gmail.com   ",
            font=("times new roman", 20, "bold"),
            bg="white",
            fg="black"
        )
        dev_label.place(x=350,y=30)




if __name__ == "__main__":
    root = Tk()
    obj = Help(root)
    root.mainloop()