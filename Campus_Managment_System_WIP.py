import customtkinter as ctk
from tkinter import messagebox

# --------------------------
# Setup theme
# --------------------------
ctk.set_appearance_mode("dark")   # Options: "light", "dark", "system"
ctk.set_default_color_theme("blue")  # You can also try: "green", "dark-blue"

# --------------------------
# Mock user data (temporary)
# --------------------------
users = {
    "admin@example.com": {"password": "admin123", "role": "Admin"},
}

# --------------------------
# Utility function
# --------------------------
def clear_window():
    for widget in app.winfo_children():
        widget.destroy()

# --------------------------
# LOGIN SCREEN
# --------------------------
def show_login():
    clear_window()
    app.title("Sign In")

    frame = ctk.CTkFrame(app, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(frame, text="Sign In", font=("Arial", 28, "bold")).grid(row=0, column=0, columnspan=2, pady=(20, 30))

    ctk.CTkLabel(frame, text="Email:", font=("Arial", 16)).grid(row=1, column=0, pady=10, padx=20, sticky="e")
    email_entry = ctk.CTkEntry(frame, width=300, placeholder_text="Enter your email")
    email_entry.grid(row=1, column=1, pady=10, padx=20)

    ctk.CTkLabel(frame, text="Password:", font=("Arial", 16)).grid(row=2, column=0, pady=10, padx=20, sticky="e")
    password_entry = ctk.CTkEntry(frame, width=300, show="*", placeholder_text="Enter your password")
    password_entry.grid(row=2, column=1, pady=10, padx=20)

    def login():
        email = email_entry.get()
        password = password_entry.get()
        if email in users and users[email]["password"] == password:
            role = users[email]["role"]
            messagebox.showinfo("Success", f"Welcome {email}! Role: {role}")
            if role == "Admin":
                show_admin_panel()
        else:
            messagebox.showerror("Error", "Invalid email or password.")

    ctk.CTkButton(frame, text="Sign In", width=200, command=login).grid(row=3, column=0, columnspan=2, pady=25)

    bottom_frame = ctk.CTkFrame(frame, fg_color="transparent")
    bottom_frame.grid(row=4, column=0, columnspan=2, pady=10)

    ctk.CTkButton(bottom_frame, text="Create Account", width=140, command=show_create_account).grid(row=0, column=0, padx=15)
    ctk.CTkButton(bottom_frame, text="Forgot Password", width=140, command=show_forgot_password).grid(row=0, column=1, padx=15)

# --------------------------
# CREATE ACCOUNT
# --------------------------
def show_create_account():
    clear_window()
    app.title("Create Account")

    frame = ctk.CTkFrame(app, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(frame, text="Create Account", font=("Arial", 28, "bold")).grid(row=0, column=0, columnspan=2, pady=(20, 30))

    fields = ["First Name", "Last Name", "Email", "Password"]
    entries = {}

    for i, label in enumerate(fields):
        ctk.CTkLabel(frame, text=f"{label}:", font=("Arial", 16)).grid(row=i+1, column=0, pady=10, padx=20, sticky="e")
        entry = ctk.CTkEntry(frame, width=300, placeholder_text=f"Enter your {label.lower()}")
        if label == "Password":
            entry.configure(show="*")
        entry.grid(row=i+1, column=1, pady=10, padx=20)
        entries[label] = entry

    def create_account():
        fname = entries["First Name"].get()
        lname = entries["Last Name"].get()
        email = entries["Email"].get()
        password = entries["Password"].get()

        if not all([fname, lname, email, password]):
            messagebox.showwarning("Warning", "All fields are required.")
        elif email in users:
            messagebox.showwarning("Warning", "Email already exists.")
        else:
            users[email] = {"password": password, "role": "User"}
            messagebox.showinfo("Success", "Account created successfully!")
            show_login()

    ctk.CTkButton(frame, text="Create Account", width=200, command=create_account).grid(row=6, column=0, columnspan=2, pady=25)
    ctk.CTkButton(frame, text="Back to Login", width=200, fg_color="gray", hover_color="dimgray", command=show_login).grid(row=7, column=0, columnspan=2, pady=(0, 20))

# --------------------------
# FORGOT PASSWORD
# --------------------------
def show_forgot_password():
    clear_window()
    app.title("Reset Password")

    frame = ctk.CTkFrame(app, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(frame, text="Reset Password", font=("Arial", 28, "bold")).grid(row=0, column=0, columnspan=2, pady=(20, 30))

    ctk.CTkLabel(frame, text="Email:", font=("Arial", 16)).grid(row=1, column=0, pady=10, padx=20, sticky="e")
    email_entry = ctk.CTkEntry(frame, width=300, placeholder_text="Enter your email")
    email_entry.grid(row=1, column=1, pady=10, padx=20)

    ctk.CTkLabel(frame, text="New Password:", font=("Arial", 16)).grid(row=2, column=0, pady=10, padx=20, sticky="e")
    new_pass_entry = ctk.CTkEntry(frame, width=300, show="*", placeholder_text="Enter new password")
    new_pass_entry.grid(row=2, column=1, pady=10, padx=20)

    def reset_password():
        email = email_entry.get()
        new_password = new_pass_entry.get()
        if email in users:
            users[email]["password"] = new_password
            messagebox.showinfo("Success", "Password updated successfully!")
            show_login()
        else:
            messagebox.showerror("Error", "Email not found.")

    ctk.CTkButton(frame, text="Update Password", width=200, command=reset_password).grid(row=3, column=0, columnspan=2, pady=25)
    ctk.CTkButton(frame, text="Back to Login", width=200, fg_color="gray", hover_color="dimgray", command=show_login).grid(row=4, column=0, columnspan=2, pady=(0, 20))

# --------------------------
# ADMIN PANEL
# --------------------------
def show_admin_panel():
    clear_window()
    app.title("Admin Panel")

    frame = ctk.CTkFrame(app, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(frame, text="Admin Panel", font=("Arial", 28, "bold")).grid(row=0, column=0, columnspan=2, pady=(20, 30))

    for i, (email, info) in enumerate(users.items(), start=1):
        ctk.CTkLabel(frame, text=f"{email} — Role: {info['role']}", font=("Arial", 16)).grid(row=i, column=0, columnspan=2, pady=5)

    ctk.CTkButton(frame, text="Back to Login", width=200, fg_color="gray", hover_color="dimgray", command=show_login).grid(row=i+1, column=0, columnspan=2, pady=30)

# --------------------------
# APP SETUP
# --------------------------
app = ctk.CTk()
app.geometry("1920x1080")
app.title("Modern Login System")
app.resizable(True, True)

show_login()
app.mainloop()