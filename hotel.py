import os
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

# Secondary window imports
from customer import Cus_Win
from details import DetailsRoom
from payment import PaymentWin  # Payment Window Import
from report import ReportWin   # Report Window Import
from room import Roombooking


class HotelManagementSystem:

    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("1550x800+0+0")

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
                img = Image.new("RGB", size, color="gray")
                return ImageTk.PhotoImage(img)

        # 1st Image (Header Banner)
        self.photoimg1 = load_image("photo1.jpg", (1550, 140))
        lblimg1 = Label(self.root, image=self.photoimg1, bd=4, relief=RIDGE)
        lblimg1.place(x=0, y=0, width=1550, height=140)

        # Logo Image
        self.photoimg2 = load_image("logo.jpg", (230, 140))
        lblimg2 = Label(self.root, image=self.photoimg2, bd=4, relief=RIDGE)
        lblimg2.place(x=0, y=0, width=230, height=140)

        # Title Label
        lbl_title = Label(
            self.root,
            text="HOTEL MANAGEMENT SYSTEM",
            font=("times new roman", 35, "bold"),
            bg="black",
            fg="gold",
            bd=4,
            relief=RIDGE,
        )
        lbl_title.place(x=0, y=140, width=1550, height=50)

        # Main Frame
        main_frame = Frame(self.root, bd=4, relief=RIDGE)
        main_frame.place(x=0, y=190, width=1550, height=620)

        # Menu Title Label
        lbl_menu = Label(
            main_frame,
            text="MENU",
            font=("times new roman", 20, "bold"),
            bg="black",
            fg="gold",
            bd=4,
            relief=RIDGE,
        )
        lbl_menu.place(x=0, y=0, width=230, height=40)

        # Button Frame (Holds vertical menu buttons - height increased to accommodate Payment)
        btn_frame = Frame(main_frame, bd=4, relief=RIDGE, bg="black")
        btn_frame.place(x=0, y=40, width=230, height=265)

        # Customer Button
        cust_btn = Button(
            btn_frame,
            text="CUSTOMER",
            command=self.cust_details,
            width=22,
            font=("times new roman", 14, "bold"),
            bg="black",
            fg="gold",
            bd=2,
            relief=RIDGE,
            cursor="hand2",
        )
        cust_btn.grid(row=0, column=0, pady=1)

        # Room Button
        room_btn = Button(
            btn_frame,
            text="ROOM",
            command=self.room_details,
            width=22,
            font=("times new roman", 14, "bold"),
            bg="black",
            fg="gold",
            bd=2,
            relief=RIDGE,
            cursor="hand2",
        )
        room_btn.grid(row=1, column=0, pady=1)

        # Details Button
        detail_btn = Button(
            btn_frame,
            text="DETAILS",
            command=self.Details_room,
            width=22,
            font=("times new roman", 14, "bold"),
            bg="black",
            fg="gold",
            bd=2,
            relief=RIDGE,
            cursor="hand2",
        )
        detail_btn.grid(row=2, column=0, pady=1)

        # Payment Button (New Integration)
        payment_btn = Button(
            btn_frame,
            text="PAYMENT",
            command=self.payment_details,
            width=22,
            font=("times new roman", 14, "bold"),
            bg="black",
            fg="gold",
            bd=2,
            relief=RIDGE,
            cursor="hand2",
        )
        payment_btn.grid(row=3, column=0, pady=1)

        # Report Button
        report_btn = Button(
            btn_frame,
            text="REPORT",
            command=self.report_details,
            width=22,
            font=("times new roman", 14, "bold"),
            bg="black",
            fg="gold",
            bd=2,
            relief=RIDGE,
            cursor="hand2",
        )
        report_btn.grid(row=4, column=0, pady=1)

        # Logout Button
        logout_btn = Button(
            btn_frame,
            text="LOGOUT",
            command=self.logout,
            width=22,
            font=("times new roman", 14, "bold"),
            bg="black",
            fg="gold",
            bd=2,
            relief=RIDGE,
            cursor="hand2",
        )
        logout_btn.grid(row=5, column=0, pady=1)

        # Right Side Main Image
        self.photoimg3 = load_image("photo2.jpg", (1310, 590))
        lblimg3 = Label(main_frame, image=self.photoimg3, bd=4, relief=RIDGE)
        lblimg3.place(x=225, y=0, width=1310, height=590)

        # Down Image 1
        self.photoimg4 = load_image("photo4.jpg", (230, 140))
        lblimg4 = Label(main_frame, image=self.photoimg4, bd=4, relief=RIDGE)
        lblimg4.place(x=0, y=305, width=230, height=140)

        # Down Image 2
        self.photoimg5 = load_image("food.jpg", (230, 140))
        lblimg5 = Label(main_frame, image=self.photoimg5, bd=4, relief=RIDGE)
        lblimg5.place(x=0, y=445, width=230, height=140)

    # Method to open Customer Window
    def cust_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Cus_Win(self.new_window)

    # Method to open Room Booking Window
    def room_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Roombooking(self.new_window)
        if hasattr(self.app, 'ensure_table_exists'):
            self.app.ensure_table_exists()

    # Method to open Room Details Window
    def Details_room(self):
        self.new_window = Toplevel(self.root)
        self.app = DetailsRoom(self.new_window)
        if hasattr(self.app, 'ensure_table_exists'):
            self.app.ensure_table_exists()

    # Method to open Payment Window
    def payment_details(self):
        self.new_window = Toplevel(self.root)
        self.app = PaymentWin(self.new_window)

    # Method to open Report Window
    def report_details(self):
        self.new_window = Toplevel(self.root)
        self.app = ReportWin(self.new_window)

    # Method to Logout with Confirmation Dialog
    def logout(self):
        reply = messagebox.askyesno(
            "Logout",
            "Are you sure you want to log out of the Hotel Management System?",
            parent=self.root,
        )
        if reply:
            self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    app = HotelManagementSystem(root)
    root.mainloop()