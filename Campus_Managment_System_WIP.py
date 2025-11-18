import customtkinter as ctk
from tkinter import messagebox   # <-- Needed for popup messages

# Temporary in-memory user database
users = {
    "test@example.com": {"first": "Test", "last": "User", "password": "1234", "role": "user"}
}

# Event database
events = {
    "Python Workshop": {"capacity": 30, "registered": 12},
    "Robotics Show": {"capacity": 100, "registered": 77},
    "AI Seminar": {"capacity": 50, "registered": 49},
    "Cloud Computing Lab": {"capacity": 25, "registered": 5},
}

# Store registrations
user_registrations = {}


# ------------------------------
# MAIN APPLICATION
# ------------------------------
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Event Registration System")
        self.geometry("1400x900")
        self.resizable(True, True)

        self.current_user = None

        self.login_page()

    # ------------------------------
    # LOGIN PAGE
    # ------------------------------
    def login_page(self):
        self.clear_window()

        frame = ctk.CTkFrame(self, width=600, height=400, corner_radius=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        title = ctk.CTkLabel(frame, text="Sign In", font=("Arial", 32, "bold"))
        title.pack(pady=20)

        self.login_email = ctk.CTkEntry(frame, placeholder_text="Email", width=350)
        self.login_email.pack(pady=10)

        self.login_password = ctk.CTkEntry(frame, placeholder_text="Password", width=350, show="*")
        self.login_password.pack(pady=10)

        login_btn = ctk.CTkButton(frame, text="Login", command=self.login_user)
        login_btn.pack(pady=20)

        create_btn = ctk.CTkButton(frame, text="Create Account", fg_color="#3a6ea5",
                                   command=self.create_account_page)
        create_btn.pack(pady=5)

        forgot_btn = ctk.CTkButton(frame, text="Forgot Password?", fg_color="gray20",
                                   command=self.forgot_password_page)
        forgot_btn.pack(pady=5)

    # Login logic
    def login_user(self):
        email = self.login_email.get()
        password = self.login_password.get()

        if email in users and users[email]["password"] == password:
            self.current_user = email
            if email not in user_registrations:
                user_registrations[email] = set()
            self.dashboard_page()
        else:
            messagebox.showerror("Error", "Invalid email or password")

    # ------------------------------
    # CREATE ACCOUNT PAGE
    # ------------------------------
    def create_account_page(self):
        self.clear_window()

        frame = ctk.CTkFrame(self, width=650, height=550, corner_radius=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        title = ctk.CTkLabel(frame, text="Create Account", font=("Arial", 30, "bold"))
        title.pack(pady=20)

        self.first_entry = ctk.CTkEntry(frame, placeholder_text="First Name", width=350)
        self.first_entry.pack(pady=10)

        self.last_entry = ctk.CTkEntry(frame, placeholder_text="Last Name", width=350)
        self.last_entry.pack(pady=10)

        self.email_entry = ctk.CTkEntry(frame, placeholder_text="Email", width=350)
        self.email_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(frame, placeholder_text="Password", width=350, show="*")
        self.password_entry.pack(pady=10)

        create_btn = ctk.CTkButton(frame, text="Create", command=self.create_account)
        create_btn.pack(pady=20)

        back_btn = ctk.CTkButton(frame, text="Back", fg_color="gray20",
                                 command=self.login_page)
        back_btn.pack(pady=10)

    def create_account(self):
        first = self.first_entry.get()
        last = self.last_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Validate fields
        if not all([first, last, email, password]):
            messagebox.showerror("Error", "All fields required.")
            return

        # Check if email exists
        if email in users:
            messagebox.showerror("Error", "Account already exists.")
            return

        # Create user
        users[email] = {
            "first": first,
            "last": last,
            "password": password,
            "role": "user"
        }

        messagebox.showinfo("Success", "Account created successfully!")

        self.login_page()

    # ------------------------------
    # FORGOT PASSWORD PAGE
    # ------------------------------
    def forgot_password_page(self):
        self.clear_window()

        frame = ctk.CTkFrame(self, width=600, height=350, corner_radius=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        title = ctk.CTkLabel(frame, text="Reset Password", font=("Arial", 28, "bold"))
        title.pack(pady=20)

        self.reset_email = ctk.CTkEntry(frame, placeholder_text="Enter your email")
        self.reset_email.pack(pady=10)

        reset_btn = ctk.CTkButton(frame, text="Send Reset Link", command=self.reset_password)
        reset_btn.pack(pady=20)

        back_btn = ctk.CTkButton(frame, text="Back", fg_color="gray20", command=self.login_page)
        back_btn.pack(pady=10)

    def reset_password(self):
        email = self.reset_email.get()

        if email not in users:
            messagebox.showerror("Error", "Email not found.")
            return

        messagebox.showinfo("Success", "Password reset instructions sent.")
        self.login_page()

    # ------------------------------
    # DASHBOARD PAGE
    # ------------------------------
    def dashboard_page(self):
        self.clear_window()

        title = ctk.CTkLabel(self, text="Available Events", font=("Arial", 32, "bold"))
        title.pack(pady=20)

        scroll = ctk.CTkScrollableFrame(self, width=1000, height=700)
        scroll.pack(pady=10)

        for event_name, data in events.items():
            self.build_event_row(scroll, event_name, data)

        logout_btn = ctk.CTkButton(self, text="Logout", fg_color="red", command=self.login_page)
        logout_btn.pack(pady=20)

    def build_event_row(self, parent, event_name, data):
        frame = ctk.CTkFrame(parent, height=100, corner_radius=15)
        frame.pack(fill="x", padx=20, pady=10)

        title = ctk.CTkLabel(frame, text=event_name, font=("Arial", 22, "bold"))
        title.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        remaining = data["capacity"] - data["registered"]

        spots = ctk.CTkLabel(frame, text=f"Available Spots: {remaining}", font=("Arial", 18))
        spots.grid(row=0, column=1, padx=20)

        user_events = user_registrations[self.current_user]

        if event_name in user_events:
            btn = ctk.CTkButton(frame, text="Cancel Registration",
                                fg_color="red", hover_color="#992222",
                                command=lambda e=event_name: self.cancel_event(e))
        else:
            btn = ctk.CTkButton(frame, text="Register",
                                fg_color="green", hover_color="#0f6",
                                command=lambda e=event_name: self.register_event(e))

        btn.grid(row=0, column=2, padx=20)

    # Register / Cancel logic
    def register_event(self, event_name):
        event = events[event_name]

        if event["registered"] >= event["capacity"]:
            messagebox.showerror("Full", "This event is full.")
            return

        event["registered"] += 1
        user_registrations[self.current_user].add(event_name)
        self.dashboard_page()

    def cancel_event(self, event_name):
        event = events[event_name]

        event["registered"] -= 1
        user_registrations[self.current_user].remove(event_name)
        self.dashboard_page()

    # Clear the window
    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()


# Run app
app = App()
app.mainloop()