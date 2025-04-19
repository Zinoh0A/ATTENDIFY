from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import webbrowser
import time
from tkinter.font import Font


class Developer:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1510x770+0+0")
        self.root.title("Attendify - Face Recognition Attendance System")
        self.root.configure(bg="#f0f0f0")

        # Create custom fonts
        self.title_font = Font(family="Helvetica", size=36, weight="bold")
        self.heading_font = Font(family="Helvetica", size=24, weight="bold")
        self.subheading_font = Font(family="Helvetica", size=16, weight="bold")
        self.text_font = Font(family="Helvetica", size=12)
        self.button_font = Font(family="Helvetica", size=12, weight="bold")

        # Create loading screen
        self.show_loading_screen()

        # Main content (will be created after loading)
        self.root.after(2000, self.create_main_content)

    def show_loading_screen(self):
        """Display an animated loading screen"""
        self.loading_frame = Frame(self.root, bg="#3498db")
        self.loading_frame.place(x=0, y=0, width=1510, height=770)

        # Loading title
        loading_title = Label(
            self.loading_frame,
            text="ATTENDIFY",
            font=self.title_font,
            bg="#3498db",
            fg="white"
        )
        loading_title.place(relx=0.5, rely=0.4, anchor=CENTER)

        # Loading subtitle
        loading_subtitle = Label(
            self.loading_frame,
            text="AI-Powered Face Recognition Attendance System",
            font=self.subheading_font,
            bg="#3498db",
            fg="white"
        )
        loading_subtitle.place(relx=0.5, rely=0.47, anchor=CENTER)

        # Loading message
        loading_msg = Label(
            self.loading_frame,
            text="Loading...",
            font=self.text_font,
            bg="#3498db",
            fg="white"
        )
        loading_msg.place(relx=0.5, rely=0.52, anchor=CENTER)

        # Create progress bar
        self.progress = ttk.Progressbar(
            self.loading_frame,
            orient=HORIZONTAL,
            length=400,
            mode='determinate'
        )
        self.progress.place(relx=0.5, rely=0.57, anchor=CENTER, width=400)

        # Animate progress bar
        self.animate_progress_bar()

    def animate_progress_bar(self):
        """Animate the progress bar from 0 to 100%"""
        for i in range(101):
            self.progress['value'] = i
            self.root.update_idletasks()
            time.sleep(0.01)

    def create_main_content(self):
        """Create the main content after loading"""
        # Remove loading screen
        self.loading_frame.destroy()

        # Apply custom style to ttk elements
        style = ttk.Style()
        style.configure('TButton', font=self.button_font)
        style.configure('TFrame', background='white')

        # Create gradient background
        self.create_gradient_background()

        # Title
        title_frame = Frame(self.root, bg="#ffffff", bd=0, highlightthickness=0)
        title_frame.place(x=50, y=20, width=1410, height=70)

        title_lbl = Label(
            title_frame,
            text="ATTENDIFY DEVELOPMENT TEAM",
            font=self.title_font,
            bg="#ffffff",
            fg="#2c3e50"
        )
        title_lbl.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Main content frame
        main_frame = Frame(self.root, bg="white", bd=0, highlightthickness=0)
        main_frame.place(x=50, y=100, width=1410, height=620)

        # Left frame with team details
        left_frame = Frame(main_frame, bg="white", bd=0)
        left_frame.place(x=20, y=20, width=500, height=580)

        # Team icon (text-based since no images)
        icon_frame = Frame(left_frame, bg="#3498db", bd=0)
        icon_frame.place(x=10, y=10, width=480, height=300)

        icon_text = Label(
            icon_frame,
            text="ATTENDIFY",
            font=self.title_font,
            bg="#3498db",
            fg="white"
        )
        icon_text.place(relx=0.5, rely=0.4, anchor=CENTER)

        icon_subtitle = Label(
            icon_frame,
            text="Face Recognition Attendance System",
            font=self.subheading_font,
            bg="#3498db",
            fg="white"
        )
        icon_subtitle.place(relx=0.5, rely=0.6, anchor=CENTER)

        # Team description panel
        desc_frame = Frame(left_frame, bg="#f8f9fa", bd=0)
        desc_frame.place(x=10, y=320, width=480, height=250)

        team_title = Label(
            desc_frame,
            text="About Attendify",
            font=self.heading_font,
            bg="#f8f9fa",
            fg="#2c3e50"
        )
        team_title.place(x=20, y=20)

        team_desc = Label(
            desc_frame,
            text="Attendify is an AI-powered face recognition system\ndeveloped by engineering students from\nEcole Nationale des Sciences Appliquées d'Al Hoceima (ENSAH).\n\nOur system automates classroom attendance tracking\nusing advanced facial recognition technology,\nreducing administrative workload and providing\naccurate attendance records.",
            font=self.text_font,
            bg="#f8f9fa",
            fg="#34495e",
            justify=LEFT
        )
        team_desc.place(x=20, y=60)

        # Right frame with developer profiles
        right_frame = Frame(main_frame, bg="white", bd=0)
        right_frame.place(x=540, y=20, width=850, height=580)

        # Create scrollable canvas for developer profiles
        canvas = Canvas(right_frame, bg="white", bd=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg="white")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Developer data
        developers = [
            {"name": "Aya Haiti", "role": "AI Engineer", "linkedin": "https://www.linkedin.com/in/aya-haiti"},
            {"name": "Zaynab Ait Addi", "role": "AI Engineer", "linkedin": "https://www.linkedin.com/in/zaynab-ait-addi-688708271"},
            {"name": "Hasnae Alballaoui", "role": "AI Engineer",
             "linkedin": "https://www.linkedin.com/in/hasnae-elballaoui-312209256"},
            {"name": "Rim Mazghout", "role": "AI Engineer", "linkedin": "https://www.linkedin.com/in/rim-mazgout-039b62316/"},
            {"name": "Mohammed Oulhadj", "role": "AI Engineer", "linkedin": "https://linkedin.com/in/mohammed-oulhadj"}
        ]

        # Create profile cards
        for i, dev in enumerate(developers):
            self.create_profile_card(scrollable_frame, dev, i)

        # Update scrollable region
        scrollable_frame.update_idletasks()

    def create_gradient_background(self):
        """Create a gradient background effect"""
        bg_canvas = Canvas(self.root, highlightthickness=0)
        bg_canvas.place(x=0, y=0, width=1510, height=770)

        # Create gradient
        for i in range(770):
            # Transition from light blue to white
            r = int(240 + (i / 770) * 15)  # 240 -> 255
            g = int(248 + (i / 770) * 7)  # 248 -> 255
            b = int(255)  # 255 -> 255

            color = f'#{r:02x}{g:02x}{b:02x}'
            bg_canvas.create_line(0, i, 1510, i, fill=color)

    def create_profile_card(self, parent, dev_data, index):
        """Create a profile card for a developer with a reveal LinkedIn button"""
        # Card frame with shadow effect
        card_frame = Frame(parent, bg="white", bd=0, highlightthickness=1, highlightbackground="#e0e0e0")
        card_frame.grid(row=index, column=0, padx=10, pady=10, sticky="ew")

        # Apply subtle hover effect
        card_frame.bind("<Enter>", lambda e, cf=card_frame: self.on_card_hover(cf, True))
        card_frame.bind("<Leave>", lambda e, cf=card_frame: self.on_card_hover(cf, False))

        # Developer icon (text-based since no images)
        dev_icon = Label(
            card_frame,
            text=dev_data["name"][0].upper(),  # First letter as icon
            font=Font(family="Helvetica", size=36, weight="bold"),
            bg="#3498db",
            fg="white",
            width=2,
            height=1
        )
        dev_icon.grid(row=0, column=0, rowspan=3, padx=15, pady=15)

        # Developer name with custom styling
        dev_name = Label(
            card_frame,
            text=dev_data["name"],
            font=self.subheading_font,
            bg="white",
            fg="#2c3e50"
        )
        dev_name.grid(row=0, column=1, padx=10, pady=(15, 5), sticky=W)

        # Developer role
        dev_role = Label(
            card_frame,
            text=dev_data["role"] + " - ENSAH",
            font=self.text_font,
            bg="white",
            fg="#7f8c8d"
        )
        dev_role.grid(row=1, column=1, padx=10, pady=5, sticky=W)

        # Create a frame for the LinkedIn content
        linkedin_frame = Frame(card_frame, bg="white")
        linkedin_frame.grid(row=2, column=1, padx=10, pady=(5, 15), sticky=W)

        # Initially hidden LinkedIn link
        linkedin_label = Label(
            linkedin_frame,
            text=dev_data["linkedin"],
            font=self.text_font,
            bg="white",
            fg="#0077b5",
            cursor="hand2"
        )
        linkedin_label.pack(pady=5)
        linkedin_label.bind("<Button-1>", lambda e, url=dev_data["linkedin"]: self.open_linkedin(url))

        # Hide the LinkedIn label initially
        linkedin_label.pack_forget()

        # Connect button
        connect_btn = Button(
            linkedin_frame,
            text="View LinkedIn Profile",
            font=self.button_font,
            bg="#0077b5",
            fg="white",
            bd=0,
            padx=10,
            cursor="hand2",
            activebackground="#00669c",
            activeforeground="white",
            command=lambda lbl=linkedin_label, btn=None: self.toggle_linkedin_view(lbl, btn)
        )
        connect_btn.pack(pady=5)
        # Store the button reference to use in toggle function
        connect_btn.config(command=lambda lbl=linkedin_label, btn=connect_btn: self.toggle_linkedin_view(lbl, btn))

        # Make the card expandable
        parent.grid_columnconfigure(0, weight=1)

    def toggle_linkedin_view(self, linkedin_label, button):
        """Toggle the LinkedIn link visibility when button is clicked"""
        if linkedin_label.winfo_viewable():
            linkedin_label.pack_forget()
            button.config(text="View LinkedIn Profile")
        else:
            linkedin_label.pack(before=button, pady=5)
            button.config(text="Hide LinkedIn Profile")

    def on_card_hover(self, card, is_hover):
        """Apply hover effect to developer card"""
        if is_hover:
            card.config(bg="#f8f9fa", highlightbackground="#c0c0c0")
            for child in card.winfo_children():
                if isinstance(child, Label) and child.cget("bg") != "#3498db":
                    child.config(bg="#f8f9fa")
                elif isinstance(child, Frame):
                    child.config(bg="#f8f9fa")
                    for subchild in child.winfo_children():
                        if isinstance(subchild, Label):
                            subchild.config(bg="#f8f9fa")
        else:
            card.config(bg="white", highlightbackground="#e0e0e0")
            for child in card.winfo_children():
                if isinstance(child, Label) and child.cget("bg") != "#3498db":
                    child.config(bg="white")
                elif isinstance(child, Frame):
                    child.config(bg="white")
                    for subchild in child.winfo_children():
                        if isinstance(subchild, Label):
                            subchild.config(bg="white")

    def open_linkedin(self, url):
        """Open LinkedIn profile in web browser"""
        if url:
            webbrowser.open_new(url)
        else:
            messagebox.showinfo("LinkedIn", "LinkedIn profile link will be available soon.")


if __name__ == "__main__":
    root = Tk()
    obj = Developer(root)
    root.mainloop()