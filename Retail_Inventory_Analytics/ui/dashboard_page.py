import customtkinter as ctk

from ui.header import Header
from ui.cards import DashboardCard
from ui.toolbar import Toolbar
from ui.inventory_table import InventoryTable


class DashboardPage(ctk.CTkFrame):

    def __init__(self,parent):

        super().__init__(
            parent,
            fg_color="#0F172A"
        )

        self.create_page()

    # ===========================================

    def create_page(self):

        # Header

        self.header = Header(self)

        self.header.pack(
            fill="x",
            padx=25,
            pady=20
        )

        # Welcome Card

        welcome = ctk.CTkFrame(
            self,
            height=120,
            fg_color="#1E293B",
            corner_radius=20
        )

        welcome.pack(
            fill="x",
            padx=25,
            pady=(0,20)
        )

        welcome.pack_propagate(False)

        title = ctk.CTkLabel(

            welcome,

            text="Welcome Back 👋",

            font=("Segoe UI",28,"bold")

        )

        title.pack(

            anchor="w",

            padx=25,

            pady=(20,5)

        )

        text = ctk.CTkLabel(

            welcome,

            text="Monitor inventory and business performance from one place.",

            font=("Segoe UI",15),

            text_color="lightgray"

        )

        text.pack(

            anchor="w",

            padx=25

        )

        self.create_cards()

        self.toolbar = Toolbar(self)

        self.toolbar.pack(

            fill="x",

            padx=25,

            pady=20

        )

        self.table = InventoryTable(self)

        self.table.pack(

            fill="both",

            expand=True,

            padx=25,

            pady=(0,20)

        )

    # ===========================================

    def create_cards(self):

        frame = ctk.CTkFrame(

            self,

            fg_color="transparent"

        )

        frame.pack(

            fill="x",

            padx=25,

            pady=15

        )

        DashboardCard(

            frame,

            "📦",

            "Products",

            "0"

        ).grid(

            row=0,

            column=0,

            padx=12

        )

        DashboardCard(

            frame,

            "💰",

            "Inventory Value",

            "₹0"

        ).grid(

            row=0,

            column=1,

            padx=12

        )

        DashboardCard(

            frame,

            "⚠",

            "Low Stock",

            "0"

        ).grid(

            row=0,

            column=2,

            padx=12

        )

        DashboardCard(

            frame,

            "🚚",

            "Suppliers",

            "0"

        ).grid(

            row=0,

            column=3,

            padx=12

        )