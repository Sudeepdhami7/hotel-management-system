import os
from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector


class PaymentWin:

    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System - Billing & Payment Processing")
        self.root.geometry("1295x620+230+180")

        # Database Configuration
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "2333438",  # Replace with your MySQL password
            "database": "hotel_management",
        }

        # Form Variables
        self.var_search_query = StringVar()  # Ref Code, Mobile, or Email
        self.var_ref = StringVar()
        self.var_cust_name = StringVar()
        self.var_mobile = StringVar()
        self.var_email = StringVar()
        self.var_room_no = StringVar()
        self.var_days = StringVar()
        self.var_subtotal = StringVar()
        self.var_tax = StringVar()
        self.var_total = StringVar()
        self.var_refund_amount = StringVar(value="0.00")
        self.var_payment_method = StringVar(value="Cash")
        self.var_payment_status = StringVar(value="Paid")

        # Header Title
        lbl_title = Label(
            self.root,
            text="BILLING, REFUND & PAYMENT PROCESSING",
            font=("times new roman", 18, "bold"),
            bg="black",
            fg="gold",
            bd=4,
            relief=RIDGE,
        )
        lbl_title.place(x=0, y=0, width=1295, height=50)

        # ---------------- Left Control Frame ----------------
        left_frame = LabelFrame(
            self.root,
            bd=2,
            relief=RIDGE,
            text="Customer & Billing Search",
            font=("arial", 12, "bold"),
        )
        left_frame.place(x=5, y=55, width=500, height=555)

        # Search Bar Row
        lbl_search = Label(left_frame, text="Ref / Mobile / Email:", font=("arial", 9, "bold"))
        lbl_search.grid(row=0, column=0, padx=5, pady=6, sticky=W)

        entry_search = ttk.Entry(left_frame, textvariable=self.var_search_query, font=("arial", 10), width=18)
        entry_search.grid(row=0, column=1, padx=5, pady=6)

        btn_fetch = Button(
            left_frame,
            text="Fetch Details",
            command=self.fetch_customer_and_booking,
            font=("arial", 9, "bold"),
            bg="black",
            fg="gold",
            cursor="hand2",
            width=12,
        )
        btn_fetch.grid(row=0, column=2, padx=5, pady=6)

        # Display Customer Details
        Label(left_frame, text="Ref Code:", font=("arial", 10, "bold")).grid(row=1, column=0, padx=10, pady=4, sticky=W)
        ttk.Entry(left_frame, textvariable=self.var_ref, font=("arial", 10), state="readonly").grid(row=1, column=1, columnspan=2, sticky=EW, pady=4)

        Label(left_frame, text="Customer Name:", font=("arial", 10, "bold")).grid(row=2, column=0, padx=10, pady=4, sticky=W)
        ttk.Entry(left_frame, textvariable=self.var_cust_name, font=("arial", 10), state="readonly").grid(row=2, column=1, columnspan=2, sticky=EW, pady=4)

        Label(left_frame, text="Mobile No:", font=("arial", 10, "bold")).grid(row=3, column=0, padx=10, pady=4, sticky=W)
        ttk.Entry(left_frame, textvariable=self.var_mobile, font=("arial", 10), state="readonly").grid(row=3, column=1, columnspan=2, sticky=EW, pady=4)

        # Display Booking & Financial Info
        Label(left_frame, text="Room Assigned:", font=("arial", 10, "bold")).grid(row=4, column=0, padx=10, pady=4, sticky=W)
        ttk.Entry(left_frame, textvariable=self.var_room_no, font=("arial", 10), state="readonly").grid(row=4, column=1, columnspan=2, sticky=EW, pady=4)

        Label(left_frame, text="Total Days:", font=("arial", 10, "bold")).grid(row=5, column=0, padx=10, pady=4, sticky=W)
        ttk.Entry(left_frame, textvariable=self.var_days, font=("arial", 10), state="readonly").grid(row=5, column=1, columnspan=2, sticky=EW, pady=4)

        Label(left_frame, text="Sub Total:", font=("arial", 10, "bold")).grid(row=6, column=0, padx=10, pady=4, sticky=W)
        ttk.Entry(left_frame, textvariable=self.var_subtotal, font=("arial", 10), state="readonly").grid(row=6, column=1, columnspan=2, sticky=EW, pady=4)

        Label(left_frame, text="Tax Amount:", font=("arial", 10, "bold")).grid(row=7, column=0, padx=10, pady=4, sticky=W)
        ttk.Entry(left_frame, textvariable=self.var_tax, font=("arial", 10), state="readonly").grid(row=7, column=1, columnspan=2, sticky=EW, pady=4)

        Label(left_frame, text="Net Payable:", font=("arial", 10, "bold")).grid(row=8, column=0, padx=10, pady=4, sticky=W)
        ttk.Entry(left_frame, textvariable=self.var_total, font=("arial", 11, "bold"), state="readonly").grid(row=8, column=1, columnspan=2, sticky=EW, pady=4)

        # Refund Field
        Label(left_frame, text="Refund Amount:", font=("arial", 10, "bold"), fg="red").grid(row=9, column=0, padx=10, pady=4, sticky=W)
        ttk.Entry(left_frame, textvariable=self.var_refund_amount, font=("arial", 10, "bold")).grid(row=9, column=1, columnspan=2, sticky=EW, pady=4)

        # Payment Controls
        Label(left_frame, text="Payment Method:", font=("arial", 10, "bold")).grid(row=10, column=0, padx=10, pady=4, sticky=W)
        combo_method = ttk.Combobox(
            left_frame,
            textvariable=self.var_payment_method,
            values=["Cash", "Credit Card", "Debit Card", "UPI / QR Code", "Net Banking"],
            state="readonly",
            font=("arial", 10),
        )
        combo_method.grid(row=10, column=1, columnspan=2, sticky=EW, pady=4)

        Label(left_frame, text="Payment Status:", font=("arial", 10, "bold")).grid(row=11, column=0, padx=10, pady=4, sticky=W)
        combo_status = ttk.Combobox(
            left_frame,
            textvariable=self.var_payment_status,
            values=["Paid", "Pending", "Refunded"],
            state="readonly",
            font=("arial", 10),
        )
        combo_status.grid(row=11, column=1, columnspan=2, sticky=EW, pady=4)
        combo_status.bind("<<ComboboxSelected>>", lambda e: self.generate_receipt_preview())

        # Action Buttons
        btn_frame = Frame(left_frame)
        btn_frame.grid(row=12, column=0, columnspan=3, pady=12)

        btn_process = Button(
            btn_frame,
            text="Process Payment",
            command=self.process_payment,
            font=("arial", 9, "bold"),
            bg="black",
            fg="gold",
            cursor="hand2",
            width=14,
            height=2,
        )
        btn_process.pack(side=LEFT, padx=4)

        btn_refund = Button(
            btn_frame,
            text="Process Refund",
            command=self.process_refund,
            font=("arial", 9, "bold"),
            bg="darkred",
            fg="white",
            cursor="hand2",
            width=14,
            height=2,
        )
        btn_refund.pack(side=LEFT, padx=4)

        btn_clear = Button(
            btn_frame,
            text="Reset / Clear",
            command=self.reset_fields,
            font=("arial", 9, "bold"),
            bg="gray",
            fg="white",
            cursor="hand2",
            width=12,
            height=2,
        )
        btn_clear.pack(side=LEFT, padx=4)

        # ---------------- Right Receipt Frame ----------------
        right_frame = LabelFrame(
            self.root,
            bd=2,
            relief=RIDGE,
            text="Official Invoice & Payment Status",
            font=("arial", 12, "bold"),
        )
        right_frame.place(x=510, y=55, width=775, height=555)

        self.txt_receipt = Text(right_frame, font=("courier new", 10), bg="#ffffff")
        self.txt_receipt.pack(fill=BOTH, expand=True, padx=10, pady=10)

    # Fetch Customer & Booking Data dynamically
    def fetch_customer_and_booking(self):
        query_val = self.var_search_query.get().strip()
        if query_val == "":
            messagebox.showerror("Validation Error", "Please enter a Ref Code, Mobile Number, or Email!", parent=self.root)
            return

        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            sql_cust = """
                SELECT ref, name, mobile, email 
                FROM customer 
                WHERE ref = %s OR mobile LIKE %s OR email = %s
            """
            cursor.execute(sql_cust, (query_val, f"%{query_val}%", query_val))
            cust_row = cursor.fetchone()

            if not cust_row:
                messagebox.showerror("Not Found", f"No customer found matching: {query_val}", parent=self.root)
                conn.close()
                return

            ref_code, name, mobile, email = cust_row
            self.var_ref.set(str(ref_code))
            self.var_cust_name.set(str(name))
            self.var_mobile.set(str(mobile))
            self.var_email.set(str(email))

            sql_booking = """
                SELECT roomavailable, noOfdays, subtotal, paidtax, total 
                FROM room_booking 
                WHERE contact LIKE %s OR contact = %s
            """
            cursor.execute(sql_booking, (f"%{query_val}%", str(ref_code)))
            booking_row = cursor.fetchone()

            if booking_row:
                self.var_room_no.set(str(booking_row[0]))
                self.var_days.set(str(booking_row[1]))
                self.var_subtotal.set(str(booking_row[2]))
                self.var_tax.set(str(booking_row[3]))
                self.var_total.set(str(booking_row[4]))
                self.generate_receipt_preview()
            else:
                self.var_room_no.set("N/A")
                self.var_days.set("0")
                self.var_subtotal.set("Rs. 0.00")
                self.var_tax.set("Rs. 0.00")
                self.var_total.set("Rs. 0.00")
                messagebox.showwarning("Notice", "Customer found, but no active room booking record was located.", parent=self.root)

            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to retrieve details: {err}", parent=self.root)

    # Render Invoice Preview with Dynamic Status Messages
    def generate_receipt_preview(self):
        self.txt_receipt.delete("1.0", END)
        self.txt_receipt.insert(END, "\t\t ROYAL HOTEL MANAGEMENT SYSTEM\n")
        self.txt_receipt.insert(END, "\t\t    OFFICIAL PAYMENT INVOICE\n")
        self.txt_receipt.insert(END, "=" * 65 + "\n")
        self.txt_receipt.insert(END, f" Customer Ref Code : {self.var_ref.get()}\n")
        self.txt_receipt.insert(END, f" Customer Name     : {self.var_cust_name.get()}\n")
        self.txt_receipt.insert(END, f" Mobile Number     : {self.var_mobile.get()}\n")
        self.txt_receipt.insert(END, f" Email Address     : {self.var_email.get()}\n")
        self.txt_receipt.insert(END, "-" * 65 + "\n")
        self.txt_receipt.insert(END, f" Room Assigned     : {self.var_room_no.get()}\n")
        self.txt_receipt.insert(END, f" Total Days Stayed : {self.var_days.get()}\n")
        self.txt_receipt.insert(END, "-" * 65 + "\n")
        self.txt_receipt.insert(END, f" Sub Total         : {self.var_subtotal.get()}\n")
        self.txt_receipt.insert(END, f" Applicable Tax    : {self.var_tax.get()}\n")
        self.txt_receipt.insert(END, f" Net Payable Total : {self.var_total.get()}\n")

        status = self.var_payment_status.get()
        if status == "Refunded":
            self.txt_receipt.insert(END, f" Refunded Amount   : Rs. {self.var_refund_amount.get()}\n")

        self.txt_receipt.insert(END, "=" * 65 + "\n")
        self.txt_receipt.insert(END, f" Payment Mode      : {self.var_payment_method.get()}\n")
        self.txt_receipt.insert(END, f" Payment Status    : {status}\n")
        self.txt_receipt.insert(END, "=" * 65 + "\n\n")

        # Dynamic Status Messages
        if status == "Paid":
            self.txt_receipt.insert(END, "\t *** STATUS: PAYMENT SUCCESSFUL ***\n")
            self.txt_receipt.insert(END, "\t Thank you for choosing Royal Hotel!\n")
        elif status == "Pending":
            self.txt_receipt.insert(END, "\t *** STATUS: PAYMENT PENDING ***\n")
            self.txt_receipt.insert(END, "\t PLEASE PAY THE BILL FIRST TO COMPLETE CHECKOUT!\n")
        elif status == "Refunded":
            self.txt_receipt.insert(END, "\t *** STATUS: AMOUNT REFUND PROCESSED ***\n")
            self.txt_receipt.insert(END, f"\t Total Refunded: Rs. {self.var_refund_amount.get()}\n")

    def clean_amount(self, value):
        """Strips currency text to return pure numeric float."""
        return float(
            str(value)
            .replace("Rs.", "")
            .replace("Rs", "")
            .replace("$", "")
            .strip() or 0.0
        )

    # Process Payment
    def process_payment(self):
        if self.var_ref.get() == "" or self.var_total.get() == "":
            messagebox.showerror("Error", "Please fetch customer details first!", parent=self.root)
            return

        if self.var_payment_status.get() == "Pending":
            messagebox.showwarning("Payment Pending", "Payment status is set to Pending. Please pay the bill first!", parent=self.root)
            self.generate_receipt_preview()
            return

        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            clean_total = self.clean_amount(self.var_total.get())

            sql_insert = """
                INSERT INTO payments (ref_no, cust_name, mobile, room_no, total_amount, payment_method, payment_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                sql_insert,
                (
                    self.var_ref.get(),
                    self.var_cust_name.get(),
                    self.var_mobile.get(),
                    self.var_room_no.get(),
                    clean_total,
                    self.var_payment_method.get(),
                    self.var_payment_status.get(),
                ),
            )
            conn.commit()
            conn.close()

            self.generate_receipt_preview()
            messagebox.showinfo("Success", "Payment processed and receipt generated successfully!", parent=self.root)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to record payment: {err}", parent=self.root)

    # Process Refund Action
    def process_refund(self):
        if self.var_ref.get() == "" or self.var_total.get() == "":
            messagebox.showerror("Error", "Please fetch customer details first!", parent=self.root)
            return

        try:
            refund_val = self.clean_amount(self.var_refund_amount.get())
            total_val = self.clean_amount(self.var_total.get())

            if refund_val <= 0:
                messagebox.showerror("Validation Error", "Please enter a valid refund amount greater than 0!", parent=self.root)
                return

            if refund_val > total_val:
                messagebox.showerror("Validation Error", f"Refund amount cannot exceed total bill amount (Rs. {total_val:.2f})!", parent=self.root)
                return

            # Set status to Refunded
            self.var_payment_status.set("Refunded")

            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            sql_insert = """
                INSERT INTO payments (ref_no, cust_name, mobile, room_no, total_amount, payment_method, payment_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                sql_insert,
                (
                    self.var_ref.get(),
                    self.var_cust_name.get(),
                    self.var_mobile.get(),
                    self.var_room_no.get(),
                    refund_val,  # Recorded as negative refund amount in records
                    self.var_payment_method.get(),
                    "Refunded",
                ),
            )
            conn.commit()
            conn.close()

            self.generate_receipt_preview()
            messagebox.showinfo("Refund Processed", f"Refund of Rs. {refund_val:.2f} processed successfully!", parent=self.root)
        except Exception as err:
            messagebox.showerror("Error", f"Failed to process refund: {err}", parent=self.root)

    # Reset / Clear All Fields
    def reset_fields(self):
        self.var_search_query.set("")
        self.var_ref.set("")
        self.var_cust_name.set("")
        self.var_mobile.set("")
        self.var_email.set("")
        self.var_room_no.set("")
        self.var_days.set("")
        self.var_subtotal.set("")
        self.var_tax.set("")
        self.var_total.set("")
        self.var_refund_amount.set("0.00")
        self.var_payment_method.set("Cash")
        self.var_payment_status.set("Paid")
        self.txt_receipt.delete("1.0", END)


if __name__ == "__main__":
    root = Tk()
    app = PaymentWin(root)
    root.mainloop()