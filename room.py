import os
import random
from datetime import datetime
from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector
from PIL import Image, ImageTk


class Roombooking:

    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System - Room Booking")
        self.root.geometry("1295x580+230+220")

        # Variables
        self.var_contact = StringVar()
        self.var_check_in = StringVar()
        self.var_check_out = StringVar()
        self.var_roomtype = StringVar()
        self.var_roomavailable = StringVar()
        self.var_meal = StringVar()
        self.var_noOfdays = StringVar()
        self.var_paidtax = StringVar()
        self.var_actualtotal = StringVar()
        self.var_total = StringVar()

        # Search Variables
        self.var_search_by = StringVar()
        self.var_search_txt = StringVar()

        # Database Configuration
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "2333438",  # Replace with your MySQL password
        }

        # Base directory for images
        img_dir = r"C:\Users\sudee\OneDrive\Desktop\DATA SCIENCE\Hotel Management System\photos"

        # Helper function to load images safely
        def load_image(filename, size):
            path = os.path.join(img_dir, filename)
            if os.path.exists(path):
                img = Image.open(path)
                img = img.resize(size, Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(img)
            else:
                img = Image.new("RGB", size, color="gray")
                return ImageTk.PhotoImage(img)

        # Title Label
        lbl_title = Label(
            self.root,
            text="ROOMBOOKING DETAILS",
            font=("times new roman", 18, "bold"),
            bg="black",
            fg="gold",
            bd=4,
            relief=RIDGE,
        )
        lbl_title.place(x=0, y=0, width=1295, height=50)

        # Left Frame - Form Inputs
        labelframeleft = LabelFrame(
            self.root,
            bd=2,
            relief=RIDGE,
            text="Roombooking Details",
            font=("times new roman", 12, "bold"),
            padx=2,
        )
        labelframeleft.place(x=5, y=50, width=425, height=490)

        # Customer Contact
        lbl_cust_contact = Label(
            labelframeleft,
            text="Customer Contact:",
            font=("arial", 11, "bold"),
            padx=2,
            pady=4,
        )
        lbl_cust_contact.grid(row=0, column=0, sticky=W)
        entry_contact = ttk.Entry(
            labelframeleft,
            textvariable=self.var_contact,
            font=("arial", 11),
            width=13,
        )
        entry_contact.grid(row=0, column=1, sticky=W)

        btnFetchData = Button(
            labelframeleft,
            text="Fetch Data",
            command=self.fetch_contact_info,
            font=("arial", 9, "bold"),
            bg="black",
            fg="gold",
            width=9,
        )
        btnFetchData.grid(row=0, column=2, padx=2)

        # Check-in Date
        check_in_date = Label(
            labelframeleft,
            text="Check_in Date:",
            font=("arial", 11, "bold"),
            padx=2,
            pady=4,
        )
        check_in_date.grid(row=1, column=0, sticky=W)
        txtcheck_in_date = ttk.Entry(
            labelframeleft,
            textvariable=self.var_check_in,
            font=("arial", 11),
            width=22,
        )
        txtcheck_in_date.grid(row=1, column=1, columnspan=2, sticky=W)

        # Check-out Date
        check_out_date = Label(
            labelframeleft,
            text="Check_Out Date:",
            font=("arial", 11, "bold"),
            padx=2,
            pady=4,
        )
        check_out_date.grid(row=2, column=0, sticky=W)
        txtcheck_out_date = ttk.Entry(
            labelframeleft,
            textvariable=self.var_check_out,
            font=("arial", 11),
            width=22,
        )
        txtcheck_out_date.grid(row=2, column=1, columnspan=2, sticky=W)

        # Room Type
        label_RoomType = Label(
            labelframeleft,
            text="Room Type:",
            font=("arial", 11, "bold"),
            padx=2,
            pady=4,
        )
        label_RoomType.grid(row=3, column=0, sticky=W)
        self.combo_RoomType = ttk.Combobox(
            labelframeleft,
            textvariable=self.var_roomtype,
            font=("arial", 11),
            width=20,
            state="readonly",
        )
        self.combo_RoomType["values"] = (
            "Single",
            "Double",
            "Luxury",
            "Deluxe",
            "Suite",
        )
        self.combo_RoomType.current(0)
        self.combo_RoomType.grid(row=3, column=1, columnspan=2, sticky=W)
        self.combo_RoomType.bind("<<ComboboxSelected>>", self.update_room_numbers)

        # Available Room
        lblRoomAvailable = Label(
            labelframeleft,
            text="Available Room:",
            font=("arial", 11, "bold"),
            padx=2,
            pady=4,
        )
        lblRoomAvailable.grid(row=4, column=0, sticky=W)
        self.combo_RoomAvailable = ttk.Combobox(
            labelframeleft,
            textvariable=self.var_roomavailable,
            font=("arial", 11),
            width=20,
            state="readonly",
        )
        self.combo_RoomAvailable.grid(row=4, column=1, columnspan=2, sticky=W)
        self.update_room_numbers()

        # Meal Plan
        lblMeal = Label(
            labelframeleft,
            text="Meal:",
            font=("arial", 11, "bold"),
            padx=2,
            pady=4,
        )
        lblMeal.grid(row=5, column=0, sticky=W)
        combo_Meal = ttk.Combobox(
            labelframeleft,
            textvariable=self.var_meal,
            font=("arial", 11),
            width=20,
            state="readonly",
        )
        combo_Meal["values"] = ("Breakfast", "Lunch", "Dinner", "All Inclusive")
        combo_Meal.current(0)
        combo_Meal.grid(row=5, column=1, columnspan=2, sticky=W)

        # No Of Days
        lblNoOfDays = Label(
            labelframeleft,
            text="No Of Days:",
            font=("arial", 11, "bold"),
            padx=2,
            pady=4,
        )
        lblNoOfDays.grid(row=6, column=0, sticky=W)
        txtNoOfDays = ttk.Entry(
            labelframeleft,
            textvariable=self.var_noOfdays,
            font=("arial", 11),
            width=22,
            state="readonly",
        )
        txtNoOfDays.grid(row=6, column=1, columnspan=2, sticky=W)

        # Paid Tax
        lblPaidTax = Label(
            labelframeleft,
            text="Paid Tax:",
            font=("arial", 11, "bold"),
            padx=2,
            pady=4,
        )
        lblPaidTax.grid(row=7, column=0, sticky=W)
        txtPaidTax = ttk.Entry(
            labelframeleft,
            textvariable=self.var_paidtax,
            font=("arial", 11),
            width=22,
            state="readonly",
        )
        txtPaidTax.grid(row=7, column=1, columnspan=2, sticky=W)

        # Sub Total
        lblSubTotal = Label(
            labelframeleft,
            text="Sub Total:",
            font=("arial", 11, "bold"),
            padx=2,
            pady=4,
        )
        lblSubTotal.grid(row=8, column=0, sticky=W)
        txtSubTotal = ttk.Entry(
            labelframeleft,
            textvariable=self.var_actualtotal,
            font=("arial", 11),
            width=22,
            state="readonly",
        )
        txtSubTotal.grid(row=8, column=1, columnspan=2, sticky=W)

        # Total Cost
        lblTotalCost = Label(
            labelframeleft,
            text="Total Cost:",
            font=("arial", 11, "bold"),
            padx=2,
            pady=4,
        )
        lblTotalCost.grid(row=9, column=0, sticky=W)
        txtTotalCost = ttk.Entry(
            labelframeleft,
            textvariable=self.var_total,
            font=("arial", 11),
            width=22,
            state="readonly",
        )
        txtTotalCost.grid(row=9, column=1, columnspan=2, sticky=W)

        # Bill Button
        btnBill = Button(
            labelframeleft,
            text="Bill",
            command=self.calculate_bill,
            font=("arial", 11, "bold"),
            bg="black",
            fg="gold",
            width=9,
        )
        btnBill.grid(row=10, column=0, pady=8, sticky=W, padx=2)

        # Action Buttons Frame
        btn_frame = Frame(labelframeleft, bd=2, relief=RIDGE)
        btn_frame.place(x=0, y=410, width=415, height=40)

        btnAdd = Button(
            btn_frame,
            text="Add",
            command=self.add_data,
            font=("arial", 10, "bold"),
            bg="black",
            fg="gold",
            width=9,
        )
        btnAdd.grid(row=0, column=0, padx=2, pady=4)

        btnUpdate = Button(
            btn_frame,
            text="Update",
            command=self.update_data,
            font=("arial", 10, "bold"),
            bg="black",
            fg="gold",
            width=9,
        )
        btnUpdate.grid(row=0, column=1, padx=2, pady=4)

        btnDelete = Button(
            btn_frame,
            text="Delete",
            command=self.delete_data,
            font=("arial", 10, "bold"),
            bg="black",
            fg="gold",
            width=9,
        )
        btnDelete.grid(row=0, column=2, padx=2, pady=4)

        btnReset = Button(
            btn_frame,
            text="Reset",
            command=self.reset_data,
            font=("arial", 10, "bold"),
            bg="black",
            fg="gold",
            width=9,
        )
        btnReset.grid(row=0, column=3, padx=2, pady=4)

        # Middle Top Frame - Customer Details Panel
        cust_details_frame = Frame(self.root, bd=2, relief=RIDGE)
        cust_details_frame.place(x=435, y=55, width=300, height=195)

        lbl_name_title = Label(cust_details_frame, text="Name:", font=("arial", 10, "bold"))
        lbl_name_title.place(x=5, y=10)
        self.lbl_name = Label(cust_details_frame, text="", font=("arial", 10))
        self.lbl_name.place(x=90, y=10)

        lbl_gender_title = Label(cust_details_frame, text="Gender:", font=("arial", 10, "bold"))
        lbl_gender_title.place(x=5, y=45)
        self.lbl_gender = Label(cust_details_frame, text="", font=("arial", 10))
        self.lbl_gender.place(x=90, y=45)

        lbl_email_title = Label(cust_details_frame, text="Email:", font=("arial", 10, "bold"))
        lbl_email_title.place(x=5, y=80)
        self.lbl_email = Label(cust_details_frame, text="", font=("arial", 10))
        self.lbl_email.place(x=90, y=80)

        lbl_nation_title = Label(cust_details_frame, text="Nationality:", font=("arial", 10, "bold"))
        lbl_nation_title.place(x=5, y=115)
        self.lbl_nation = Label(cust_details_frame, text="", font=("arial", 10))
        self.lbl_nation.place(x=90, y=115)

        lbl_address_title = Label(cust_details_frame, text="Address:", font=("arial", 10, "bold"))
        lbl_address_title.place(x=5, y=150)
        self.lbl_address = Label(cust_details_frame, text="", font=("arial", 10))
        self.lbl_address.place(x=90, y=150)

        # Right Top Frame - Room Image
        self.photo_room = load_image("room.jpg", (530, 195))
        lbl_room_img = Label(
            self.root, image=self.photo_room, bd=2, relief=RIDGE
        )
        lbl_room_img.place(x=745, y=55, width=535, height=195)

        # Right Bottom Frame - View Details & Search System
        table_frame = LabelFrame(
            self.root,
            bd=2,
            relief=RIDGE,
            text="View Deatils And Seaarch System",
            font=("times new roman", 12, "bold"),
        )
        table_frame.place(x=435, y=260, width=850, height=280)

        # Search Controls
        lblSearchBy = Label(
            table_frame,
            text="Search By:",
            font=("arial", 11, "bold"),
            bg="red",
            fg="white",
        )
        lblSearchBy.grid(row=0, column=0, sticky=W, padx=2)

        combo_Search = ttk.Combobox(
            table_frame,
            textvariable=self.var_search_by,
            font=("arial", 11),
            width=15,
            state="readonly",
        )
        combo_Search["values"] = ("Contact", "Room No")
        combo_Search.current(0)
        combo_Search.grid(row=0, column=1, padx=2)

        txtSearch = ttk.Entry(
            table_frame,
            textvariable=self.var_search_txt,
            font=("arial", 11),
            width=24,
        )
        txtSearch.grid(row=0, column=2, padx=2)

        btnSearch = Button(
            table_frame,
            text="Search",
            command=self.search_data,
            font=("arial", 9, "bold"),
            bg="black",
            fg="gold",
            width=9,
        )
        btnSearch.grid(row=0, column=3, padx=2)

        btnShowAll = Button(
            table_frame,
            text="Show All",
            command=self.fetch_table_data,
            font=("arial", 9, "bold"),
            bg="black",
            fg="gold",
            width=9,
        )
        btnShowAll.grid(row=0, column=4, padx=2)

        # Table Grid Display
        details_frame = Frame(table_frame, bd=2, relief=RIDGE)
        details_frame.place(x=0, y=35, width=840, height=215)

        scroll_x = ttk.Scrollbar(details_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(details_frame, orient=VERTICAL)

        self.Room_Table = ttk.Treeview(
            details_frame,
            columns=(
                "contact",
                "check_in",
                "check_out",
                "roomtype",
                "roomavailable",
                "meal",
                "noOfdays",
            ),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set,
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.Room_Table.xview)
        scroll_y.config(command=self.Room_Table.yview)

        self.Room_Table.heading("contact", text="Contact")
        self.Room_Table.heading("check_in", text="Check-in")
        self.Room_Table.heading("check_out", text="Check-out")
        self.Room_Table.heading("roomtype", text="Room Type")
        self.Room_Table.heading("roomavailable", text="Room No")
        self.Room_Table.heading("meal", text="Meal")
        self.Room_Table.heading("noOfdays", text="NoOfDays")

        self.Room_Table["show"] = "headings"
        self.Room_Table.column("contact", width=110)
        self.Room_Table.column("check_in", width=110)
        self.Room_Table.column("check_out", width=110)
        self.Room_Table.column("roomtype", width=110)
        self.Room_Table.column("roomavailable", width=90)
        self.Room_Table.column("meal", width=100)
        self.Room_Table.column("noOfdays", width=80)

        self.Room_Table.pack(fill=BOTH, expand=1)
        self.Room_Table.bind("<ButtonRelease-1>", self.get_cursor_data)

    def update_room_numbers(self, event=""):
        selected_type = self.var_roomtype.get()
        rooms = []

        if selected_type == "Single":
            rooms = (
                list(range(100, 105))
                + list(range(200, 205))
                + list(range(300, 305))
            )
        elif selected_type == "Double":
            rooms = (
                list(range(105, 109))
                + list(range(205, 209))
                + list(range(305, 309))
            )
        elif selected_type == "Luxury":
            rooms = (
                list(range(109, 113))
                + list(range(209, 213))
                + list(range(309, 313))
            )
        elif selected_type == "Deluxe":
            rooms = (
                list(range(113, 117))
                + list(range(213, 217))
                + list(range(313, 317))
            )
        elif selected_type == "Suite":
            rooms = (
                list(range(117, 121))
                + list(range(217, 221))
                + list(range(317, 321))
            )

        str_rooms = [str(r) for r in rooms]
        self.combo_RoomAvailable["values"] = tuple(str_rooms)

        if self.var_roomavailable.get() not in str_rooms and str_rooms:
            self.combo_RoomAvailable.current(0)

    def get_db_connection(self):
        config = self.db_config.copy()
        config["database"] = "hotel_management"
        return mysql.connector.connect(**config)

    def ensure_table_exists(self):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS hotel_management")
            conn.close()

            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS room_booking (
                    contact VARCHAR(50) PRIMARY KEY,
                    check_in VARCHAR(20),
                    check_out VARCHAR(20),
                    roomtype VARCHAR(50),
                    roomavailable VARCHAR(10),
                    meal VARCHAR(50),
                    noOfdays VARCHAR(10),
                    paidtax VARCHAR(20),
                    subtotal VARCHAR(20),
                    total VARCHAR(20)
                )
                """
            )
            conn.commit()
            conn.close()
            self.fetch_table_data()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"MySQL Error: {err}")

    def calculate_bill(self):
        try:
            in_date = datetime.strptime(self.var_check_in.get(), "%Y-%m-%d")
            out_date = datetime.strptime(self.var_check_out.get(), "%Y-%m-%d")

            days = (out_date - in_date).days
            if days <= 0:
                messagebox.showerror(
                    "Invalid Date", "Check-out date must be after Check-in date."
                )
                return

            self.var_noOfdays.set(str(days))

            rates = {
                "Single": 50,
                "Double": 80,
                "Luxury": 120,
                "Deluxe": 180,
                "Suite": 250,
            }
            meal_rates = {
                "Breakfast": 10,
                "Lunch": 15,
                "Dinner": 20,
                "All Inclusive": 40,
            }

            room_cost = rates.get(self.var_roomtype.get(), 50)
            meal_cost = meal_rates.get(self.var_meal.get(), 0)

            sub_total = (room_cost + meal_cost) * days
            tax = sub_total * 0.10
            total = sub_total + tax

            self.var_paidtax.set(f"Rs.{tax:.2f}")
            self.var_actualtotal.set(f"Rs.{sub_total:.2f}")
            self.var_total.set(f"Rs.{total:.2f}")

        except ValueError:
            messagebox.showerror("Error", "Please enter dates in YYYY-MM-DD format.")

    def add_data(self):
        if self.var_contact.get() == "" or self.var_check_in.get() == "":
            messagebox.showerror("Error", "All required fields must be filled!")
            return

        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO room_booking VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    self.var_contact.get(),
                    self.var_check_in.get(),
                    self.var_check_out.get(),
                    self.var_roomtype.get(),
                    self.var_roomavailable.get(),
                    self.var_meal.get(),
                    self.var_noOfdays.get(),
                    self.var_paidtax.get(),
                    self.var_actualtotal.get(),
                    self.var_total.get(),
                ),
            )
            conn.commit()
            self.fetch_table_data()
            conn.close()
            messagebox.showinfo("Success", "Room Booking details added successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error adding record: {err}")

    def fetch_table_data(self):
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT contact, check_in, check_out, roomtype, roomavailable, meal, noOfdays FROM room_booking")
            rows = cursor.fetchall()

            self.Room_Table.delete(*self.Room_Table.get_children())
            for row in rows:
                self.Room_Table.insert("", END, values=row)
            conn.close()
        except mysql.connector.Error as err:
            pass

    def search_data(self):
        if self.var_search_txt.get() == "":
            messagebox.showerror("Error", "Please enter search criteria!")
            return

        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            column = "contact" if self.var_search_by.get() == "Contact" else "roomavailable"
            
            query = f"SELECT contact, check_in, check_out, roomtype, roomavailable, meal, noOfdays FROM room_booking WHERE {column} LIKE %s"
            cursor.execute(query, ("%" + self.var_search_txt.get() + "%",))
            rows = cursor.fetchall()

            if len(rows) != 0:
                self.Room_Table.delete(*self.Room_Table.get_children())
                for row in rows:
                    self.Room_Table.insert("", END, values=row)
            else:
                messagebox.showwarning("Not Found", "No matching records found.")
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error during search: {err}")

    def get_cursor_data(self, event=""):
        cursor_row = self.Room_Table.focus()
        content = self.Room_Table.item(cursor_row)
        row = content["values"]

        if row:
            self.var_contact.set(row[0])
            self.var_check_in.set(row[1])
            self.var_check_out.set(row[2])
            self.var_roomtype.set(row[3])

            self.update_room_numbers()
            self.var_roomavailable.set(str(row[4]))

            self.var_meal.set(row[5])
            self.var_noOfdays.set(row[6])
            self.fetch_contact_info()

    def fetch_contact_info(self):
        """Fetches contact data from customer table and populates details panel."""
        search_contact = self.var_contact.get().strip()
        if search_contact == "":
            messagebox.showerror("Error", "Please enter a contact number!")
            return

        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()

            # Query customer details table
            cursor.execute(
                "SELECT Name, Gender, Email, Nationality, Address FROM customer WHERE Mobile LIKE %s OR Ref LIKE %s",
                (f"%{search_contact}%", f"%{search_contact}%"),
            )
            cust_row = cursor.fetchone()

            if cust_row:
                self.lbl_name.config(text=str(cust_row[0]))
                self.lbl_gender.config(text=str(cust_row[1]))
                self.lbl_email.config(text=str(cust_row[2]))
                self.lbl_nation.config(text=str(cust_row[3]))
                self.lbl_address.config(text=str(cust_row[4]))
            else:
                messagebox.showwarning("Not Found", "No customer found with this contact/ref.")

            # Check room_booking table for existing booking details
            cursor.execute(
                "SELECT * FROM room_booking WHERE contact LIKE %s",
                (f"%{search_contact}%",),
            )
            booking_row = cursor.fetchone()

            if booking_row:
                self.var_check_in.set(booking_row[1])
                self.var_check_out.set(booking_row[2])
                self.var_roomtype.set(booking_row[3])
                self.update_room_numbers()
                self.var_roomavailable.set(str(booking_row[4]))
                self.var_meal.set(booking_row[5])
                self.var_noOfdays.set(booking_row[6])
                self.var_paidtax.set(booking_row[7])
                self.var_actualtotal.set(booking_row[8])
                self.var_total.set(booking_row[9])

            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Database error: {err}")

    def update_data(self):
        if self.var_contact.get() == "":
            messagebox.showerror("Error", "Please specify a contact number.")
            return

        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE room_booking SET check_in=%s, check_out=%s, roomtype=%s, 
                roomavailable=%s, meal=%s, noOfdays=%s, paidtax=%s, subtotal=%s, total=%s WHERE contact=%s
                """,
                (
                    self.var_check_in.get(),
                    self.var_check_out.get(),
                    self.var_roomtype.get(),
                    self.var_roomavailable.get(),
                    self.var_meal.get(),
                    self.var_noOfdays.get(),
                    self.var_paidtax.get(),
                    self.var_actualtotal.get(),
                    self.var_total.get(),
                    self.var_contact.get(),
                ),
            )
            conn.commit()
            self.fetch_table_data()
            conn.close()
            messagebox.showinfo("Success", "Booking details updated successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error updating record: {err}")

    def delete_data(self):
        if self.var_contact.get() == "":
            messagebox.showerror("Error", "Please select or enter a contact number.")
            return

        confirm = messagebox.askyesno(
            "Confirm Delete", "Are you sure you want to delete this booking?"
        )
        if confirm:
            try:
                conn = self.get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM room_booking WHERE contact=%s",
                    (self.var_contact.get(),),
                )
                conn.commit()
                self.fetch_table_data()
                self.reset_data()
                conn.close()
                messagebox.showinfo("Success", "Booking deleted successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error deleting record: {err}")

    def reset_data(self):
        self.var_contact.set("")
        self.var_check_in.set("")
        self.var_check_out.set("")
        self.var_roomtype.set("Single")
        self.update_room_numbers()
        self.var_meal.set("Breakfast")
        self.var_noOfdays.set("")
        self.var_paidtax.set("")
        self.var_actualtotal.set("")
        self.var_total.set("")
        self.var_search_txt.set("")

        self.lbl_name.config(text="")
        self.lbl_gender.config(text="")
        self.lbl_email.config(text="")
        self.lbl_nation.config(text="")
        self.lbl_address.config(text="")


if __name__ == "__main__":
    root = Tk()
    obj = Roombooking(root)
    obj.ensure_table_exists()
    root.mainloop()