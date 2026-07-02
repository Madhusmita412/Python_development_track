import customtkinter as ctk
from datetime import datetime


class Header(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            height=100,
            corner_radius=20,
            fg_color="#1E293B"
        )

        self.pack_propagate(False)

        self.create_header()

   
    # Create Header
   

    def create_header(self):

        # ---------------- Left Side ----------------

        left_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        left_frame.pack(
            side="left",
            padx=25,
            pady=18
        )

        title = ctk.CTkLabel(
            left_frame,
            text="Retail Inventory Analytics Dashboard",
            font=("Segoe UI", 28, "bold")
        )

        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            left_frame,
            text="Inventory Management & Business Intelligence Platform",
            font=("Segoe UI", 14),
            text_color="gray80"
        )

        subtitle.pack(anchor="w")

        # ---------------- Right Side ----------------

        right_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        right_frame.pack(
            side="right",
            padx=25,
            pady=15
        )

        # Date

        today = datetime.now().strftime("%d %b %Y")

        date_label = ctk.CTkLabel(
            right_frame,
            text=f"📅 {today}",
            font=("Segoe UI", 14)
        )

        date_label.pack(anchor="e")

        # Theme Switch

        self.theme_switch = ctk.CTkSwitch(
            right_frame,
            text="🌙 Dark Mode",
            command=self.toggle_theme
        )

        self.theme_switch.select()

        self.theme_switch.pack(
            anchor="e",
            pady=(12, 0)
        )

        # Admin

        admin = ctk.CTkLabel(
            right_frame,
            text="👤 Admin",
            font=("Segoe UI", 16, "bold")
        )

        admin.pack(
            anchor="e",
            pady=(12, 0)
        )

   
    # Theme Switch
   

    def toggle_theme(self):

        if self.theme_switch.get():

            ctk.set_appearance_mode("Dark")

            self.theme_switch.configure(
                text="🌙 Dark Mode"
            )

        else:

            ctk.set_appearance_mode("Light")

            self.theme_switch.configure(
                text="☀ Light Mode"
            )