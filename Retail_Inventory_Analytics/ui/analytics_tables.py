import customtkinter as ctk
from tkinter import ttk


class AnalyticsTables(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.create_layout()

    # =====================================================
    # Create Layout
    # =====================================================

    def create_layout(self):

        title = ctk.CTkLabel(
            self,
            text="📋 Inventory Insights",
            font=("Segoe UI", 24, "bold")
        )

        title.pack(
            anchor="w",
            padx=10,
            pady=(10, 20)
        )

        container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        container.pack(
            fill="both",
            expand=True
        )

        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)

        # Left Table
        self.create_top_products(container)

        # Right Table
        self.create_low_stock(container)

    # =====================================================
    # Top Products
    # =====================================================

    def create_top_products(self, parent):

        frame = ctk.CTkFrame(
            parent,
            fg_color="#1E293B",
            corner_radius=18
        )

        frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10)
        )

        title = ctk.CTkLabel(
            frame,
            text="🏆 Top Products",
            font=("Segoe UI", 18, "bold")
        )

        title.pack(
            anchor="w",
            padx=15,
            pady=15
        )

        columns = (

            "Product",

            "Category",

            "Stock",

            "Price",

            "Value"

        )

        self.top_tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
            height=8
        )

        for col in columns:

            self.top_tree.heading(
                col,
                text=col
            )

            self.top_tree.column(
                col,
                width=110,
                anchor="center"
            )

        self.top_tree.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0,15)
        )

    # =====================================================
    # Low Stock Table
    # =====================================================

    def create_low_stock(self, parent):

        frame = ctk.CTkFrame(
            parent,
            fg_color="#1E293B",
            corner_radius=18
        )

        frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(10,0)
        )

        title = ctk.CTkLabel(
            frame,
            text="⚠ Low Stock Alerts",
            font=("Segoe UI",18,"bold")
        )

        title.pack(
            anchor="w",
            padx=15,
            pady=15
        )

        columns = (

            "Product",

            "Stock",

            "Reorder",

            "Status"

        )

        self.low_tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
            height=8
        )

        for col in columns:

            self.low_tree.heading(
                col,
                text=col
            )

            self.low_tree.column(
                col,
                width=120,
                anchor="center"
            )

        self.low_tree.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0,15)
        )

    # =====================================================
    # Update Tables
    # =====================================================

    def update_tables(self, dataframe):

        for item in self.top_tree.get_children():
            self.top_tree.delete(item)

        for item in self.low_tree.get_children():
            self.low_tree.delete(item)

        if dataframe.empty:
            return

        # --------------------------
        # Top Products
        # --------------------------

        top = dataframe.copy()

        top["Value"] = (
            top["Stock"] *
            top["Price"]
        )

        top = top.sort_values(
            "Value",
            ascending=False
        ).head(10)

        for _, row in top.iterrows():

            self.top_tree.insert(

                "",

                "end",

                values=(

                    row["Product Name"],

                    row["Category"],

                    row["Stock"],

                    f"₹{row['Price']:,.0f}",

                    f"₹{row['Value']:,.0f}"

                )

            )

        # --------------------------
        # Low Stock
        # --------------------------

        low = dataframe[

            dataframe["Stock"] <=

            dataframe["Reorder Level"]

        ]

        for _, row in low.iterrows():

            self.low_tree.insert(

                "",

                "end",

                values=(

                    row["Product Name"],

                    row["Stock"],

                    row["Reorder Level"],

                    row["Status"]

                )

            )