import customtkinter as ctk

from ui.header import Header
from ui.cards import DashboardCard


class DashboardPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="#0F172A"
        )

        self.card_color = "#1E293B"

        self.create_page()

    
    # Create Dashboard Page
    

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
            fg_color=self.card_color,
            height=120,
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
            font=("Segoe UI",26,"bold")
        )

        title.pack(
            anchor="w",
            padx=25,
            pady=(20,5)
        )

        subtitle = ctk.CTkLabel(
            welcome,
            text="Retail Inventory Analytics Dashboard",
            font=("Segoe UI",15),
            text_color="lightgray"
        )

        subtitle.pack(
            anchor="w",
            padx=25
        )

        # KPI Cards

        cards_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        cards_frame.pack(
            fill="x",
            padx=25,
            pady=15
        )

        self.products = DashboardCard(
            cards_frame,
            "📦",
            "Products",
            "0"
        )

        self.products.grid(
            row=0,
            column=0,
            padx=10
        )

        self.value = DashboardCard(
            cards_frame,
            "💰",
            "Inventory Value",
            "₹0"
        )

        self.value.grid(
            row=0,
            column=1,
            padx=10
        )

        self.low_stock = DashboardCard(
            cards_frame,
            "⚠️",
            "Low Stock",
            "0"
        )

        self.low_stock.grid(
            row=0,
            column=2,
            padx=10
        )

        self.suppliers = DashboardCard(
            cards_frame,
            "🚚",
            "Suppliers",
            "0"
        )

        self.suppliers.grid(
            row=0,
            column=3,
            padx=10
        )

    
    # Update KPI Cards
    

    def update_cards(self, kpis):

        self.products.update_value(
            str(kpis["products"])
        )

        self.value.update_value(
            f"₹{kpis['inventory_value']:,.0f}"
        )

        self.low_stock.update_value(
            str(kpis["low_stock"])
        )

        self.suppliers.update_value(
            str(kpis["suppliers"])
        )