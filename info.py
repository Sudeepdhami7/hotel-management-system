from tkinter import *
from tkinter import ttk
import textwrap


class HotelInfoWin:

    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Information & Policies")
        self.root.geometry("620x560+500+200")

        # Header Title
        lbl_title = Label(
            self.root,
            text="ROYAL HOTEL INFORMATION & POLICIES",
            font=("times new roman", 16, "bold"),
            bg="black",
            fg="gold",
            bd=4,
            relief=RIDGE,
        )
        lbl_title.pack(side=TOP, fill=X)

        # Container Frame for Text and Scrollbar
        frame_text = Frame(self.root)
        frame_text.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Scrollbar Setup
        scrollbar = ttk.Scrollbar(frame_text, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Text Display Widget
        info_text = Text(
            frame_text,
            font=("arial", 10),
            wrap=WORD,
            padx=15,
            pady=15,
            yscrollcommand=scrollbar.set,
            bg="#fbfbfb",
            fg="#222222",
        )
        info_text.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=info_text.yview)

        # Formatted Hotel Details
        details = """
        ===================================================================
                               WELCOME TO ROYAL HOTEL
        ===================================================================

        📍 ADDRESS & LOCATION:
       Royal Hotel, Main Street, Jomsom
        Mustang District, Gandaki Province, Nepal
        Postal Code: 33100
        

        📞 CONTACT INFORMATION:
        Front Desk   : +977 9840 885 626
        Reservations : reservations@royalhotel.com
        Official Web : www.royalhotel.com

        ⏰ CHECK-IN / CHECK-OUT POLICIES:
        • Standard Check-in Time  : 12:00 PM
        • Standard Check-out Time : 11:00 AM
        • Early Check-in / Late Check-out subject to availability.

        🏨 AMENITIES & SERVICES INCLUDED:
        • Free High-Speed Wi-Fi Across All Rooms & Common Areas
        • 24/7 Room Service & Housekeeping Assistance
        • Complimentary Breakfast Served Daily (7:00 AM - 10:00 AM)
        • Swimming Pool, Sauna & Fitness Center Access

        📋 CANCELLATION & REFUND POLICY:
        • Full refund available for cancellations made at least 24 hours prior to check-in time.

        ===================================================================
                   Redirecting to Main Management Dashboard...
        ===================================================================
        """

        # Insert formatted text into widget
        info_text.insert(END, textwrap.dedent(details).strip())
        info_text.config(state=DISABLED)  # Make text widget read-only

        # Bottom Frame with Timer Status & Manual Skip Button
        bottom_frame = Frame(self.root, bg="black", bd=2, relief=RIDGE)
        bottom_frame.pack(side=BOTTOM, fill=X)

        lbl_timer = Label(
            bottom_frame,
            text="Opening Dashboard automatically...",
            font=("arial", 10, "italic"),
            bg="black",
            fg="gold",
        )
        lbl_timer.pack(side=LEFT, padx=15, pady=8)

        btn_skip = Button(
            bottom_frame,
            text="Skip to Dashboard >>",
            command=self.open_hotel_dashboard,
            font=("arial", 9, "bold"),
            bg="gold",
            fg="black",
            cursor="hand2",
        )
        btn_skip.pack(side=RIGHT, padx=15, pady=8)

        # Automatic Timer Setup: 5000 ms = 5 seconds
        # Change 5000 to 60000 for 1 minute or 180000 for 3 minutes
        self.delay_time = 5000 
        self.root.after(self.delay_time, self.open_hotel_dashboard)

    def open_hotel_dashboard(self):
        """Destroys current info window and opens main hotel dashboard."""
        try:
            self.root.destroy()  # Close current window
            
            import tkinter as tk
            from hotel import HotelManagementSystem

            hotel_root = tk.Tk()
            app = HotelManagementSystem(hotel_root)
            hotel_root.mainloop()
        except Exception as e:
            pass


if __name__ == "__main__":
    root = Tk()
    app = HotelInfoWin(root)
    root.mainloop()