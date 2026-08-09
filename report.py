import os
from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector


class ReportWin:

    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System - System Reports")
        self.root.geometry("1295x580+230+220")

        # Database Configuration
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "2333438",  # Replace with your MySQL password
            "database": "hotel_management",
        }

        # Title Header
        lbl_title = Label(
            self.root,
            text="HOTEL MANAGEMENT ANALYTICS & REPORTS",
            font=("times new roman", 18, "bold"),
            bg="black",
            fg="gold",
            bd=4,
            relief=RIDGE,
        )
        lbl_title.place(x=0, y=0, width=1295, height=50)

        # ---------------- Top Summary Cards ----------------
        cards_frame = Frame(self.root, bd=2, relief=RIDGE, bg="#1e1e1e")
        cards_frame.place(x=5, y=55, width=1285, height=130)

        # Card 1: Total Customers
        self.card1 = Frame(cards_frame, bg="#2c3e50", bd=2, relief=RIDGE)
        self.card1.place(x=15, y=15, width=280, height=95)
        Label(
            self.card1,
            text="TOTAL CUSTOMERS",
            font=("arial", 11, "bold"),
            bg="#2c3e50",
            fg="white",
        ).pack(pady=5)
        self.lbl_total_cust = Label(
            self.card1,
            text="0",
            font=("times new roman", 22, "bold"),
            bg="#2c3e50",
            fg="gold",
        )
        self.lbl_total_cust.pack()

        # Card 2: Total Room Bookings
        self.card2 = Frame(cards_frame, bg="#27ae60", bd=2, relief=RIDGE)
        self.card2.place(x=330, y=15, width=280, height=95)
        Label(
            self.card2,
            text="TOTAL BOOKINGS",
            font=("arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
        ).pack(pady=5)
        self.lbl_total_bookings = Label(
            self.card2,
            text="0",
            font=("times new roman", 22, "bold"),
            bg="#27ae60",
            fg="white",
        )
        self.lbl_total_bookings.pack()

        # Card 3: Total Revenue Generated
        self.card3 = Frame(cards_frame, bg="#d35400", bd=2, relief=RIDGE)
        self.card3.place(x=645, y=15, width=280, height=95)
        Label(
            self.card3,
            text="TOTAL REVENUE",
            font=("arial", 11, "bold"),
            bg="#d35400",
            fg="white",
        ).pack(pady=5)
        self.lbl_total_revenue = Label(
            self.card3,
            text="Rs. 0.00",
            font=("times new roman", 22, "bold"),
            bg="#d35400",
            fg="gold",
        )
        self.lbl_total_revenue.pack()

        # Card 4: Total Rooms Configured
        self.card4 = Frame(cards_frame, bg="#8e44ad", bd=2, relief=RIDGE)
        self.card4.place(x=960, y=15, width=280, height=95)
        Label(
            self.card4,
            text="AVAILABLE ROOMS",
            font=("arial", 11, "bold"),
            bg="#8e44ad",
            fg="white",
        ).pack(pady=5)
        self.lbl_total_rooms = Label(
            self.card4,
            text="0",
            font=("times new roman", 22, "bold"),
            bg="#8e44ad",
            fg="white",
        )
        self.lbl_total_rooms.pack()

        # ---------------- Bottom Detailed Table ----------------
        table_frame = LabelFrame(
            self.root,
            bd=2,
            relief=RIDGE,
            text="Booking Revenue Detailed Summary",
            font=("times new roman", 12, "bold"),
        )
        table_frame.place(x=5, y=190, width=1285, height=380)

        # Controls & Refresh Button
        btn_refresh = Button(
            table_frame,
            text="Refresh Data",
            command=self.load_report_data,
            font=("arial", 10, "bold"),
            bg="black",
            fg="gold",
            width=15,
        )
        btn_refresh.pack(anchor=NE, padx=10, pady=5)

        # Treeview Table
        details_frame = Frame(table_frame, bd=2, relief=RIDGE)
        details_frame.place(x=10, y=40, width=1260, height=310)

        scroll_x = ttk.Scrollbar(details_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(details_frame, orient=VERTICAL)

        self.report_table = ttk.Treeview(
            details_frame,
            columns=(
                "contact",
                "check_in",
                "check_out",
                "roomtype",
                "roomno",
                "days",
                "tax",
                "subtotal",
                "total",
            ),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set,
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.report_table.xview)
        scroll_y.config(command=self.report_table.yview)

        self.report_table.heading("contact", text="Contact No")
        self.report_table.heading("check_in", text="Check-In")
        self.report_table.heading("check_out", text="Check-Out")
        self.report_table.heading("roomtype", text="Room Type")
        self.report_table.heading("roomno", text="Room No")
        self.report_table.heading("days", text="Days Stayed")
        self.report_table.heading("tax", text="Paid Tax")
        self.report_table.heading("subtotal", text="Sub Total")
        self.report_table.heading("total", text="Total Cost")

        self.report_table["show"] = "headings"
        self.report_table.column("contact", width=130)
        self.report_table.column("check_in", width=120)
        self.report_table.column("check_out", width=120)
        self.report_table.column("roomtype", width=130)
        self.report_table.column("roomno", width=100)
        self.report_table.column("days", width=100)
        self.report_table.column("tax", width=130)
        self.report_table.column("subtotal", width=140)
        self.report_table.column("total", width=150)

        self.report_table.pack(fill=BOTH, expand=1)

        # Load data on open
        self.load_report_data()

    def get_db_connection(self):
        return mysql.connector.connect(**self.db_config)

    def load_report_data(self):
        """Fetches live aggregates and rows from the database."""
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()

            # 1. Total Customers Count
            cursor.execute("SELECT COUNT(*) FROM customer")
            cust_count = cursor.fetchone()[0]
            self.lbl_total_cust.config(text=str(cust_count))

            # 2. Total Bookings Count
            cursor.execute("SELECT COUNT(*) FROM room_booking")
            booking_count = cursor.fetchone()[0]
            self.lbl_total_bookings.config(text=str(booking_count))

            # 3. Total Revenue
            cursor.execute(
                "SELECT total FROM room_booking"
            )
            total_rows = cursor.fetchall()
            revenue_sum = 0.0
            for row in total_rows:
                # Sanitize string format (e.g. 'Rs.275.00')
                clean_val = (
                    str(row[0]).replace("Rs.", "").replace("$", "").strip()
                )
                try:
                    revenue_sum += float(clean_val)
                except ValueError:
                    pass
            self.lbl_total_revenue.config(text=f"Rs. {revenue_sum:.2f}")

            # 4. Total Configured Rooms
            try:
                cursor.execute("SELECT COUNT(*) FROM rooms")
                rooms_count = cursor.fetchone()[0]
                self.lbl_total_rooms.config(text=str(rooms_count))
            except mysql.connector.Error:
                self.lbl_total_rooms.config(text="0")

            # 5. Populate Detailed Table
            cursor.execute(
                "SELECT contact, check_in, check_out, roomtype, roomavailable, noOfdays, paidtax, subtotal, total FROM room_booking"
            )
            rows = cursor.fetchall()

            self.report_table.delete(*self.report_table.get_children())
            for row in rows:
                self.report_table.insert("", END, values=row)

            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch report data: {err}")


if __name__ == "__main__":
    root = Tk()
    obj = ReportWin(root)
    root.mainloop()