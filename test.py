attendanceId_label = Label(
            left_inside_frame,
            text="AttendenceID:",
            font=("times new roman", 13, "bold"),
            bg="white",
        )
        attendanceId_label.grid(row=0, column=0, padx=10, sticky=W)
        attendanceId_entry =ttk.Entry(
            left_inside_frame,
            width=20,
            font=("times new roman", 13, "bold"),
        )
        attendanceId_entry.grid(row=0, column=1, padx=10, sticky=W)
        # student name
        rolllabel = Label(
            left_inside_frame,
            text="Roll:",
            font=("comicsansns 11 bold"),
            bg="white",
        )
        rolllabel.grid(row=0, column=2, padx=4, pady=10)
        attenroll = ttk.Entry(
            left_inside_frame,
            width=22,
            font=("comicsansns 11 bold")
        )
        attenroll.grid(row=0, column=3 ,pady=8)
        #date
        name_label = Label(
            left_inside_frame,
            text="Name:",
            font=("comicsansns 11 bold"),
            bg="white",
        )
        name_label.grid(row=1, column=0)
        attend_name = ttk.Entry(
            left_inside_frame,
            width=22,
             font=("comicsansns 11 bold"),
        )
        attend_name.grid(row=1, column=1,pady=8)
        # Departement
        dep_label = Label(
            left_inside_frame,
            text="Departement:",
            font=("comicsansns 11 bold"),
            bg="white",
        )
        dep_label.grid(row=1, column=0)
        attend_dep = ttk.Entry(
            left_inside_frame,
            width=22,
             font=("comicsansns 11 bold"),
        )
        attend_dep.grid(row=1, column=3,pady=8)
        #time
        time_label = Label(
            left_inside_frame,
            text="Time:",
            font=("comicsansns 11 bold"),
            bg="white",
        )
        time_label.grid(row=2, column=0)
        attend_time = ttk.Entry(
            left_inside_frame,
            width=22,
             font=("comicsansns 11 bold"),
        )
        attend_time.grid(row=2, column=1,pady=8)
        #Date
        date_label = Label(
            left_inside_frame,
            text="Date:",
            font=("comicsansns 11 bold"),
            bg="white",
        )
        date_label.grid(row=2, column=2)
        attend_date= ttk.Entry(
            left_inside_frame,
            width=22,
             font=("comicsansns 11 bold"),
        )
        attend_date.grid(row=2, column=3,pady=8)
        #attendance
        attendanceLabel = Label(
            left_inside_frame,
            text="Attendance Status:",
            font=("comicsansns 11 bold"),
            bg="white",
        )
        attendanceLabel.grid(row=3, column=0)
        self.attend_status = ttk.Combobox(
            left_inside_frame,
            width=20,
            font="comicsansns 11 bold",
            state="readonly"
           
            
        )
           
        self.attend_status["values"] = (
            "Status",
            "Present",
            "Abscent",
        )
        self.attend_status.current(0)
        self.attend_status.grid(row=3, column=1, pady=8)
        # right label frame
        Right_frame = LabelFrame(
            main_frame,
            bd=2,
            relief=RIDGE,
            text="Student Detail",
            font=("times new roman", 13, "bold"),
            bg="white",
        )
        Right_frame.place(x=755, y=2, width=590, height=580)