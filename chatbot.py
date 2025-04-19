from tkinter import *
from tkinter import ttk, messagebox, font
from PIL import Image, ImageTk
import ollama
import time
import threading
import os
import datetime
import json


class ChatBot:
    def __init__(self, root):
        self.root = root
        self.root.title("ATTENDIFY AI")
        self.root.geometry("1100x700+200+50")  # Wider to accommodate sidebar
        self.root.configure(bg='#f5f5f5')
        self.root.iconbitmap('chatbot_images/icon.ico') if os.path.exists('chatbot_images/icon.ico') else None
        self.root.bind('<Return>', self.enter_func)

        # Custom font
        self.custom_font = font.Font(family="Segoe UI", size=11)
        self.title_font = font.Font(family="Segoe UI", size=24, weight="bold")
        self.sidebar_font = font.Font(family="Segoe UI", size=10)
        self.sidebar_title_font = font.Font(family="Segoe UI", size=12, weight="bold")

        # Chat history
        self.chat_history = []
        self.history_file = "chat_history.json"
        self.conversations = {}  # Dictionary to store multiple conversations
        self.current_conversation_id = None
        self.conversations_file = "conversations.json"
        self.load_conversations()

        # Model selection
        self.available_models = ["deepseek-r1", "llama3", "mistral", "phi3"]
        self.selected_model = StringVar(value=self.available_models[0])

        # Create main container
        main_container = Frame(self.root, bg='#f5f5f5')
        main_container.pack(fill=BOTH, expand=True)

        # Sidebar for conversations
        self.sidebar_frame = Frame(main_container, bg='#f0f0f0', width=200, relief=RIDGE, bd=1)
        self.sidebar_frame.pack(side=LEFT, fill=Y, padx=(10, 0), pady=10)
        self.sidebar_frame.pack_propagate(False)  # Prevent frame from shrinking

        # Sidebar header
        sidebar_header = Frame(self.sidebar_frame, bg='#f0f0f0', height=50)
        sidebar_header.pack(fill=X, pady=(10, 5))

        # New chat button
        self.new_chat_button = Button(sidebar_header, text="+ New Chat", command=self.new_conversation,
                                      font=self.sidebar_font, bg='#2E7D32', fg='white',
                                      activebackground='#388E3C', activeforeground='white',
                                      cursor="hand2", bd=0, relief=RAISED, padx=10)
        self.new_chat_button.pack(fill=X, padx=10)

        # Conversations title
        conversations_title = Label(self.sidebar_frame, text="Conversations", font=self.sidebar_title_font,
                                    bg='#f0f0f0', fg='#333333')
        conversations_title.pack(fill=X, padx=10, pady=(10, 5), anchor=W)

        # Conversations list frame with scrollbar
        self.conversations_frame = Frame(self.sidebar_frame, bg='#f0f0f0')
        self.conversations_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

        self.conversations_canvas = Canvas(self.conversations_frame, bg='#f0f0f0', highlightthickness=0)
        self.conversations_scrollbar = ttk.Scrollbar(self.conversations_frame, orient=VERTICAL,
                                                     command=self.conversations_canvas.yview)
        self.conversations_scrollbar.pack(side=RIGHT, fill=Y)
        self.conversations_canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.conversations_canvas.configure(yscrollcommand=self.conversations_scrollbar.set)

        self.conversations_list = Frame(self.conversations_canvas, bg='#f0f0f0')
        self.conversations_canvas.create_window((0, 0), window=self.conversations_list, anchor=NW)
        self.conversations_list.bind("<Configure>", lambda e: self.conversations_canvas.configure(
            scrollregion=self.conversations_canvas.bbox("all")))

        # Chat container with padding
        container = Frame(main_container, bg='#f5f5f5')
        container.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

        # Header Frame
        header_frame = Frame(container, bg='#ffffff', relief=RIDGE, bd=1)
        header_frame.pack(fill=X, pady=(0, 15))

        # Load logo
        try:
            img_chat = Image.open("chatbot_images/chatbot.png")
            img_chat = img_chat.resize((60, 60))
            self.photoimg = ImageTk.PhotoImage(img_chat)
            logo_label = Label(header_frame, image=self.photoimg, bg='#ffffff')
            logo_label.pack(side=LEFT, padx=20, pady=10)
        except Exception as e:
            print(f"Could not load logo: {e}")
            self.photoimg = None

        # Title
        title_label = Label(header_frame, text="ATTENDIFY AI", font=self.title_font, fg='#051729', bg='#ffffff')
        title_label.pack(side=LEFT, padx=10, pady=10)

        # Model selection dropdown
        model_frame = Frame(header_frame, bg='#ffffff')
        model_frame.pack(side=RIGHT, padx=20, pady=10)

        model_label = Label(model_frame, text="Model:", font=self.custom_font, bg='#ffffff', fg='#555555')
        model_label.pack(side=LEFT, padx=(0, 5))

        model_dropdown = ttk.Combobox(model_frame, textvariable=self.selected_model, values=self.available_models,
                                      font=self.custom_font, width=12, state="readonly")
        model_dropdown.pack(side=LEFT)

        # Style configuration for ttk widgets
        style = ttk.Style()
        style.configure("TScrollbar", background="#dddddd", troughcolor="#f0f0f0",
                        arrowcolor="#555555", bordercolor="#dddddd")
        style.configure("TCombobox", background="#ffffff", fieldbackground="#ffffff")

        # Chat Frame
        chat_frame = Frame(container, bg='#ffffff', relief=RIDGE, bd=1)
        chat_frame.pack(fill=BOTH, expand=True)

        # Chat Display Area with improved scrollbar
        self.scroll_y = ttk.Scrollbar(chat_frame, orient=VERTICAL, style="TScrollbar")
        self.scroll_y.pack(side=RIGHT, fill=Y)

        self.text = Text(chat_frame, width=80, height=20, bd=0, relief=FLAT,
                         font=self.custom_font, yscrollcommand=self.scroll_y.set,
                         wrap=WORD, bg='#ffffff', fg='#333333', padx=10, pady=10)
        self.scroll_y.config(command=self.text.yview)
        self.text.pack(fill=BOTH, expand=True)

        # Configure tags for bubble messages
        self.text.tag_configure('user', background='#348feb', foreground='white',
                                justify='right', lmargin1=200, lmargin2=200, rmargin=20,
                                spacing3=10, relief='solid', borderwidth=1)

        self.text.tag_configure('bot', background='#f0f0f0', foreground='#333333',
                                justify='left', lmargin1=20, lmargin2=20, rmargin=200,
                                spacing3=10, relief='solid', borderwidth=1)

        self.text.tag_configure('user_time', foreground='#888888', justify='right',
                                spacing3=2, font=(self.custom_font.name, 8))

        self.text.tag_configure('bot_time', foreground='#888888', justify='left',
                                spacing3=2, font=(self.custom_font.name, 8))

        self.text.tag_configure('typing', foreground='#888888',
                                font=(self.custom_font.name, self.custom_font.cget('size'), 'italic'))

        self.text.tag_configure('error', foreground='#e53935',
                                font=(self.custom_font.name, self.custom_font.cget('size')))

        self.text.tag_configure('welcome', background='#e8f5e9', foreground='#1b5e20',
                                justify='left', lmargin1=20, lmargin2=20, rmargin=20,
                                spacing3=10, relief='solid', borderwidth=1, font=(self.custom_font.name, 12, 'bold'))

        # Input Frame with rounded appearance
        input_frame = Frame(container, bg='#ffffff', relief=RIDGE, bd=1, height=120)
        input_frame.pack(fill=X, pady=(15, 0))

        # Entry Field - Multiline
        entry_frame = Frame(input_frame, bg='#ffffff', padx=10, pady=10)
        entry_frame.pack(fill=BOTH, expand=True)

        self.entry = Text(entry_frame, width=50, height=3, font=self.custom_font,
                          bg='#f9f9f9', fg='#333333', relief=FLAT, padx=10, pady=10)
        self.entry.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))

        # Buttons Frame
        button_frame = Frame(entry_frame, bg='#ffffff')
        button_frame.pack(side=RIGHT, fill=Y)

        # Send Button
        self.send_button = Button(button_frame, text="Send", command=self.send,
                                  font=self.custom_font, width=10, height=1,
                                  bg='#2E7D32', fg='#ffffff', bd=0, relief=RAISED,
                                  activebackground='#388E3C', activeforeground='#ffffff',
                                  cursor="hand2")
        self.send_button.pack(pady=(0, 5))

        # Clear Button
        self.clear_button = Button(button_frame, text="Clear", command=self.clear,
                                   font=self.custom_font, width=10, height=1,
                                   bg='#f44336', fg='#ffffff', bd=0, relief=RAISED,
                                   activebackground='#e53935', activeforeground='#ffffff',
                                   cursor="hand2")
        self.clear_button.pack(pady=(0, 5))

        # Delete All Button
        self.delete_all_button = Button(button_frame, text="Delete All", command=self.delete_all,
                                        font=self.custom_font, width=10, height=1,
                                        bg='#d32f2f', fg='#ffffff', bd=0, relief=RAISED,
                                        activebackground='#c62828', activeforeground='#ffffff',
                                        cursor="hand2")
        self.delete_all_button.pack(pady=(0, 5))

        # Save Button
        self.save_button = Button(button_frame, text="Save", command=self.save_chat,
                                  font=self.custom_font, width=10, height=1,
                                  bg='#1976D2', fg='#ffffff', bd=0, relief=RAISED,
                                  activebackground='#1565C0', activeforeground='#ffffff',
                                  cursor="hand2")
        self.save_button.pack()

        # Status Bar
        self.status_var = StringVar()
        self.status_bar = Label(container, textvariable=self.status_var,
                                font=(self.custom_font.name, 9), fg='#888888', bg='#f5f5f5',
                                anchor=W)
        self.status_bar.pack(fill=X, pady=(5, 0))
        self.status_var.set("Ready")

        # Start a new conversation if none exist
        if not self.conversations:
            self.new_conversation()
        else:
            # Load the most recent conversation
            self.update_conversations_list()
            last_conv_id = list(self.conversations.keys())[-1]
            self.load_conversation(last_conv_id)

    def new_conversation(self):
        """Create a new conversation"""
        # Generate a new conversation ID
        conv_id = f"conv_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Create a new conversation entry
        self.conversations[conv_id] = {
            "created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "title": f"New Chat ({datetime.datetime.now().strftime('%H:%M')})",
            "messages": []
        }

        # Set as current conversation
        self.current_conversation_id = conv_id
        self.chat_history = []

        # Clear the chat display
        self.text.delete('1.0', END)

        # Display welcome message with typing effect
        threading.Thread(target=self.display_welcome_message_with_typing, daemon=True).start()

        # Update the conversations list in the sidebar
        self.update_conversations_list()

        # Save conversations
        self.save_conversations()

    def display_welcome_message_with_typing(self):
        """Display a welcome message with typing animation"""
        welcome_message = "Hello! I'm ATTENDIFY chatbot. How can I help you with your face recognition attendance system today?"
        current_time = datetime.datetime.now().strftime("%H:%M")

        # Add typing indicator
        self.text.insert(END, "\nBot is typing...\n", 'typing')
        self.text.see(END)

        time.sleep(0.5)  # Simulate initial delay

        # Remove the typing indicator
        self.text.delete('end-2l', 'end')

        # Insert welcome tag
        self.text.insert(END, f"\n", 'welcome')

        # Type out the message character by character
        for char in welcome_message:
            self.text.insert(END, char, 'welcome')
            self.text.see(END)
            time.sleep(0.03)  # Adjust typing speed here

            # Update the root to show typing in real-time
            self.root.update_idletasks()

        self.text.insert(END, "\n", 'welcome')
        self.text.insert(END, f"{current_time}\n", 'bot_time')
        self.text.see(END)

        # Add this welcome message to conversation history
        if self.current_conversation_id:
            message = {
                "role": "assistant",
                "content": welcome_message,
                "time": current_time,
                "model": self.selected_model.get()
            }
            self.chat_history.append(message)
            self.conversations[self.current_conversation_id]["messages"] = self.chat_history

            # Update the conversation title with first few words of welcome message
            title_text = welcome_message.split()[:3]
            title = " ".join(title_text) + "..."
            self.conversations[self.current_conversation_id]["title"] = title

            # Save and update
            self.save_conversations()
            self.update_conversations_list()

    def load_conversations(self):
        """Load all conversations from file"""
        try:
            if os.path.exists(self.conversations_file):
                with open(self.conversations_file, "r", encoding="utf-8") as file:
                    self.conversations = json.load(file)
        except Exception as e:
            print(f"Error loading conversations: {e}")
            self.conversations = {}

    def save_conversations(self):
        """Save all conversations to file"""
        try:
            with open(self.conversations_file, "w", encoding="utf-8") as file:
                json.dump(self.conversations, file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving conversations: {e}")

    def update_conversations_list(self):
        """Update the conversations list in the sidebar"""
        # Clear existing items
        for widget in self.conversations_list.winfo_children():
            widget.destroy()

        # Add conversation items in reverse order (newest first)
        for conv_id in reversed(list(self.conversations.keys())):
            conv = self.conversations[conv_id]

            # Create frame for each conversation
            conv_frame = Frame(self.conversations_list, bg='#f0f0f0', pady=5)
            conv_frame.pack(fill=X, padx=5, pady=2)

            # Conversation button with title
            title_text = conv["title"]
            if len(title_text) > 23:
                title_text = title_text[:20] + "..."

            bg_color = '#d4edda' if conv_id == self.current_conversation_id else '#f0f0f0'
            conv_button = Button(conv_frame, text=title_text, font=self.sidebar_font,
                                 anchor=W, bg=bg_color, fg='#333333', bd=0,
                                 relief=FLAT, padx=5, pady=5,
                                 command=lambda cid=conv_id: self.load_conversation(cid))
            conv_button.pack(side=LEFT, fill=X, expand=True)

            # Delete button
            delete_button = Button(conv_frame, text="×", font=self.sidebar_font,
                                   bg=bg_color, fg='#cc0000', bd=0,
                                   relief=FLAT, padx=5, pady=0,
                                   command=lambda cid=conv_id: self.delete_conversation(cid))
            delete_button.pack(side=RIGHT)

        # Update the canvas
        self.conversations_list.update_idletasks()
        self.conversations_canvas.configure(scrollregion=self.conversations_canvas.bbox("all"))

    def load_conversation(self, conv_id):
        """Load a specific conversation"""
        if conv_id in self.conversations:
            # Set as current conversation
            self.current_conversation_id = conv_id
            self.chat_history = self.conversations[conv_id]["messages"]

            # Display conversation messages
            self.display_chat_history()

            # Update UI
            self.update_conversations_list()
            self.status_var.set(f"Loaded conversation from {self.conversations[conv_id]['created']}")

    def delete_conversation(self, conv_id):
        """Delete a specific conversation"""
        if messagebox.askyesno("Delete Conversation", "Do you want to delete this conversation?"):
            if conv_id in self.conversations:
                # Delete the conversation
                del self.conversations[conv_id]

                # If we deleted the current conversation, load another one or create new
                if conv_id == self.current_conversation_id:
                    if self.conversations:
                        new_current = list(self.conversations.keys())[-1]
                        self.load_conversation(new_current)
                    else:
                        self.new_conversation()

                # Update UI
                self.update_conversations_list()
                self.save_conversations()
                self.status_var.set("Conversation deleted")

    def enter_func(self, event):
        # Only send if Shift+Enter is not pressed
        if not (event.state & 0x1):  # Check if shift is not pressed
            self.send()
            return "break"  # Prevents the default behavior

    def clear(self):
        """Clear current conversation but keep history"""
        if messagebox.askyesno("Clear Confirmation", "Do you want to clear the current chat?"):
            self.text.delete('1.0', END)
            self.entry.delete('1.0', END)
            # Display welcome message with typing effect
            threading.Thread(target=self.display_welcome_message_with_typing, daemon=True).start()
            self.status_var.set("Chat cleared")

    def delete_all(self):
        """Delete all conversation history and start fresh"""
        if messagebox.askyesno("Delete All Confirmation",
                               "Do you want to delete all conversations? This action cannot be undone."):
            # Clear text widgets
            self.text.delete('1.0', END)
            self.entry.delete('1.0', END)

            # Clear all conversations
            self.conversations = {}
            self.chat_history = []

            # Delete history files if they exist
            for file_path in [self.history_file, self.conversations_file]:
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        print(f"Error deleting file {file_path}: {e}")

            # Create a new conversation
            self.new_conversation()

            self.status_var.set("All conversations deleted")

    def send(self):
        user_input = self.entry.get('1.0', END).strip()
        if not user_input:
            self.status_var.set("Please enter some input")
            return

        # Clear entry field
        self.entry.delete('1.0', END)

        # Get current time
        current_time = datetime.datetime.now().strftime("%H:%M")

        # Display user message
        self.text.insert(END, f"\n", 'user')
        self.text.insert(END, f"{user_input}\n", 'user')
        self.text.insert(END, f"{current_time}\n", 'user_time')
        self.text.see(END)

        # Store in chat history
        self.chat_history.append({"role": "user", "content": user_input, "time": current_time})

        # If this is the first user message, update the conversation title
        if self.current_conversation_id and len(self.chat_history) == 2:  # 1 welcome message + 1 user message
            title_words = user_input.split()[:3]
            title = " ".join(title_words)
            if len(title) > 20:
                title = title[:20] + "..."
            self.conversations[self.current_conversation_id]["title"] = title
            self.update_conversations_list()

        # Save to current conversation
        if self.current_conversation_id:
            self.conversations[self.current_conversation_id]["messages"] = self.chat_history
            self.save_conversations()

        # Disable buttons while processing
        self.toggle_input_state(DISABLED)
        self.status_var.set("Processing...")

        # Start a new thread for the bot's response
        threading.Thread(target=self.bot_response, args=(user_input,), daemon=True).start()

    def bot_response(self, user_input):
        try:
            # Simulate typing effect
            self.text.insert(END, "\nBot is typing...\n", 'typing')
            self.text.see(END)

            # Get current model
            model = self.selected_model.get()

            # Use Ollama to generate a response
            start_time = time.time()
            response = ollama.generate(
                model=model,
                prompt=user_input,
                options={"temperature": 0.7, "top_k": 50, "top_p": 0.95}
            )

            # Clean response
            bot_response = response['response'].replace('<think>', '').replace('</think>', '')

            # Remove first 3 lines if they exist
            response_lines = bot_response.split('\n')
            if len(response_lines) > 3:
                bot_response = '\n'.join(response_lines[3:])

            # Calculate response time
            elapsed_time = time.time() - start_time

            # Remove the "Bot is typing..." message
            self.text.delete('end-2l', 'end')

            # Get current time
            current_time = datetime.datetime.now().strftime("%H:%M")

            # Display bot response
            self.text.insert(END, "\n", 'bot')

            # Display character by character (with reduced delay for better UX)
            for char in bot_response:
                self.text.insert(END, char, 'bot')
                self.text.see(END)
                time.sleep(0.005)  # Reduced typing speed for better UX
                # Update the root to show typing in real-time
                self.root.update_idletasks()

            self.text.insert(END, "\n", 'bot')
            self.text.insert(END, f"{current_time} ({elapsed_time:.1f}s)\n", 'bot_time')

            # Store in chat history
            self.chat_history.append({
                "role": "assistant",
                "content": bot_response,
                "time": current_time,
                "model": model
            })

            # Update current conversation
            if self.current_conversation_id:
                self.conversations[self.current_conversation_id]["messages"] = self.chat_history
                self.save_conversations()

            self.status_var.set(f"Response generated with {model} in {elapsed_time:.1f}s")

        except Exception as e:
            self.text.delete('end-2l', 'end')
            error_msg = f"Error generating response: {str(e)}"
            self.text.insert(END, f"\n{error_msg}\n", 'error')
            self.status_var.set("Error occurred")

        # Re-enable buttons
        self.toggle_input_state(NORMAL)

    def toggle_input_state(self, state):
        self.entry.config(state=state)
        self.send_button.config(state=state)
        self.clear_button.config(state=state)
        self.delete_all_button.config(state=state)
        self.save_button.config(state=state)

    def save_chat(self):
        try:
            # Create a timestamped filename
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"chat_{timestamp}.txt"

            with open(filename, "w", encoding="utf-8") as file:
                file.write(f"===== Chat saved at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} =====\n\n")

                for msg in self.chat_history:
                    role = "You" if msg["role"] == "user" else "Assistant"
                    file.write(f"{role} ({msg['time']}):\n{msg['content']}\n\n")

            self.status_var.set(f"Chat saved to {filename}")
            messagebox.showinfo("Save successful", f"Chat has been saved to {filename}")

        except Exception as e:
            self.status_var.set(f"Error saving chat: {str(e)}")
            messagebox.showerror("Save Error", f"Could not save chat: {str(e)}")

    def save_chat_history(self):
        try:
            with open(self.history_file, "w", encoding="utf-8") as file:
                json.dump(self.chat_history, file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving chat history: {e}")

    def load_chat_history(self):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, "r", encoding="utf-8") as file:
                    self.chat_history = json.load(file)
        except Exception as e:
            print(f"Error loading chat history: {e}")
            self.chat_history = []

    def display_chat_history(self):
        if not self.chat_history:
            self.display_welcome_message_with_typing()
            return

        # Clear existing text first
        self.text.delete('1.0', END)

        for msg in self.chat_history:
            if msg["role"] == "user":
                self.text.insert(END, f"\n", 'user')
                self.text.insert(END, f"{msg['content']}\n", 'user')
                self.text.insert(END, f"{msg['time']}\n", 'user_time')
            else:
                self.text.insert(END, f"\n", 'bot')
                self.text.insert(END, f"{msg['content']}\n", 'bot')

                # Display model info if available
                time_text = msg['time']
                if 'model' in msg:
                    time_text += f" ({msg['model']})"
                self.text.insert(END, f"{time_text}\n", 'bot_time')

        self.text.see(END)


def process_model_response(response_text):
    """
    Process the model's response to remove the first 3 lines.
    Used when loading models other than Ollama.
    """
    lines = response_text.split('\n')
    if len(lines) > 3:
        return '\n'.join(lines[3:])
    return response_text


if __name__ == '__main__':
    # Create necessary directories
    os.makedirs("chatbot_images", exist_ok=True)

    root = Tk()
    obj = ChatBot(root)
    root.mainloop()