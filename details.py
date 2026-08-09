import os
from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector
from PIL import Image, ImageTk


class DetailsRoom:

    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System - Room Details")
        self.root.geometry("1295x580+230+220")

        # Variables
        self.var_floor = StringVar()
        self.var_roomNo = StringVar()
        self.var_roomType = StringVar()
        self.var_price = StringVar()
        self.var_status = StringVar()

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
            text="ROOM ADDING DETAILS",
            font=("times new roman", 18, "bold"),
            bg="black",
            fg="gold",
            bd=4,
            relief=RIDGE,
        )
        lbl_title.place(x=0, y=0, width=1295, height=50)

        # Left Frame - Input Form
        labelframeleft = LabelFrame(
            self.root,
            bd=2,
            relief=RIDGE,
            text="New Room Details",
            font=("times new roman", 12, "bold"),
            padx=2,
        )
        labelframeleft.place(x=5, y=50, width=425, height=490)

        # Floor Number
        lbl_floor = Label(
            labelframeleft,
            text="Floor Number:",
            font=("arial", 11, "bold"),
            padx=2,
            pady=6,
        )
        lbl_floor.grid(row=0, column=0, sticky=W)
        entry_floor = ttk.Entry(
            labelframeleft,
            textvariable=self.var_floor,
            font=("arial", 11),
            width=20,
        )
        entry_floor.grid(row=0, column=1, sticky=W)

        # Room Number
        lbl_roomNo = Label(
            labelframeleft,
            text="Room Number:",
            font=("arial", 11, "bold"),
            padx=2,
            pady=6,
        )
        lbl_roomNo.grid(row=1, column=0, sticky=W)
        entry_roomNo = ttk.Entry(
            labelframeleft,
            textvariable=self.var_roomNo,
            font=("arial", 11),
            width=20,
        )
        entry_roomNo.grid(row=1, column=1, sticky=W)

        # Room Type
        lbl_roomType = Label(
            labelframeleft,
            text="Room Type:",
            font=("arial", 11, "bold"),
            padx=2,
            pady=6,
        )
        lbl_roomType.grid(row=2, column=0, sticky=W)
        combo_roomType = ttk.Combobox(
            labelframeleft,
            textvariable=self.var_roomType,
            font=("arial", 11),
            width=18,
            state="readonly",
        )
        combo_roomType["values"] = ("Single", "Double", "Luxury", "Deluxe", "Suite")
        combo_roomType.current(0)
        combo_roomType.grid(row=2, column=1, sticky=W)

        # Room Price
        lbl_price = Label(
            labelframeleft,
            text="Price ($/Night):",
            font=("arial", 11, "bold"),
            padx=2,
            pady=6,
        )
        lbl_price.grid(row=3, column=0, sticky=W)
        entry_price = ttk.Entry(
            labelframeleft,
            textvariable=self.var_price,
            font=("arial", 11),
            width=20,
        )
        entry_price.grid(row=3, column=1, sticky=W)

        # Availability Status
        lbl_status = Label(
            labelframeleft,
            text="Room Status:",
            font=("arial", 11, "bold"),
            padx=2,
            pady=6,
        )
        lbl_status.grid(row=4, column=0, sticky=W)
        combo_status = ttk.Combobox(
            labelframeleft,
            textvariable=self.var_status,
            font=("arial", 11),
            width=18,
            state="readonly",
        )
        combo_status["values"] = ("Available", "Occupied", "Maintenance")
        combo_status.current(0)
        combo_status.grid(row=4, column=1, sticky=W)

        # Action Buttons Frame
        btn_frame = Frame(labelframeleft, bd=2, relief=RIDGE)
        btn_frame.place(x=0, y=300, width=415, height=40)

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

        # Right Side - Table View Frame
        table_frame = LabelFrame(
            self.root,
            bd=2,
            relief=RIDGE,
            text="Show Room Details",
            font=("times new roman", 12, "bold"),
        )
        table_frame.place(x=435, y=50, width=850, height=490)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.room_table = ttk.Treeview(
            table_frame,
            columns=("floor", "roomno", "roomtype", "price", "status"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set,
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.room_table.xview)
        scroll_y.config(command=self.room_table.yview)

        self.room_table.heading("floor", text="Floor")
        self.room_table.heading("roomno", text="Room No")
        self.room_table.heading("roomtype", text="Room Type")
        self.room_table.heading("price", text="Price ($)")
        self.room_table.heading("status", text="Status")

        self.room_table["show"] = "headings"
        self.room_table.column("floor", width=120)
        self.room_table.column("roomno", width=140)
        self.room_table.column("roomtype", width=180)
        self.room_table.column("price", width=140)
        self.room_table.column("status", width=160)

        self.room_table.pack(fill=BOTH, expand=1)
        self.room_table.bind("<ButtonRelease-1>", self.get_cursor_data)

    def get_db_connection(self):
        config = self.db_config.copy()
        config["database"] = "hotel_management"
        return mysql.connector.connect(**config)

    def ensure_table_exists(self):
        """Ensures database, rooms table, and required columns exist."""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS hotel_management")
            conn.close()

            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS rooms (
                    floor VARCHAR(10),
                    room_number VARCHAR(10) PRIMARY KEY,
                    room_type VARCHAR(50),
                    price DECIMAL(10,2),
                    status VARCHAR(20)
                )
                """
            )
            # Ensure floor column exists if table was created previously without it
            try:
                cursor.execute("ALTER TABLE rooms ADD COLUMN floor VARCHAR(10) FIRST")
            except mysql.connector.Error:
                pass  # Column already exists

            conn.commit()
            conn.close()
            self.fetch_table_data()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"MySQL Error: {err}")

    def add_data(self):
        if self.var_roomNo.get() == "" or self.var_price.get() == "":
            messagebox.showerror("Error", "Room Number and Price are required!")
            return

        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO rooms (floor, room_number, room_type, price, status) VALUES (%s, %s, %s, %s, %s)",
                (
                    self.var_floor.get(),
                    self.var_roomNo.get(),
                    self.var_roomType.get(),
                    self.var_price.get(),
                    self.var_status.get(),
                ),
            )
            conn.commit()
            self.fetch_table_data()
            conn.close()
            messagebox.showinfo("Success", "New room added successfully!")
            self.reset_data()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error adding room: {err}")

    def fetch_table_data(self):
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT floor, room_number, room_type, price, status FROM rooms")
            rows = cursor.fetchall()

            self.room_table.delete(*self.room_table.get_children())
            for row in rows:
                self.room_table.insert("", END, values=row)
            conn.close()
        except mysql.connector.Error as err:
            pass

    def get_cursor_data(self, event=""):
        cursor_row = self.room_table.focus()
        content = self.room_table.item(cursor_row)
        row = content["values"]

        if row:
            self.var_floor.set(row[0])
            self.var_roomNo.set(row[1])
            self.var_roomType.set(row[2])
            self.var_price.set(row[3])
            self.var_status.set(row[4])

    def update_data(self):
        if self.var_roomNo.get() == "":
            messagebox.showerror("Error", "Please specify a room number.")
            return

        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE rooms SET floor=%s, room_type=%s, price=%s, status=%s WHERE room_number=%s
                """,
                (
                    self.var_floor.get(),
                    self.var_roomType.get(),
                    self.var_price.get(),
                    self.var_status.get(),
                    self.var_roomNo.get(),
                ),
            )
            conn.commit()
            self.fetch_table_data()
            conn.close()
            messagebox.showinfo("Success", "Room details updated successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error updating room: {err}")

    def delete_data(self):
        if self.var_roomNo.get() == "":
            messagebox.showerror("Error", "Please select a room number.")
            return

        confirm = messagebox.askyesno(
            "Confirm Delete", "Are you sure you want to delete this room?"
        )
        if confirm:
            try:
                conn = self.get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM rooms WHERE room_number=%s",
                    (self.var_roomNo.get(),),
                )
                conn.commit()
                self.fetch_table_data()
                self.reset_data()
                conn.close()
                messagebox.showinfo("Success", "Room deleted successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error deleting room: {err}")

    def reset_data(self):
        self.var_floor.set("")
        self.var_roomNo.set("")
        self.var_roomType.set("Single")
        self.var_price.set("")
        self.var_status.set("Available")


if __name__ == "__main__":
    root = Tk()
    obj = DetailsRoom(root)
    obj.ensure_table_exists()
    root.mainloop()