import customtkinter as ctk
from datetime import datetime


class Header(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            height=90,
            corner_radius=15,
            fg_color="#1E293B"
        )

        self.pack_propagate(False)

        self.create_header()

    def create_header(self):

        # ---------------- Left Side ----------------

        left_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        left_frame.pack(
            side="left",
            padx=20,
            pady=15
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
            padx=20
        )

        today = datetime.now().strftime("%d %b %Y")

        date_label = ctk.CTkLabel(
            right_frame,
            text=f"📅 {today}",
            font=("Segoe UI", 14)
        )

        date_label.pack(anchor="e")

        admin = ctk.CTkLabel(
            right_frame,
            text="👤 Admin",
            font=("Segoe UI", 16, "bold")
        )

        admin.pack(anchor="e")