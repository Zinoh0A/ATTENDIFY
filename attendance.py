from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import csv
from tkinter import filedialog

mydata = []


# Redesigned Attendance page with modern UI
class Attendance:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Smart Face Recognition Attendance System")
        self.root.configure(bg="#f0f0f0")  # Match main page background

        # Variables
        self.var_atten_id = StringVar()
        self.var_atten_roll = StringVar()
        self.var_atten_name = StringVar()
        self.var_atten_dep = StringVar()
        self.var_atten_time = StringVar()
        self.var_atten_date = StringVar()
        self.var_atten_attendance = StringVar()

        # Create consistent styles
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12, "bold"), borderwidth=1)
        style.map("TButton", background=[("active", "#3366ff"), ("!active", "#0052cc")])
        style.configure("TEntry", font=("Arial", 11))
        style.configure("TCombobox", font=("Arial", 11))
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

        # Header Frame
        header_frame = Frame(self.root, bg="#0052cc")  # Same dark blue header
        header_frame.place(x=0, y=0, width=1530, height=130)

        # Title in header
        title_lbl = Label(header_frame, text="ATTENDANCE MANAGEMENT SYSTEM",
                          font=("Montserrat", 32, "bold"), bg="#0052cc", fg="white")
        title_lbl.pack(pady=40)

        # Logo on left
        img = Image.open(r"icones\ENSAH.png")
        img = img.resize((100, 100), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)
        logo_lbl = Label(header_frame, image=self.photoimg, bg="#0052cc", bd=0)
        logo_lbl.place(x=20, y=15)

        # Main content area
        main_frame = Frame(self.root, bg="#f0f0f0")
        main_frame.place(x=0, y=130, width=1530, height=630)

        # Create content card with shadow effect
        content_shadow = Frame(main_frame, bg="#cccccc")
        content_shadow.place(x=25, y=25, width=1480, height=580)

        content_card = Frame(main_frame, bg="white", bd=0)
        content_card.place(x=20, y=20, width=1480, height=580)

        # Left side - Form panel
        left_frame = Frame(content_card, bg="white", bd=0)
        left_frame.place(x=10, y=10, width=720, height=560)

        # Title for form panel
        left_title = Label(left_frame, text="Student Attendance Details",
                           font=("Arial", 18, "bold"), bg="white", fg="#0052cc")
        left_title.place(x=0, y=0, width=720, height=50)

        # Image banner
        img_left = Image.open(r"attendance_systeme\StudentsAttendency.png")
        img_left = img_left.resize((400, 140), Image.LANCZOS)
        self.photoimg_left = ImageTk.PhotoImage(img_left)
        banner_lbl = Label(left_frame, image=self.photoimg_left, bg="white", bd=0)
        banner_lbl.place(x=0, y=60, width=720, height=130)

        # Form container
        form_frame = Frame(left_frame, bg="white", bd=0)
        form_frame.place(x=10, y=200, width=700, height=350)

        # Form fields with modern layout
        # Using grid with consistent padding and styling

        # Row 1
        attendanceId_label = Label(form_frame, text="Attendance ID:",
                                   font=("Arial", 12), bg="white", fg="#333333")
        attendanceId_label.grid(row=0, column=0, padx=20, pady=20, sticky=W)
        attendanceId_entry = ttk.Entry(form_frame, textvariable=self.var_atten_id, width=22)
        attendanceId_entry.grid(row=0, column=1, padx=10, pady=20, sticky=W)

        roll_label = Label(form_frame, text="Roll:", font=("Arial", 12), bg="white", fg="#333333")
        roll_label.grid(row=0, column=2, padx=20, pady=20, sticky=W)
        roll_entry = ttk.Entry(form_frame, textvariable=self.var_atten_roll, width=22)
        roll_entry.grid(row=0, column=3, padx=10, pady=20, sticky=W)

        # Row 2
        name_label = Label(form_frame, text="Name:", font=("Arial", 12), bg="white", fg="#333333")
        name_label.grid(row=1, column=0, padx=20, pady=20, sticky=W)
        name_entry = ttk.Entry(form_frame, textvariable=self.var_atten_name, width=22)
        name_entry.grid(row=1, column=1, padx=10, pady=20, sticky=W)

        dep_label = Label(form_frame, text="Department:", font=("Arial", 12), bg="white", fg="#333333")
        dep_label.grid(row=1, column=2, padx=20, pady=20, sticky=W)
        dep_entry = ttk.Entry(form_frame, textvariable=self.var_atten_dep, width=22)
        dep_entry.grid(row=1, column=3, padx=10, pady=20, sticky=W)

        # Row 3
        time_label = Label(form_frame, text="Time:", font=("Arial", 12), bg="white", fg="#333333")
        time_label.grid(row=2, column=0, padx=20, pady=20, sticky=W)
        time_entry = ttk.Entry(form_frame, textvariable=self.var_atten_time, width=22)
        time_entry.grid(row=2, column=1, padx=10, pady=20, sticky=W)

        date_label = Label(form_frame, text="Date:", font=("Arial", 12), bg="white", fg="#333333")
        date_label.grid(row=2, column=2, padx=20, pady=20, sticky=W)
        date_entry = ttk.Entry(form_frame, textvariable=self.var_atten_date, width=22)
        date_entry.grid(row=2, column=3, padx=10, pady=20, sticky=W)

        # Row 4
        attendance_label = Label(form_frame, text="Attendance Status:",
                                 font=("Arial", 12), bg="white", fg="#333333")
        attendance_label.grid(row=3, column=0, padx=20, pady=20, sticky=W)

        self.attend_status = ttk.Combobox(form_frame, textvariable=self.var_atten_attendance,
                                          width=20, state="readonly")
        self.attend_status["values"] = ("Status", "Present", "Absent")
        self.attend_status.current(0)
        self.attend_status.grid(row=3, column=1, padx=10, pady=20, sticky=W)

        # Button frame with modern buttons
        btn_frame = Frame(form_frame, bg="white")
        btn_frame.place(x=0, y=240, width=700, height=80)

        # Create modern buttons with consistent style and spacing
        import_btn = Button(btn_frame, text="Import CSV", command=self.importCsv,
                            font=("Arial", 11, "bold"), width=16, bg="#0052cc", fg="white",
                            cursor="hand2", activebackground="#3366ff", activeforeground="white")
        import_btn.grid(row=0, column=0, padx=10, pady=20)

        export_btn = Button(btn_frame, text="Export CSV", command=self.exportCsv,
                            font=("Arial", 11, "bold"), width=16, bg="#0052cc", fg="white",
                            cursor="hand2", activebackground="#3366ff", activeforeground="white")
        export_btn.grid(row=0, column=1, padx=10, pady=20)

        update_btn = Button(btn_frame, text="Update",
                            font=("Arial", 11, "bold"), width=16, bg="#0052cc", fg="white",
                            cursor="hand2", activebackground="#3366ff", activeforeground="white")
        update_btn.grid(row=0, column=2, padx=10, pady=20)

        reset_btn = Button(btn_frame, text="Reset", command=self.reset_data,
                           font=("Arial", 11, "bold"), width=16, bg="#0052cc", fg="white",
                           cursor="hand2", activebackground="#3366ff", activeforeground="white")
        reset_btn.grid(row=0, column=3, padx=10, pady=20)

        # Right side - Table panel
        right_frame = Frame(content_card, bg="white", bd=0)
        right_frame.place(x=740, y=10, width=730, height=560)

        # Title for table panel
        right_title = Label(right_frame, text="Attendance Records",
                            font=("Arial", 18, "bold"), bg="white", fg="#0052cc")
        right_title.place(x=0, y=0, width=730, height=50)

        # Table frame with shadow effect
        table_shadow = Frame(right_frame, bg="#cccccc")
        table_shadow.place(x=15, y=65, width=700, height=480)

        table_frame = Frame(right_frame, bg="white", bd=0)
        table_frame.place(x=10, y=60, width=700, height=480)

        # Scrollbars
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        # Treeview
        self.AttendanceReportTable = ttk.Treeview(table_frame,
                                                  column=(
                                                  "id", "roll", "name", "departement", "time", "date", "attendance"),
                                                  xscrollcommand=scroll_x.set,
                                                  yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.AttendanceReportTable.xview)
        scroll_y.config(command=self.AttendanceReportTable.yview)  # Fixed yview issue

        # Configure column headings
        self.AttendanceReportTable.heading("id", text="ID")
        self.AttendanceReportTable.heading("roll", text="Roll")
        self.AttendanceReportTable.heading("name", text="Name")
        self.AttendanceReportTable.heading("departement", text="Department")
        self.AttendanceReportTable.heading("time", text="Time")
        self.AttendanceReportTable.heading("date", text="Date")
        self.AttendanceReportTable.heading("attendance", text="Status")

        self.AttendanceReportTable["show"] = "headings"

        # Configure column widths
        self.AttendanceReportTable.column("id", width=80)
        self.AttendanceReportTable.column("roll", width=80)
        self.AttendanceReportTable.column("name", width=120)
        self.AttendanceReportTable.column("departement", width=120)
        self.AttendanceReportTable.column("time", width=80)
        self.AttendanceReportTable.column("date", width=80)
        self.AttendanceReportTable.column("attendance", width=80)

        self.AttendanceReportTable.bind("<ButtonRelease>", self.get_cursor)
        self.AttendanceReportTable.pack(fill=BOTH, expand=1)

        # Footer
        footer_frame = Frame(self.root, bg="#0052cc", height=30)
        footer_frame.place(x=0, y=760, width=1530, height=30)

        footer_text = Label(footer_frame, text="© 2025 Smart Face Recognition System. All Rights Reserved.",
                            font=("Arial", 10), bg="#0052cc", fg="white")
        footer_text.place(x=0, y=0, width=1530, height=30)

    # Fetch data to populate table
    def fetchData(self, rows):
        self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
        for i in rows:
            self.AttendanceReportTable.insert("", END, values=i)

    # Import CSV
    def importCsv(self):
        global mydata
        mydata.clear()
        fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open CSV",
                                         filetypes=(("CSV File", "*.csv"), ("All File", "*.*")), parent=self.root)
        if fln:  # Check if file was selected
            try:
                with open(fln) as myfile:
                    csvread = csv.reader(myfile, delimiter=",")
                    for i in csvread:
                        mydata.append(i)
                    self.fetchData(mydata)
                    messagebox.showinfo("Success", f"Data imported from {os.path.basename(fln)} successfully",
                                        parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Error due to: {str(es)}", parent=self.root)

    # Export CSV
    def exportCsv(self):
        try:
            if len(mydata) < 1:
                messagebox.showerror("No Data", "No data found to export", parent=self.root)
                return False
            fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save CSV",
                                               filetypes=(("CSV File", "*.csv"), ("All File", "*.*")), parent=self.root)
            if fln:  # Check if a filename was provided
                with open(fln, mode="w", newline="") as myfile:
                    exp_write = csv.writer(myfile, delimiter=",")
                    for i in mydata:
                        exp_write.writerow(i)
                    messagebox.showinfo("Data Export", f"Your data exported to {os.path.basename(fln)} successfully")
        except Exception as es:
            messagebox.showerror("Error", f"Error due to: {str(es)}", parent=self.root)

    # Get cursor
    def get_cursor(self, event=""):
        cursor_row = self.AttendanceReportTable.focus()
        content = self.AttendanceReportTable.item(cursor_row)
        rows = content['values']
        if rows:  # Ensure rows exists
            self.var_atten_id.set(rows[0])
            self.var_atten_roll.set(rows[1])
            self.var_atten_name.set(rows[2])
            self.var_atten_dep.set(rows[3])
            self.var_atten_time.set(rows[4])
            self.var_atten_date.set(rows[5])
            self.var_atten_attendance.set(rows[6])

    # Reset data
    def reset_data(self):
        self.var_atten_id.set("")
        self.var_atten_roll.set("")
        self.var_atten_name.set("")
        self.var_atten_dep.set("")
        self.var_atten_time.set("")
        self.var_atten_date.set("")
        self.var_atten_attendance.set("Status")


if __name__ == "__main__":
    root = Tk()
    obj = Attendance(root)
    root.mainloop()