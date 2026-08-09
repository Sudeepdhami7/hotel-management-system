import os
import re
from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

# Import the HotelInfoWin module to display information/policies after login
try:
    from info import HotelInfoWin
except ImportError:
    HotelInfoWin = None


class AnimatedButton(Button):
    """Custom Tkinter Button with smooth hover color animations."""

    def __init__(self, master, bg_normal, bg_hover, fg_normal, fg_hover, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.bg_normal = bg_normal
        self.bg_hover = bg_hover
        self.fg_normal = fg_normal
        self.fg_hover = fg_hover

        self.configure(
            bg=self.bg_normal,
            fg=self.fg_normal,
            activebackground=self.bg_hover,
            activeforeground=self.fg_hover,
            bd=0,
            relief=FLAT,
            cursor="hand2",
        )

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.configure(bg=self.bg_hover, fg=self.fg_hover)

    def on_leave(self, e):
        self.configure(bg=self.bg_normal, fg=self.fg_normal)


class LoginWindow:

    def __init__(self, root):
        self.root = root
        self.root.title("Royal Hotel - Admin Portal")
        self.root.geometry("1550x800+0+0")
        self.root.configure(bg="#0f0f11")

        # Variables
        self.var_login_id = StringVar()  # Stores Name, Email, or Mobile Number
        self.var_password = StringVar()
        self.show_password = BooleanVar(value=False)

        # In-Memory Database Store
        # Key: Primary Username / ID
        self.users_db = {
            "admin": {
                "name": "admin",
                "mobile": "9876543210",
                "email": "admin@hotel.com",
                "password": "admin",
                "question": "Your First Pet Name",
                "answer": "admin",
            }
        }

        # Base directory for image assets
        img_dir = r"C:\Users\sudee\OneDrive\Desktop\DATA SCIENCE\Hotel Management System\photos"

        # Helper function to load and resize images safely
        def load_image(filename, size):
            path = os.path.join(img_dir, filename)
            if os.path.exists(path):
                img = Image.open(path)
                img = img.resize(size, Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(img)
            else:
                img = Image.new("RGB", size, color="#0f0f11")
                return ImageTk.PhotoImage(img)

        # Background Image
        self.bg_photo = load_image("photo2.jpg", (1550, 800))
        self.lbl_bg = Label(self.root, image=self.bg_photo, bg="#0f0f11")
        self.lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        # Glassmorphic Login Container Card
        self.login_card = Frame(self.root, bg="#18181c", bd=0)
        self.card_y = 220
        self.login_card.place(x=550, y=self.card_y, width=450, height=540)

        # Gold Top Accent Line
        accent_bar = Frame(self.login_card, bg="gold", height=4)
        accent_bar.pack(fill=X, side=TOP)

        # Header Title
        title_lbl = Label(
            self.login_card,
            text="ROYAL HOTEL",
            font=("times new roman", 24, "bold"),
            bg="#18181c",
            fg="gold",
        )
        title_lbl.pack(pady=(20, 2))

        subtitle_lbl = Label(
            self.login_card,
            text="ADMINISTRATOR LOGIN",
            font=("arial", 9, "bold"),
            bg="#18181c",
            fg="#888888",
        )
        subtitle_lbl.pack(pady=(0, 15))

        # --- Form Container ---
        form_frame = Frame(self.login_card, bg="#18181c")
        form_frame.pack(fill=BOTH, expand=True, padx=45)

        # Multi-Format Login Identifier Field (Name / Email / Mobile)
        lbl_user = Label(
            form_frame,
            text="NAME / EMAIL / MOBILE NO.",
            font=("arial", 9, "bold"),
            bg="#18181c",
            fg="#aaaaaa",
            anchor=W,
        )
        lbl_user.pack(fill=X, pady=(5, 2))

        self.user_border = Frame(form_frame, bg="#333338", bd=1)
        self.user_border.pack(fill=X, pady=(0, 12))

        self.entry_user = Entry(
            self.user_border,
            textvariable=self.var_login_id,
            font=("arial", 12),
            bg="#222226",
            fg="white",
            insertbackground="gold",
            bd=0,
            relief=FLAT,
        )
        self.entry_user.pack(fill=X, ipady=7, padx=10)
        self.entry_user.bind("<FocusIn>", lambda e: self.on_focus_in(self.user_border))
        self.entry_user.bind("<FocusOut>", lambda e: self.on_focus_out(self.user_border))

        # Password Field
        lbl_pass = Label(
            form_frame,
            text="PASSWORD",
            font=("arial", 9, "bold"),
            bg="#18181c",
            fg="#aaaaaa",
            anchor=W,
        )
        lbl_pass.pack(fill=X, pady=(5, 2))

        self.pass_border = Frame(form_frame, bg="#333338", bd=1)
        self.pass_border.pack(fill=X, pady=(0, 8))

        self.entry_pass = Entry(
            self.pass_border,
            textvariable=self.var_password,
            show="•",
            font=("arial", 12),
            bg="#222226",
            fg="white",
            insertbackground="gold",
            bd=0,
            relief=FLAT,
        )
        self.entry_pass.pack(fill=X, ipady=7, padx=10)
        self.entry_pass.bind("<FocusIn>", lambda e: self.on_focus_in(self.pass_border))
        self.entry_pass.bind("<FocusOut>", lambda e: self.on_focus_out(self.pass_border))

        # Options Row: Show Password + Forgot Password
        opts_frame = Frame(form_frame, bg="#18181c")
        opts_frame.pack(fill=X, pady=(0, 15))

        self.chk_show_pass = Checkbutton(
            opts_frame,
            text=" Show Password",
            variable=self.show_password,
            command=self.toggle_password_visibility,
            font=("arial", 9),
            bg="#18181c",
            fg="#aaaaaa",
            activebackground="#18181c",
            activeforeground="gold",
            selectcolor="#222226",
            bd=0,
            cursor="hand2",
        )
        self.chk_show_pass.pack(side=LEFT)

        btn_forgot = Button(
            opts_frame,
            text="Forgot Password?",
            command=self.forgot_password_popup,
            font=("arial", 9, "bold"),
            bg="#18181c",
            fg="gold",
            activebackground="#18181c",
            activeforeground="#e6c200",
            bd=0,
            relief=FLAT,
            cursor="hand2",
        )
        btn_forgot.pack(side=RIGHT)

        # Action Buttons
        self.btn_login = AnimatedButton(
            form_frame,
            bg_normal="gold",
            bg_hover="#e6c200",
            fg_normal="black",
            fg_hover="black",
            text="LOG IN",
            font=("arial", 11, "bold"),
            command=self.login_action,
            height=2,
        )
        self.btn_login.pack(fill=X, pady=(5, 8))

        self.btn_reset = AnimatedButton(
            form_frame,
            bg_normal="#25252a",
            bg_hover="#33333a",
            fg_normal="#ffffff",
            fg_hover="gold",
            text="RESET FIELDS",
            font=("arial", 9, "bold"),
            command=self.reset_fields,
            height=2,
        )
        self.btn_reset.pack(fill=X, pady=(0, 10))

        # Registration Link Row
        reg_frame = Frame(form_frame, bg="#18181c")
        reg_frame.pack(fill=X)

        lbl_no_account = Label(
            reg_frame,
            text="New User?",
            font=("arial", 9),
            bg="#18181c",
            fg="#888888",
        )
        lbl_no_account.pack(side=LEFT, padx=(65, 5))

        btn_register_link = Button(
            reg_frame,
            text="Register New Account",
            command=self.register_popup,
            font=("arial", 9, "bold"),
            bg="#18181c",
            fg="gold",
            activebackground="#18181c",
            activeforeground="#e6c200",
            bd=0,
            relief=FLAT,
            cursor="hand2",
        )
        btn_register_link.pack(side=LEFT)

        # Trigger Entrance Animation
        self.animate_card_entrance()

    def animate_card_entrance(self):
        target_y = 130
        if self.card_y > target_y:
            self.card_y -= 4
            self.login_card.place(x=550, y=self.card_y, width=450, height=540)
            self.root.after(10, self.animate_card_entrance)

    def on_focus_in(self, frame_widget):
        frame_widget.configure(bg="gold")

    def on_focus_out(self, frame_widget):
        frame_widget.configure(bg="#333338")

    def toggle_password_visibility(self):
        if self.show_password.get():
            self.entry_pass.configure(show="")
        else:
            self.entry_pass.configure(show="•")

    def find_user_by_identifier(self, login_input):
        """Searches database for a match against Name, Email, or Mobile Number."""
        query = login_input.strip().lower()
        for user_key, data in self.users_db.items():
            if (
                query == data["name"].lower()
                or query == data["email"].lower()
                or query == data["mobile"]
            ):
                return user_key, data
        return None, None

    def login_action(self):
        login_input = self.var_login_id.get().strip()
        password = self.var_password.get().strip()

        if login_input == "" or password == "":
            messagebox.showerror("Validation Error", "Please enter your Name/Email/Mobile and Password!", parent=self.root)
            return

        user_key, user_data = self.find_user_by_identifier(login_input)

        if user_data and user_data["password"] == password:
            messagebox.showinfo("Access Granted", f"Welcome back, {user_data['name']}!", parent=self.root)
            self.root.destroy()  # Close the Login Window

            # Directly open info.py (HotelInfoWin) after login
            if HotelInfoWin is not None:
                info_root = Tk()
                app = HotelInfoWin(info_root)
                info_root.mainloop()
            else:
                messagebox.showerror("Error", "Information module ('info.py') not found!")
        else:
            messagebox.showerror("Access Denied", "Invalid Credentials! Check your Name, Email, Mobile, or Password.", parent=self.root)

    def reset_fields(self):
        self.var_login_id.set("")
        self.var_password.set("")
        self.show_password.set(False)
        self.toggle_password_visibility()
        self.user_border.configure(bg="#333338")
        self.pass_border.configure(bg="#333338")
        self.entry_user.focus_set()

    # ---------------- Registration Window ----------------
    def register_popup(self):
        reg_win = Toplevel(self.root)
        reg_win.title("Register New Account")
        reg_win.geometry("420x560+565+140")
        reg_win.configure(bg="#18181c")
        reg_win.grab_set()

        Frame(reg_win, bg="gold", height=4).pack(fill=X, side=TOP)

        Label(
            reg_win,
            text="CREATE ACCOUNT",
            font=("times new roman", 16, "bold"),
            bg="#18181c",
            fg="gold",
        ).pack(pady=(15, 10))

        # Full Name / Username
        Label(reg_win, text="Full Name / Username:", font=("arial", 9, "bold"), bg="#18181c", fg="#aaaaaa").pack(anchor=W, padx=30)
        var_r_name = StringVar()
        ttk.Entry(reg_win, textvariable=var_r_name, font=("arial", 10)).pack(fill=X, padx=30, pady=(2, 8))

        # Mobile Number
        Label(reg_win, text="Mobile Number:", font=("arial", 9, "bold"), bg="#18181c", fg="#aaaaaa").pack(anchor=W, padx=30)
        var_r_mobile = StringVar()
        ttk.Entry(reg_win, textvariable=var_r_mobile, font=("arial", 10)).pack(fill=X, padx=30, pady=(2, 8))

        # Email Address
        Label(reg_win, text="Email Address (Gmail):", font=("arial", 9, "bold"), bg="#18181c", fg="#aaaaaa").pack(anchor=W, padx=30)
        var_r_email = StringVar()
        ttk.Entry(reg_win, textvariable=var_r_email, font=("arial", 10)).pack(fill=X, padx=30, pady=(2, 8))

        # Security Question
        Label(reg_win, text="Security Question:", font=("arial", 9, "bold"), bg="#18181c", fg="#aaaaaa").pack(anchor=W, padx=30)
        combo_r_q = ttk.Combobox(
            reg_win,
            values=[
                "Your First Pet Name",
                "Your Birthplace City",
                "Your Favorite Color",
                "Your Primary School Name",
            ],
            state="readonly",
            font=("arial", 9),
        )
        combo_r_q.current(0)
        combo_r_q.pack(fill=X, padx=30, pady=(2, 8))

        # Security Answer
        Label(reg_win, text="Security Answer:", font=("arial", 9, "bold"), bg="#18181c", fg="#aaaaaa").pack(anchor=W, padx=30)
        var_r_ans = StringVar()
        ttk.Entry(reg_win, textvariable=var_r_ans, font=("arial", 10)).pack(fill=X, padx=30, pady=(2, 8))

        # Password
        Label(reg_win, text="Password:", font=("arial", 9, "bold"), bg="#18181c", fg="#aaaaaa").pack(anchor=W, padx=30)
        var_r_pass = StringVar()
        ttk.Entry(reg_win, textvariable=var_r_pass, show="•", font=("arial", 10)).pack(fill=X, padx=30, pady=(2, 8))

        # Confirm Password
        Label(reg_win, text="Confirm Password:", font=("arial", 9, "bold"), bg="#18181c", fg="#aaaaaa").pack(anchor=W, padx=30)
        var_r_cpass = StringVar()
        ttk.Entry(reg_win, textvariable=var_r_cpass, show="•", font=("arial", 10)).pack(fill=X, padx=30, pady=(2, 15))

        def save_new_user():
            name = var_r_name.get().strip()
            mobile = var_r_mobile.get().strip()
            email = var_r_email.get().strip()
            q = combo_r_q.get()
            ans = var_r_ans.get().strip()
            p = var_r_pass.get().strip()
            cp = var_r_cpass.get().strip()

            if name == "" or mobile == "" or email == "" or ans == "" or p == "":
                messagebox.showerror("Error", "All registration fields are required!", parent=reg_win)
                return

            if p != cp:
                messagebox.showerror("Error", "Passwords do not match!", parent=reg_win)
                return

            # Check if Name, Mobile, or Email is already taken
            for key, udata in self.users_db.items():
                if udata["name"].lower() == name.lower():
                    messagebox.showerror("Error", "Name / Username already registered!", parent=reg_win)
                    return
                if udata["mobile"] == mobile:
                    messagebox.showerror("Error", "Mobile Number already registered!", parent=reg_win)
                    return
                if udata["email"].lower() == email.lower():
                    messagebox.showerror("Error", "Email Address already registered!", parent=reg_win)
                    return

            # Store user details
            self.users_db[name] = {
                "name": name,
                "mobile": mobile,
                "email": email,
                "password": p,
                "question": q,
                "answer": ans,
            }

            messagebox.showinfo("Success", "Account registered successfully!\nYou can now log in using your Name, Email, or Mobile Number.", parent=reg_win)
            reg_win.destroy()

        btn_register_submit = AnimatedButton(
            reg_win,
            bg_normal="gold",
            bg_hover="#e6c200",
            fg_normal="black",
            fg_hover="black",
            text="REGISTER NOW",
            font=("arial", 10, "bold"),
            command=save_new_user,
            height=2,
        )
        btn_register_submit.pack(fill=X, padx=30, pady=5)

    # ---------------- Forgot Password Window ----------------
    def forgot_password_popup(self):
        forgot_win = Toplevel(self.root)
        forgot_win.title("Password Recovery")
        forgot_win.geometry("400x440+575+200")
        forgot_win.configure(bg="#18181c")
        forgot_win.grab_set()

        Frame(forgot_win, bg="gold", height=4).pack(fill=X, side=TOP)

        Label(
            forgot_win,
            text="PASSWORD RECOVERY",
            font=("times new roman", 16, "bold"),
            bg="#18181c",
            fg="gold",
        ).pack(pady=(20, 15))

        Label(forgot_win, text="Name / Email / Mobile:", font=("arial", 10, "bold"), bg="#18181c", fg="#aaaaaa").pack(anchor=W, padx=30)
        var_f_id = StringVar()
        e_f_id = ttk.Entry(forgot_win, textvariable=var_f_id, font=("arial", 11))
        e_f_id.pack(fill=X, padx=30, pady=(2, 10))

        Label(forgot_win, text="Security Question:", font=("arial", 10, "bold"), bg="#18181c", fg="#aaaaaa").pack(anchor=W, padx=30)
        combo_q = ttk.Combobox(
            forgot_win,
            values=[
                "Your First Pet Name",
                "Your Birthplace City",
                "Your Favorite Color",
                "Your Primary School Name",
            ],
            state="readonly",
            font=("arial", 10),
        )
        combo_q.current(0)
        combo_q.pack(fill=X, padx=30, pady=(2, 10))

        Label(forgot_win, text="Security Answer:", font=("arial", 10, "bold"), bg="#18181c", fg="#aaaaaa").pack(anchor=W, padx=30)
        var_f_ans = StringVar()
        e_f_ans = ttk.Entry(forgot_win, textvariable=var_f_ans, font=("arial", 11))
        e_f_ans.pack(fill=X, padx=30, pady=(2, 10))

        Label(forgot_win, text="New Password:", font=("arial", 10, "bold"), bg="#18181c", fg="#aaaaaa").pack(anchor=W, padx=30)
        var_f_newpass = StringVar()
        e_f_newpass = ttk.Entry(forgot_win, textvariable=var_f_newpass, show="•", font=("arial", 11))
        e_f_newpass.pack(fill=X, padx=30, pady=(2, 20))

        def reset_password_action():
            ident = var_f_id.get().strip()
            q = combo_q.get()
            ans = var_f_ans.get().strip()
            np = var_f_newpass.get().strip()

            if ident == "" or ans == "" or np == "":
                messagebox.showerror("Error", "All recovery fields are required!", parent=forgot_win)
                return

            user_key, udata = self.find_user_by_identifier(ident)

            if udata:
                saved_q = udata.get("question")
                saved_ans = udata.get("answer")

                if saved_q == q and saved_ans.lower() == ans.lower():
                    self.users_db[user_key]["password"] = np
                    messagebox.showinfo("Success", "Password updated successfully! You can now log in.", parent=forgot_win)
                    forgot_win.destroy()
                else:
                    messagebox.showerror("Error", "Security question or answer does not match!", parent=forgot_win)
            else:
                messagebox.showerror("Error", f"No account registered with identifier '{ident}'!", parent=forgot_win)

        btn_update_pass = AnimatedButton(
            forgot_win,
            bg_normal="gold",
            bg_hover="#e6c200",
            fg_normal="black",
            fg_hover="black",
            text="UPDATE PASSWORD",
            font=("arial", 10, "bold"),
            command=reset_password_action,
            height=2,
        )
        btn_update_pass.pack(fill=X, padx=30, pady=5)


if __name__ == "__main__":
    root = Tk()
    app = LoginWindow(root)
    root.mainloop()