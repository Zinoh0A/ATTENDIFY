from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import random
import time
import datetime
from main import Face_Recognition_System
def main():
   win=Tk()
   app=Login_Window(win)
   win.mainloop()

class Login_Window:
   def __init__(self,root):
         self.root=root  
         self.root.geometry("1530x790+0+0")
         self.root.title("Login")
         
         img3 = Image.open(r"login_images\login.jpg")
         img3 = img3.resize((1400, 1000), Image.LANCZOS)
         self.photoimg3 = ImageTk.PhotoImage(img3)

         lbl_bg = Label(self.root, image=self.photoimg3)
         lbl_bg.place(x=0, y=0, width=1400, height=1000)
         
         frame=Frame(self.root,bg="black")
         frame.place(x=500,y=170,width=340,height=450)
         img1=Image.open(r"login_images\login1.png")
         img1 = img1.resize((100, 100), Image.LANCZOS)
         self.photoimg1 = ImageTk.PhotoImage(img1)

         lblimg1 = Label(image=self.photoimg1,bg="black",borderwidth=0)
         lblimg1.place(x=625, y=175, width=100, height=100)

         get_str=Label(frame,text="Get started",font=("times new roman",20,"bold"),fg="white",bg="black")
         get_str.place(x=100,y=100,)
         #label
         username=lbl=Label(frame,text="Username",font=("times new roman",15,"bold"),fg="white",bg="black")
         username.place(x=70,y=155)
         
         self.txtuser=ttk.Entry(frame,font=("times new roman",15,"bold"))
         self.txtuser.place(x=25,y=180,width=270)
         password=lbl=Label(frame,text="Password",font=("times new roman",15,"bold"),fg="white",bg="black")
         password.place(x=70,y=255)
            
         self.txtpass=ttk.Entry(frame,font=("times new roman",15,"bold"))
         self.txtpass.place(x=25,y=290,width=270)
         

         #---------------Icon Image------------------
         img4=Image.open(r"login_images\user.png")
         img4 = img4.resize((27, 27), Image.LANCZOS)
         self.photoimg4= ImageTk.PhotoImage(img4)

         lblimg4 = Label(image=self.photoimg4,bg="black",borderwidth=0)
         lblimg4.place(x=540, y=323, width=27, height=27)

         img2=Image.open(r"login_images\pass.png")
         img2 = img2.resize((23, 23), Image.LANCZOS)
         self.photoimg2= ImageTk.PhotoImage(img2)

         lblimg2= Label(image=self.photoimg2,bg="black",borderwidth=0)
         lblimg2.place(x=540, y=430 ,width=23, height=23)
         #login button
         loginbtn=Button(frame,text="Login",command=self.login,font=("times new roman",15,"bold"),bd=3,relief=RIDGE,fg="white",bg="red")
         loginbtn.place(x=100,y=330,width=120,height=35)
         #register button
         registerbtn=Button(frame,text="New user Register",command=self.Register,font=("times new roman",8,"bold"),borderwidth=0,fg="red",bg="black")
         registerbtn.place(x=20,y=370,width=120)
         #forget passwordbtn
         forgetbtn=Button(frame,text="Forget password",font=("times new roman",8,"bold"),borderwidth=0,fg="red",bg="black")
         forgetbtn.place(x=-5,y=390,width=160)
   def register_window(self):
         self.new_window=Toplevel(self.root)
         #self.app=Register(self.new_window)
   def login(self):

      if self.txtuser.get()=="" or self.txtpass.get()=="":

         messagebox.showerror("Error","All fields are required",parent=self.root)
      elif self.txtuser.get()=='Wiam' and self.txtpass.get()=="2002":
            messagebox.showinfo("Sucess","Welcome to Systeme management",parent=self.root,)
        
         

      else:


            con=mysql.connector.connect(host="localhost",username="root",password="",database="login")

            cur=con.cursor()

            cur.execute('select * from register where username=%s and password=%s'

                        ,(self.txtuser.get(),self.txtpass.get()))

            row=cur.fetchone()

            if row==None:

               messagebox.showerror('Error','Invalid Username And Password'

                                    ,parent=self.root)

            else:
               open_main=messagebox.askyesno("YesNo","Access only Authority Person")
               if open_main>0:
                  self.new_window=Toplevel(self.root)
                  self.app=Face_Recognition_System(self.new_window)
               else:
                  if not open_main:
                     return
            con.commit()
            self.clear()
            con.close()
   def Register(self):



      Frame_login1=Frame(self.root,bg="white")

      Frame_login1.place(x=0,y=0,height=700,width=1366)

      

      self.img=ImageTk.PhotoImage(file="icones\back.jpg")
      img=Label(Frame_login1,image=self.img).place(x=0,y=0,width=1366,height=700)

      

      frame_input2=Frame(self.root,bg='white')

      frame_input2.place(x=320,y=130,height=450,width=630)



      label1=Label(frame_input2,text="Register Here",font=('impact',32,'bold'),fg="black",bg='white')

      label1.place(x=45,y=20)



      label2=Label(frame_input2,text="Username",font=("Goudy old style",20,"bold"),fg='orangered',bg='white')

      label2.place(x=30,y=95)

      self.entry=Entry(frame_input2,font=("times new roman",15,"bold"),bg='lightgray')

      self.entry.place(x=30,y=145,width=270,height=35)

      

      label3=Label(frame_input2,text="Password",font=("Goudy old style",20,"bold"),fg='orangered',bg='white')

      label3.place(x=30,y=195)

      self.entry2=Entry(frame_input2,font=("times new roman",15,"bold"),bg='lightgray')

      self.entry2.place(x=30,y=245,width=270,height=35)



      label4=Label(frame_input2,text="Email-id",font=("Goudy old style",20,"bold"),fg='orangered',bg='white')

      label4.place(x=330,y=95)

      self.entry3=Entry(frame_input2,font=("times new roman",15,"bold"),bg='lightgray')

      self.entry3.place(x=330,y=145,width=270,height=35)



      label5=Label(frame_input2,text="Confirm Password",font=("Goudy old style",20,"bold"),fg='orangered',bg='white')

      label5.place(x=330,y=195)

      self.entry4=Entry(frame_input2,font=("times new roman",15,"bold"),bg='lightgray')

      self.entry4.place(x=330,y=245,width=270,height=35)



      btn2=Button(frame_input2,command=self.register,text="Register"

                  ,cursor="hand2",font=("times new roman",15),fg="white",

                  bg="orangered",bd=0,width=15,height=1)

      btn2.place(x=90,y=340)


      btn3=Button(frame_input2,command=self.login,

                  text="Already Registered?Login",cursor="hand2",

                  font=("calibri",10),bg='white',fg="black",bd=0)

      btn3.place(x=110,y=390)
   def register(self):

      if self.entry.get()==""or self.entry2.get()==""or self.entry3.get()==""or self.entry4.get()=="":

         messagebox.showerror("Error","All Fields Are Required",parent=self.root)

      elif self.entry2.get()!=self.entry4.get():

         messagebox.showerror("Error","Password and Confirm Password Should Be Same"

                              ,parent=self.root)

      else:

         try:

            con=mysql.connector.connect(host="localhost",username="root",password="0000",

                              database="login")

            cur=con.cursor()

            cur.execute("select * from register where emailid=%s", [self.entry3.get()])


            row=cur.fetchone()

            if row!=None:

               messagebox.showerror("Error"

               ,"User already Exist,Please try with another Email"

                                    ,parent=self.root)

               self.regclear()

               self.entry.focus()

            else:

               cur.execute("INSERT INTO register (username, emailid, password, confirm_password) VALUES (%s, %s, %s, %s)",
               (self.entry.get(), self.entry3.get(), self.entry2.get(), self.entry4.get()))


               con.commit()

               con.close()

               messagebox.showinfo("Success","Register Succesfull",parent=self.root)

               self.regclear()

         except Exception as es:

            messagebox.showerror("Error",f"Error due to:{str(es)}"

                                 ,parent=self.root)
   def regclear(self):

      self.entry.delete(0,END)

      self.entry2.delete(0,END)

      self.entry3.delete(0,END)

      self.entry4.delete(0,END)



   def loginclear(self):

      self.email_txt.delete(0,END)

      self.password.delete(0,END)











if __name__ == "__main__":
      root = Tk()
      app = Login_Window(root)
      root.mainloop()

