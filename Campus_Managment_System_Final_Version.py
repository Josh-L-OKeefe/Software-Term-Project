import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
from mysql.connector import errorcode
import hashlib
import datetime


# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "12345",
    "database": "event_system" 
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def hash_password(password: str) -> str:
    """Return a SHA-256 hex digest of the password."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def is_valid_email(email: str) -> bool:
    email = email.strip()
    if "@" not in email or "." not in email:
        return False
    try:
        return email.index("@") < email.rindex(".")
    except ValueError:
        return False
    
# Setup DB (create tables if not exist)
def init_db():
    cnx = None
    try:
        cnx = get_db()
        cursor = cnx.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                userid INT AUTO_INCREMENT PRIMARY KEY,
                firstName VARCHAR(100),
                lastName VARCHAR(100),
                email VARCHAR(255) UNIQUE,
                userPassword VARCHAR(255),
                permissions BOOLEAN DEFAULT FALSE
            );
        """)
        # Create Events table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Events (
                eid INT AUTO_INCREMENT PRIMARY KEY,
                eventName VARCHAR(255),
                eventDate DATE,
                eventTime TIME,
                eventLocation VARCHAR(255),
                eventDescription TEXT,
                eventCapacity INT
            );
        """)
        # Create Rooms table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Rooms (
                rid INT PRIMARY KEY,
                roomAvailability BOOLEAN
            );
        """)
        # Create Registrations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Registrations (
                regid INT AUTO_INCREMENT PRIMARY KEY,
                userid INT,
                eid INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (userid) REFERENCES Users(userid) ON DELETE CASCADE,
                FOREIGN KEY (eid) REFERENCES Events(eid) ON DELETE CASCADE,
                UNIQUE KEY uniq_user_event (userid, eid)
            );
        """)
        cnx.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print("Error initializing DB:", err)
        raise
    finally:
        if cnx:
            cnx.close()
try:
    init_db()
except Exception as e:
    print("Failed to initialize database. Please check DB connection and config.")
    print(e)

# Main Application:
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Event Registration System (MySQL)")
        self.geometry("1200x800")
        self.resizable(True, True)

        self.current_user_email = None
        self.current_user_id = None
        self.current_user_permissions = False

        self.login_page()

    # Login Page:
    def login_page(self):
        self.clear_window()

        frame = ctk.CTkFrame(self, width=600, height=420, corner_radius=12)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="Sign In", font=("Arial", 30, "bold")).pack(pady=18)

        self.login_email = ctk.CTkEntry(frame, placeholder_text="Email", width=380)
        self.login_email.pack(pady=8)

        self.login_password = ctk.CTkEntry(frame, placeholder_text="Password", width=380, show="*")
        self.login_password.pack(pady=8)

        ctk.CTkButton(frame, text="Login", width=200, command=self.login_user).pack(pady=12)

        btn_row = ctk.CTkFrame(frame)
        btn_row.pack(pady=8)
        ctk.CTkButton(btn_row, text="Create Account", command=self.create_account_page, width=160).grid(row=0, column=0, padx=8)
        ctk.CTkButton(btn_row, text="Forgot Password?", command=self.forgot_password_page, width=160, fg_color="gray20").grid(row=0, column=1, padx=8)

    def login_user(self):
        email = self.login_email.get().strip()
        password = self.login_password.get()

        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password.")
            return
        hashed = hash_password(password)
        try:
            cnx = get_db()
            cursor = cnx.cursor(dictionary=True)
            cursor.execute("SELECT userid, email, userPassword, permissions FROM Users WHERE email = %s", (email,))
            row = cursor.fetchone()
            cursor.close()
            cnx.close()
        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", f"Database connection error: {err}")
            return

        if not row:
            messagebox.showerror("Error", "Invalid email or password.")
            return

        if row["userPassword"] != hashed:
            messagebox.showerror("Error", "Invalid email or password.")
            return
        self.current_user_email = row["email"]
        self.current_user_id = row["userid"]
        self.current_user_permissions = bool(row["permissions"])
        self.my_events_page()

    # Create Account Page
    def create_account_page(self):
        self.clear_window()

        frame = ctk.CTkFrame(self, width=700, height=520, corner_radius=12)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="Create Account", font=("Arial", 28, "bold")).pack(pady=12)

        self.ca_first = ctk.CTkEntry(frame, placeholder_text="First name", width=420)
        self.ca_first.pack(pady=8)
        self.ca_last = ctk.CTkEntry(frame, placeholder_text="Last name", width=420)
        self.ca_last.pack(pady=8)
        self.ca_email = ctk.CTkEntry(frame, placeholder_text="Email", width=420)
        self.ca_email.pack(pady=8)
        self.ca_password = ctk.CTkEntry(frame, placeholder_text="Password", width=420, show="*")
        self.ca_password.pack(pady=8)

        ctk.CTkButton(frame, text="Create Account", command=self.create_account, width=240).pack(pady=12)
        ctk.CTkButton(frame, text="Back", command=self.login_page, width=120, fg_color="gray20").pack(pady=6)

    def create_account(self):
        first = self.ca_first.get().strip()
        last = self.ca_last.get().strip()
        email = self.ca_email.get().strip()
        password = self.ca_password.get()

        if not all([first, last, email, password]):
            messagebox.showerror("Error", "All fields required.")
            return

        if not is_valid_email(email):
            messagebox.showerror("Error", "Invalid email format.")
            return

        hashed = hash_password(password)
        try:
            cnx = get_db()
            cursor = cnx.cursor()
            cursor.execute("SELECT userid FROM Users WHERE email = %s", (email,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Account already exists with that email.")
                cursor.close()
                cnx.close()
                return

            sql = "INSERT INTO Users (firstName, lastName, email, userPassword, permissions) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (first, last, email, hashed, False))
            cnx.commit()
            cursor.close()
            cnx.close()
            messagebox.showinfo("Success", "Account created successfully!")
            self.login_page()
        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", f"Could not create account: {err}")

    #Forgot Password Page
    def forgot_password_page(self):
        self.clear_window()
        frame = ctk.CTkFrame(self, width=600, height=260, corner_radius=12)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="Reset Password", font=("Arial", 22, "bold")).pack(pady=12)
        self.fp_email = ctk.CTkEntry(frame, placeholder_text="Enter your email", width=420)
        self.fp_email.pack(pady=8)
        ctk.CTkButton(frame, text="Send Reset", command=self.reset_password, width=220).pack(pady=12)
        ctk.CTkButton(frame, text="Back", command=self.login_page, width=120, fg_color="gray20").pack(pady=6)

    def reset_password(self):
        email = self.fp_email.get().strip()
        if not email:
            messagebox.showerror("Error", "Please enter your email.")
            return

        try:
            cnx = get_db()
            cursor = cnx.cursor()
            cursor.execute("SELECT userid FROM Users WHERE email = %s", (email,))
            if not cursor.fetchone():
                messagebox.showerror("Error", "Email not found.")
                cursor.close()
                cnx.close()
                return
            cursor.close()
            cnx.close()
            messagebox.showinfo("Success", "Password reset instructions sent (demo).")
            self.login_page()
        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", f"Database error: {err}")

    # My events page
    def my_events_page(self):
        self.clear_window()

        header = ctk.CTkLabel(self, text="My Registered Events", font=("Arial", 26, "bold"))
        header.pack(pady=12)

        # Fetch user's registrations from DB
        regs = []
        try:
            cnx = get_db()
            cursor = cnx.cursor(dictionary=True)
            cursor.execute("""
                SELECT r.regid, e.eid, e.eventName, e.eventDate, e.eventTime, e.eventLocation
                FROM Registrations r
                JOIN Events e ON r.eid = e.eid
                WHERE r.userid = %s
                ORDER BY e.eventDate, e.eventTime
            """, (self.current_user_id,))
            regs = cursor.fetchall()
            cursor.close()
            cnx.close()
        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", f"Failed to load registrations: {err}")
            return

        scroll = ctk.CTkScrollableFrame(self, width=1000, height=560)
        scroll.pack(pady=10)

        if not regs:
            ctk.CTkLabel(scroll, text="You are not registered for any events.", font=("Arial", 18)).pack(pady=20)
        else:
            for r in regs:
                f = ctk.CTkFrame(scroll, corner_radius=10)
                f.pack(fill="x", padx=16, pady=8)
                n = f"{r['eventName']} — {r['eventDate'].strftime('%Y-%m-%d')} {str(r['eventTime'])}"
                ctk.CTkLabel(f, text=n, font=("Arial", 18, "bold")).pack(side="left", padx=12, pady=10)
                ctk.CTkButton(f, text="Cancel Registration", fg_color="red",
                              command=lambda regid=r['regid'], eid=r['eid']: self.cancel_registration(regid, eid)).pack(side="right", padx=12)

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=12)
        ctk.CTkButton(btn_frame, text="Browse Events", fg_color="green", command=self.dashboard_page, width=180).grid(row=0, column=0, padx=8)
        ctk.CTkButton(btn_frame, text="Logout", fg_color="red", command=self.logout, width=120).grid(row=0, column=1, padx=8)

    # Cancel registration
    def cancel_registration(self, regid: int, eid: int):
        try:
            cnx = get_db()
            cursor = cnx.cursor()
            cursor.execute("DELETE FROM Registrations WHERE regid = %s", (regid,))
            cnx.commit()
            cursor.close()
            cnx.close()
            messagebox.showinfo("Success", "Registration cancelled.")
            self.my_events_page()
        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", f"Could not cancel registration: {err}")

    # Dashboard (Browse Events) + User Create Event Button
    def dashboard_page(self):
        self.clear_window()

        ctk.CTkLabel(self, text="Available Events", font=("Arial", 28, "bold")).pack(pady=12)

        # Load events from Database
        events = []
        try:
            cnx = get_db()
            cursor = cnx.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Events ORDER BY eventDate, eventTime")
            events = cursor.fetchall()
            cursor.close()
            cnx.close()
        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", f"Failed to load events: {err}")
            return

        scroll = ctk.CTkScrollableFrame(self, width=1000, height=560)
        scroll.pack(pady=10)

        registered_eids = set()
        try:
            cnx = get_db()
            cursor = cnx.cursor()
            cursor.execute("SELECT eid FROM Registrations WHERE userid = %s", (self.current_user_id,))
            rows = cursor.fetchall()
            registered_eids = {r[0] for r in rows}
            cursor.close()
            cnx.close()
        except mysql.connector.Error:
            registered_eids = set()

        for evt in events:
            f = ctk.CTkFrame(scroll, corner_radius=10)
            f.pack(fill="x", padx=16, pady=8)
            name = evt['eventName']
            date = evt['eventDate'].strftime("%Y-%m-%d") if isinstance(evt['eventDate'], datetime.date) else str(evt['eventDate'])
            time = str(evt['eventTime'])
            loc = evt['eventLocation'] or ""
            cap = evt['eventCapacity'] or 0

            try:
                cnx = get_db()
                cursor = cnx.cursor()
                cursor.execute("SELECT COUNT(*) FROM Registrations WHERE eid = %s", (evt['eid'],))
                cur_reg = cursor.fetchone()[0]
                cursor.close()
                cnx.close()
            except mysql.connector.Error:
                cur_reg = 0

            remaining = cap - cur_reg

            left_text = f"{name} — {date} {time} @ {loc}"
            ctk.CTkLabel(f, text=left_text, font=("Arial", 16, "bold")).grid(row=0, column=0, sticky="w", padx=12, pady=6)
            ctk.CTkLabel(f, text=f"Available Spots: {remaining}", font=("Arial", 14)).grid(row=0, column=1, padx=12)

            if evt['eid'] in registered_eids:
                ctk.CTkButton(f, text="Registered", fg_color="gray20", state="disabled").grid(row=0, column=2, padx=12)
            else:
                btn = ctk.CTkButton(f, text="Register", fg_color="green",
                                    command=lambda eid=evt['eid'], cap=cap, cur_reg=cur_reg: self.register_event(eid, cap, cur_reg))
                btn.grid(row=0, column=2, padx=12)

        # Bottom buttons
        bframe = ctk.CTkFrame(self)
        bframe.pack(pady=12)
        ctk.CTkButton(bframe, text="Home", fg_color="#3a6ea5", command=self.my_events_page, width=160).grid(row=0, column=0, padx=8)
        ctk.CTkButton(bframe, text="Create Event", fg_color="orange", command=self.user_create_event_page, width=160).grid(row=0, column=1, padx=8)
        if self.current_user_permissions:
            ctk.CTkButton(bframe, text="Admin", fg_color="orange", command=self.admin_page, width=120).grid(row=0, column=2, padx=8)
        ctk.CTkButton(bframe, text="Logout", fg_color="red", command=self.logout, width=120).grid(row=0, column=3, padx=8)

    # Register event
    def register_event(self, eid: int, capacity: int, current_registered: int):
        if current_registered >= capacity:
            messagebox.showerror("Full", "This event is full.")
            return
        try:
            cnx = get_db()
            cursor = cnx.cursor()
            cursor.execute("INSERT INTO Registrations (userid, eid) VALUES (%s, %s)", (self.current_user_id, eid))
            cnx.commit()
            cursor.close()
            cnx.close()
            messagebox.showinfo("Success", "Registered for event.")
            self.dashboard_page()
        except mysql.connector.IntegrityError as ie:
            messagebox.showerror("Error", "You are already registered for this event.")
        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", f"Could not register: {err}")

    # User create event page
    def get_room_list(self):
        try:
            cnx = get_db()
            cursor = cnx.cursor()
            cursor.execute("SELECT rid FROM Rooms ORDER BY rid")
            rooms = [str(r[0]) for r in cursor.fetchall()]
            cursor.close()
            cnx.close()
            return rooms
        except:
            return []
   
    def user_create_event_page(self):
        self.clear_window()
        frame = ctk.CTkFrame(self, width=700, height=520, corner_radius=12)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="Create Event", font=("Arial", 28, "bold")).pack(pady=12)

        self.uc_name = ctk.CTkEntry(frame, placeholder_text="Event name", width=420)
        self.uc_name.pack(pady=6)

        self.uc_date = ctk.CTkEntry(frame, placeholder_text="YYYY-MM-DD", width=180)
        self.uc_date.pack(pady=6)

        self.uc_time = ctk.CTkEntry(frame, placeholder_text="HH:MM:SS", width=180)
        self.uc_time.pack(pady=6)

        rooms = self.get_room_list()
        if not rooms:
            rooms = ["No Rooms Found"]

        ctk.CTkLabel(frame, text="Select Room").pack(pady=4)
        self.uc_loc = ctk.CTkOptionMenu(frame, values=rooms, width=200)
        self.uc_loc.pack(pady=6)

        self.uc_cap = ctk.CTkEntry(frame, placeholder_text="Capacity (int)", width=150)
        self.uc_cap.pack(pady=6)

        self.uc_desc = ctk.CTkEntry(frame, placeholder_text="Short description", width=420)
        self.uc_desc.pack(pady=6)

        ctk.CTkButton(frame, text="Create Event", command=self.user_create_event, width=240).pack(pady=12)
        ctk.CTkButton(frame, text="Back", command=self.dashboard_page, width=120, fg_color="gray20").pack(pady=6)

    # User Create Event Database Function
    def user_create_event(self):
        name = self.uc_name.get().strip()
        date_s = self.uc_date.get().strip()
        time_s = self.uc_time.get().strip()
        loc = self.uc_loc.get().strip()
        cap_s = self.uc_cap.get().strip()
        desc = self.uc_desc.get().strip()

        if not name or not cap_s:
            messagebox.showerror("Error", "Please enter at least name and capacity.")
            return
        try:
            cap = int(cap_s)
        except ValueError:
            messagebox.showerror("Error", "Capacity must be an integer.")
            return
        date_val = None
        time_val = None
        try:
            if date_s:
                date_val = datetime.datetime.strptime(date_s, "%Y-%m-%d").date()
            if time_s:
                time_val = datetime.datetime.strptime(time_s, "%H:%M:%S").time()
        except ValueError:
            messagebox.showerror("Error", "Date must be YYYY-MM-DD and time HH:MM:SS.")
            return
        try:
            cnx = get_db()
            cursor = cnx.cursor()
            cursor.execute("""
                INSERT INTO Events (eventName, eventDate, eventTime, eventLocation, eventDescription, eventCapacity)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, date_val, time_val, loc, desc, cap))
            cnx.commit()
            cursor.close()
            cnx.close()
            messagebox.showinfo("Success", "Event created.")
            self.dashboard_page()
        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", f"Could not create event: {err}")

    # Logout
    def logout(self):
        self.current_user_email = None
        self.current_user_id = None
        self.current_user_permissions = False
        self.login_page()

    # Clear window utlility
    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

# Run App:
if __name__ == "__main__":
    app = App()
    app.mainloop()